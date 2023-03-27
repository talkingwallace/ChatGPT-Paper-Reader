import pickle
from gpt_reader.paper.paper import Paper
from gpt_reader.pdf_reader import PaperReader

reader = PaperReader(openai_key='')
paper = Paper('./alexnet.pdf')
summary = reader.summarize(paper)

# save paper & load
pickle.dump(paper, open('digested_paper.pkl', 'wb'))
paper = pickle.load(open('digested_paper.pkl', 'rb'))
print(paper.paper_summaries)


# ask some question about this paper
reader.question(paper, 'The author of this paper?')
reader.question(paper, 'What is CNN?')
reader.question(paper, 'What does dataset this paper use?')