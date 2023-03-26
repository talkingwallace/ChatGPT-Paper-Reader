import pickle
from gpt_reader.bot.openai import ReaderBot, OpenAIBotCore
from gpt_reader.paper.paper import Paper
from gpt_reader.pdf_reader import PaperReader

reader = PaperReader(openai_key='')

# bot = ReaderBot(bot_core)
paper = Paper('./alexnet.pdf')
summary = reader.summarize(paper)
