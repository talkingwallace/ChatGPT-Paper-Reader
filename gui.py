import gradio as gr

from gpt_reader.pdf_reader import PaperReader
from gpt_reader.prompt import BASE_POINTS


class GUI:
    def __init__(self):
        self.api_key = ""
        self.session = ""

    def analyse(self, api_key, pdf_file):
        self.session = PaperReader(api_key, points_to_focus=BASE_POINTS)
        return self.session.read_pdf_and_summarize(pdf_file)

    def ask_question(self, question):
        if self.session == "":
            return "Please upload PDF file first!"
        return self.session.question(question)


with gr.Blocks() as demo:
    gr.Markdown(
        """
        # CHATGPT-PAPER-READER
        """)

    with gr.Tab("Upload PDF File"):
        pdf_input = gr.File(label="PDF File")
        api_input = gr.Textbox(label="OpenAI API Key")
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
    upload_button.click(fn=app.analyse, inputs=[api_input, pdf_input], outputs=result)
    ask_button.click(app.ask_question, inputs=question_input, outputs=answer)

if __name__ == "__main__":
    demo.title = "CHATGPT-PAPER-READER"
    demo.launch(server_port=2333)  # add "share=True" to share CHATGPT-PAPER-READER app on Internet.
