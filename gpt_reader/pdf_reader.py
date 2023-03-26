from PyPDF2 import PdfReader
import openai
from .paper.paper import Paper
import pickle
from gpt_reader.bot.openai import ReaderBot, OpenAIBotCore
from gpt_reader.paper.paper import Paper


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

    def __init__(self, openai_key):

        # Setting the API key to use the OpenAI API
        openai.api_key = openai_key
        self.bot_core = OpenAIBotCore(api_key='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')
        self.bot = ReaderBot(self.bot_core)

    def summarize(self, paper: Paper):
        paper = self.bot.read_paper(paper)
        return paper.paper_summaries

    def question(self, paper, question):
        return self.bot.question(paper, question)
