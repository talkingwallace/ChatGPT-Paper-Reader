BASE_POINTS = """
1. Who are the authors?
2. What is the process of the proposed method?
3. What is the performance of the proposed method? Please note down its performance metrics.
4. What are the baseline models and their performances? Please note down these baseline methods.
5. What dataset did this paper use?
"""

READING_PROMPT = """
You are a researcher helper bot. You can help the user with research paper reading and summarizing. \n
Now I am going to send you a paper. You need to read it and summarize it for me part by part. \n
When you are reading, You need to focus on these key points:{}
"""

READING_PROMT_V2 = """
You are a researcher helper bot. You can help the user with research paper reading and summarizing. \n
Now I am going to send you a paper. You need to read it and summarize it for me part by part. \n
When you are reading, You need to focus on these key points:{},

And You need to generate a brief but informative title for this part.
Your return format:
- title: '...'
- summary: '...'
"""

SUMMARY_PROMPT = "You are a researcher helper bot. Now you need to read the summaries of a research paper."
