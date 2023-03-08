from PyPDF2 import PdfReader
import openai
from .prompt import BASE_POINTS, READING_PROMT_V2
from .paper import Paper
from .model_interface import OpenAIModel


# Setting the API key to use the OpenAI API
class PaperReader:

    """
    A class for summarizing research papers using the OpenAI API.

    Attributes:
        openai_key (str): The API key to use the OpenAI API.
        token_length (int): The length of text to send to the API at a time.
        model (str): The GPT model to use for summarization.
        points_to_focus (str): The key points to focus on while summarizing.
        verbose (bool): A flag to enable/disable verbose logging.

    """

    def __init__(self, openai_key, token_length=4000, model="gpt-3.5-turbo",
                 points_to_focus=BASE_POINTS, verbose=False):

        # Setting the API key to use the OpenAI API
        openai.api_key = openai_key

        # Initializing prompts for the conversation
        self.init_prompt = READING_PROMT_V2.format(points_to_focus)

        self.summary_prompt = 'You are a researcher helper bot. Now you need to read the summaries of a research paper.'
        self.messages = []  # Initializing the conversation messages
        self.summary_msg = []  # Initializing the summary messages
        self.token_len = token_length  # Setting the token length to use
        self.keep_round = 2  # Rounds of previous dialogues to keep in conversation
        self.model = model  # Setting the GPT model to use
        self.verbose = verbose  # Flag to enable/disable verbose logging
        self.model = OpenAIModel(api_key=openai_key, model=model)

    def drop_conversation(self, msg):
        # This method is used to drop previous messages from the conversation and keep only recent ones
        if len(msg) >= (self.keep_round + 1) * 2 + 1:
            new_msg = [msg[0]]
            for i in range(3, len(msg)):
                new_msg.append(msg[i])
            return new_msg
        else:
            return msg

    def send_msg(self, msg):
        return self.model.send_msg(msg)

    def _chat(self, message):
        # This method is used to send a message and get a response from the OpenAI API

        # Adding the user message to the conversation messages
        self.messages.append({"role": "user", "content": message})
        # Sending the messages to the API and getting the response
        response = self.send_msg(self.messages)
        # Adding the system response to the conversation messages
        self.messages.append({"role": "system", "content": response})
        # Dropping previous conversation messages to keep the conversation history short
        self.messages = self.drop_conversation(self.messages)
        # Returning the system response
        return response

    def summarize(self, paper: Paper):
        # This method is used to summarize a given research paper

        # Adding the initial prompt to the conversation messages
        self.messages = [
            {"role": "system", "content": self.init_prompt},
        ]
        # Adding the summary prompt to the summary messages
        self.summary_msg = [{"role": "system", "content": self.summary_prompt}]

         # Reading and summarizing each part of the research paper
        for (page_idx, part_idx, text) in paper.iter_pages():
            print('page: {}, part: {}'.format(page_idx, part_idx))
            # Sending the text to the API and getting the response
            summary = self._chat('now I send you page {}, part {}：{}'.format(page_idx, part_idx, text))
            # Logging the summary if verbose logging is enabled
            if self.verbose:
                print(summary)
            # Adding the summary of the part to the summary messages
            self.summary_msg.append({"role": "user", "content": '{}'.format(summary)})

        # Adding a prompt for the user to summarize the whole paper to the summary messages
        self.summary_msg.append({"role": "user", "content": 'Now please make a summary of the whole paper'})
        # Sending the summary messages to the API and getting the response
        result = self.send_msg(self.summary_msg)
        # Returning the summary of the whole paper
        return result

    def read_pdf_and_summarize(self, pdf_path):
        # This method is used to read a research paper from a PDF file and summarize it
        
        # Creating a PdfReader object to read the PDF file
        pdf_reader = PdfReader(pdf_path)
        paper = Paper(pdf_reader)
        # Summarizing the full text of the research paper and returning the summary
        print('reading pdf finished')
        summary = self.summarize(paper)
        return summary

    def get_summary_of_each_part(self):
        # This method is used to get the summary of each part of the research paper
        return self.summary_msg

    def question(self, question):
        # This method is used to ask a question after summarizing a paper

        # Adding the question to the summary messages
        self.summary_msg.append({"role": "user", "content": question})
        # Sending the summary messages to the API and getting the response
        response = self.send_msg(self.summary_msg)
        # Adding the system response to the summary messages
        self.summary_msg.append({"role": "system", "content": response})
        # Returning the system response
        return response
