from gpt_reader.paper.paper import Paper
import openai
from typing import List
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
import json
import tqdm
import tiktoken


BASE_POINTS = """
1. Who are the authors?
2. What is the process of the proposed method?
3. What is the performance of the proposed method? Please note down its performance metrics.
4. What are the baseline models and their performances? Please note down these baseline methods.
5. What dataset did this paper use?
"""


class OpenAIBotCore(object):

    def __init__(self, api_key, model='gpt-3.5-turbo', temperature=0.2, context_size=4096, proxy=None) -> None:
        openai.api_key = api_key
        openai.proxy = proxy
        self.model = model
        self.temperature = temperature
        self.context_szie = context_size

    def communicate(self, msg: List[dict], return_raw_text=True):
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=msg,
            temperature=self.temperature
        )

        if return_raw_text:
            return response["choices"][0]["message"]["content"]
        else:
            return response
        


class ReaderBot(object):

    def __init__(self, bot_core: OpenAIBotCore, points_to_focus=BASE_POINTS) -> None:
        self.bot_core = bot_core
        self.enc = tiktoken.encoding_for_model(bot_core.model)
        self.points_to_focus = points_to_focus
        self.read_buff = 300
        self.question_msg = None

    def init_prompt(self, text):
        prompt = [
            {"role": "system", "content": text},
        ]

        return prompt


    def parse_pdf_title(self, pdf_path, title_length_filter=30):

        init_prompt = """
            You are a researcher helper bot. Now I will give several texts and you help me to find out which of them are the section titles of a research paper.
            You must return me in this json format:
            {
                "titles": ["section title text", "section title text", ...]
            }
            If the title has a number, the number MUST be retained!!!!
            """

        possible_titles = []
        for page_layout in extract_pages(pdf_path):
            for element in page_layout:
                if isinstance(element, LTTextContainer):
                    
                    txt = element.get_text()
                    if len(txt) <= title_length_filter and len(txt) > 3:
                        possible_titles.append(txt)

        msg = self.init_prompt(init_prompt)
        msg.append({
            "role": "user", "content": "This are the texts: {}".format(possible_titles)
        })

        ret = self.bot_core.communicate(msg)
        rs = json.loads(ret)
        return rs
    
    def read_from_path(self, ):
        pass

    def drop_conversation_(self, msg, keep_round=3):
        # This method is used to drop previous messages from the conversation and keep only recent ones
        if len(msg) >= (keep_round + 1) * 2 + 1:
            new_msg = [msg[0]]
            for i in range(3, len(msg)):
                new_msg.append(msg[i])
            return new_msg
        else:
            return msg
        
    def drop_conversation(self, msg, context_size):
        total_len = self.count_token(msg)
        if total_len < context_size - self.read_buff:  # incase the count not correct
            return msg
        else:
            acc = 0
            drop = [False for i in range(len(msg))]
            idx = 1
            for send, resp in zip(msg[1::2], msg[2::2]):
                len_ = self.count_token([send, resp])
                drop[idx] = True
                drop[idx+1] = True
                idx += 2
                if total_len - (len_ + acc) >= (context_size - self.read_buff):
                    acc += len_
                else:
                    break
            new_msg = []
            for i, d in zip(msg, drop):
                if d:
                    continue
                else:
                    new_msg.append(i)
            return new_msg
        
        
    def count_token(self, msg):
        token_len = 0
        for i in msg:
            token_len += len(self.enc.encode(i['content']))
        return token_len
        
    def read_paper(self, paper: Paper):

        # prepare paper
        if not paper.has_catelogue():
            print('Beep....Beep....Beep.... Parsing')
            titles = self.parse_pdf_title(paper.pdf_path)
            paper.set_catelogue(titles['titles'])
        paper.split_paper_by_titles()
        tokens = paper.compute_part_tokens()
        print('Beep....Beep....Beep.... I am reading')

        reading_prompt = """
        You are a researcher helper bot. You can help the user with research paper reading and summarizing. \n
        Now I am going to send you a paper. You need to read it and summarize it for me part by part. \n
        When you are reading, You need to focus on these key points:{},

        And You need to generate a brief but informative summary for this part in one sentence.
        Your return format:
        - summary: '...'
        """.format(self.points_to_focus)

        msg = self.init_prompt(reading_prompt)
        # Reading and summarizing each part of the research paper
        summaries = []
        for (title, contents) in tqdm.tqdm(paper.paper_parts):

            # Adding the user message to the conversation messages
            new_msg = {"role": "user", "content": 'now I send you page part {}：{}'.format(title, contents)}
            msg.append(new_msg)
            # Sending the messages to the API and getting the response
            msg = self.drop_conversation(msg, self.bot_core.context_szie)
            response = self.bot_core.communicate(msg)
            resp = {"role":"system", "content": response}
            msg.append(resp)
            # Dropping previous conversation messages to keep the conversation history short
            summaries.append((title, response))

        paper.paper_summaries.extend(summaries)
        print('Bzzzt-klonk... Reading Done, I have built memories for this paper.')
        return paper

    def question(self, paper: Paper, question_str):
        
        prompt = """
        You are a researcher helper bot. You can answer the user's questions about the paper based on the 
        summaries of the paper.
        This is the summary of the paper:
        {}
        """.format(paper.paper_summaries)

        reply_format = """
        You need to find out realted sections and reply me ONLY in this json format:
        {{"reply": "..."
          "related_sections": ["section title", "section title", ...]
        }}
        """

        if self.question_msg is None:
            self.question_msg = [{'role': 'system', 'content': prompt}]
        
        self.question_msg.append({'role': 'user', 'content': """Now I send you the quenstion: {} \n   
                        """.format(question_str)})
        ret = self.bot_core.communicate(self.question_msg)
        self.question_msg.append({'role': 'system', 'content': ret})
        return ret
