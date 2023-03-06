from gpt_reader.pdf_reader import PaperReader

api_key = 'Your api key'
session = PaperReader(api_key)
summary = session.read_pdf_and_summarize('./alexnet.pdf')

print(summary)