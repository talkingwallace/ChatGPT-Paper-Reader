import openai
from .paper.paper import Paper
from gpt_reader.bot.openai import ReaderBot, OpenAIBotCore
from gpt_reader.paper.paper import Paper
from gpt_reader.bot.openai import BASE_POINTS


# Setting the API key to use the OpenAI API
class PaperReader:

    """
    This class is used to read a paper and summarize it.

    Parameters
    ----------
    openai_key : str
        The API key to use the OpenAI API.
    focus_points : str
        The points to focus on when summarizing the paper.
    """

    def __init__(self, openai_key, points_to_focus=BASE_POINTS, proxy=None):

        # Setting the API key to use the OpenAI API
        openai.api_key = openai_key
        openai.proxy = proxy
        self.bot_core = OpenAIBotCore(api_key=openai_key, proxy=proxy)
        self.bot = ReaderBot(self.bot_core, points_to_focus=points_to_focus)

    def summarize(self, paper: Paper):
        paper = self.bot.read_paper(paper)
        return paper.paper_summaries

    def question(self, paper, question):
        return self.bot.question(paper, question)
