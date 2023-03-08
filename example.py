from gpt_reader.pdf_reader import PaperReader, BASE_POINTS

api_key = ''
session = PaperReader(api_key, points_to_focus=BASE_POINTS)
summary = session.read_pdf_and_summarize('./alexnet.pdf')
 
print(summary)
