import pickle
from gpt_reader.paper.paper import Paper
from gpt_reader.pdf_reader import PaperReader

reader = PaperReader(openai_key='')
paper = Paper('./alexnet.pdf')
summary = reader.summarize(paper)

# save paper & load
pickle.dump(paper, open('digested_paper.pkl', 'wb'))
paper = pickle.load(open('digested_paper.pkl', 'rb'))
# print summary of a section
print(paper.paper_summaries[4])

print(reader.question(paper, 'Describe the proposed method in details.'))