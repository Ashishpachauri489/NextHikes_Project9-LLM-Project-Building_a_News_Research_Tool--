# 🧠 LLM Project: Buiding a News Research Assistant  
 Real-Time Professional AI-Powered News Equity Research Assistant using LangChain, Groq & NewsAPI

[![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge)](https://www.python.org/downloads/release/python-3130a1/)
[![LangChain](https://img.shields.io/badge/LangChain%20+%20Groq-News%20API-orange?style=for-the-badge)](https://www.langchain.com/)

</div>

---

## 📌 Project Overview

The **News Research Assistant** is an interactive web app that allows users to:

- 🔍 Search for any trending topic (e.g. "AI in healthcare", "Global warming", "Climate changes news")
- 📡 Fetch real-time articles using **NewsAPI**
- 🧠 Generate crisp, point-wise summaries using **Groq's llama-3.3** via **LangChain**
- 🖥️ Use a simple, secure **Streamlit interface**
- 📥 Download summaries as `.txt` or `.pdf`.json
- 📚 See previous query history,clear query,

---

## 🚀 Key Features

- 🔐 Login-required access (username/password)
- 🔍 Real-time topic-based news search
- 🧠 Short bullet-style summarization using LLM
- 📁 Export summaries in multiple formats
- 💡 
- 🕓 Past 5-query history preview,total query,show stats

---

## 🧰 Built With

| Component       | Purpose                           |
|------------------|-----------------------------------|
| 🐍 Python 3.12    | Base language                     |
| 🧠 Groq (llama-3.3)  | Fast LLM summarization            |
| 🦜 LangChain      | LLM orchestration logic           |
| 🌐 NewsAPI        | Real-time news data               |
| 🌿 Streamlit      | Web app frontend                  |
| 🧾 ReportLab      | multiple file  export generation             |
| 🔐 python-dotenv  | Secure API key loading            |

---

## 📁 File Structure

```

├── main.py               # Streamlit interface
├── langchain_config.py  # LLM + NewsAPI setup
├── requirements.txt     # Python dependencies
├── README.md            # This documentation

```

## 📒 Note:
- API keys (GROQ_API_KEY and NEWS_API_KEY) are securely stored in Streamlit Secrets rather than in a .env or .secrets file, unlike during development in VS Code.
- This is to prevent exposure on GitHub, where keys in .env files can be automatically revoked by GitHub or Groq for security reasons.

---

## 🙋‍♂️ About Me

**Ashish Pachauri**  
HR Development | Data Science Intern  
✅ Automated 80%+ of manual processes at my workplace  
📊 Skilled in Python, Power BI, SQL, Google Apps Script, ML, DL, NLP GEN AI, Agentic AI 
<p align="left">
  📫 <strong>Connect with me:</strong>&nbsp;

  <a href="https://linkedin.com/in/ashish-pachauri-62853a143">
    <img src="https://img.shields.io/badge/LinkedIn-View_Profile-blue?logo=linkedin&logoColor=white" />
  </a>

  <a href="mailto:Ashish.pachauri@yahoo.com">
    <img src="https://img.shields.io/badge/Gmail-Mail_Me-red?logo=gmail&logoColor=white" />
  </a>
  
</p>

---

⭐ If you found this project helpful, don’t forget to **star this repo** and stay connected!

---

## 🧠 Powered By

- [LangChain](https://www.langchain.com/)  
- [Groq API](https://console.groq.com/)  
- [NewsAPI](https://newsapi.org/)  
- [Streamlit](https://streamlit.io/)

> ✨Engineered to deliver high-fidelity research and actionable insights through live LLM integration.
