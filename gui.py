import gradio as gr
from gpt_reader.paper.paper import Paper
from gpt_reader.pdf_reader import PaperReader


class GUI:
    def __init__(self):
        self.api_key = ""
        self.proxy = None # {'http': xxxx, 'https': xxxx}
        self.session = ""
        self.paper = None

    def analyse(self, api_key, pdf_file, http_proxy):
        if http_proxy:  # if do not provide http_proxy, use the value in __init__ function
            self.proxy = {'http': http_proxy, 'https': http_proxy}
        if api_key:  # if do not provide api_key, use the value in __init__ function
            self.api_key = api_key
        self.session = PaperReader(self.api_key, proxy=self.proxy)
        self.paper = Paper(pdf_file.name)
        return self.session.summarize(self.paper)

    def ask_question(self, question):
        if self.session == "":
            return "Please upload PDF file first!"
        return self.session.question(self.paper, question)


with gr.Blocks() as demo:
    gr.Markdown(
        """
        # CHATGPT-PAPER-READER
        """)

    with gr.Tab("Upload PDF File"):
        pdf_input = gr.File(label="PDF File")
        api_input = gr.Textbox(label="OpenAI API Key, sk-***")
        http_proxy = gr.Textbox(label="Proxy, http://***:***, leave blank if you do not need proxy")
        result = gr.Textbox(label="PDF Summary")
        upload_button = gr.Button("Start Analyse")
    with gr.Tab("Ask question about your PDF"):
        question_input = gr.Textbox(label="Your Question", placeholder="Authors of this paper?")
        answer = gr.Textbox(label="Answer")
        ask_button = gr.Button("Ask")
    with gr.Accordion("About this project"):
        gr.Markdown(
            """## CHATGPT-PAPER-READER📝 
            This repository provides a simple interface that utilizes the gpt-3.5-turbo 
            model to read academic papers in PDF format locally. You can use it to help you summarize papers, 
            create presentation slides, or simply fulfill tasks assigned by your supervisor.\n 
            [Github](https://github.com/talkingwallace/ChatGPT-Paper-Reader)""")

    app = GUI()
    upload_button.click(fn=app.analyse, inputs=[api_input, pdf_input, http_proxy], outputs=result)
    ask_button.click(app.ask_question, inputs=question_input, outputs=answer)

if __name__ == "__main__":
    demo.title = "CHATGPT-PAPER-READER"
    demo.launch(server_port=2333)  # add "share=True" to share CHATGPT-PAPER-READER app on Internet.
