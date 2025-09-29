import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from newsapi import NewsApiClient

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
news_api_key = os.getenv("NEWS_API_KEY")

llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.3-70b-versatile", temperature=0.3)


enhanced_template = """
You are an intelligent and unbiased AI summarizer.

Your job is to summarize real-time news based on the provided articles and the user query.

✅ Please ensure:
• The summary is accurate, factual, and fresh
• The summary must clearly cover the full incident, including place, time and reflect all relevant and recent developments, if any.
• Each bullet starts with a strong unique point or fact with no repitition
• Use exactly 5 to 8 bullets, prefixed with "•"
• Avoid repeating the query or giving generic summaries
• Start the summary with your strongest bullet — do NOT prefix it with any label like 'Top News Header'
• Do NOT add conclusions, advice, or any extra fluff
• NEVER invent information — rely strictly on what’s in the article content

---

📝 User Query:
{query}

📰 News Article Content:
{summaries}

---

📌 Return only the final bullet-point summary below:
"""

prompt = PromptTemplate(template=enhanced_template, input_variables=["query", "summaries"])
llm_chain = LLMChain(prompt=prompt, llm=llm)
newsapi = NewsApiClient(api_key=news_api_key)

def get_news_articles(query):
    return newsapi.get_everything(q=query, language='en', sort_by='publishedAt', page_size=10).get("articles", [])

def summarize_articles(articles):
    return ' '.join(
        article.get('description') or article.get('content') or ''
        for article in articles
    )
    
def get_summary(query):
    articles = get_news_articles(query)
    summaries = summarize_articles(articles)

    if not summaries.strip():
        return "⚠️ No content found to summarize. Try another topic.", []

    used_articles = [a for a in articles if a.get('description') or a.get('content')]
    summary_output = llm_chain.run(query=query, summaries=summaries)

    return summary_output, used_articles