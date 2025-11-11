# 🦜 LangChain Summarizer: YouTube & Web

A simple Streamlit app that summarizes YouTube videos or website content using Groq’s Gemma-7B-It model and LangChain. Paste a URL, click one button, and get a clear ~300-word summary.

## How It Works
Users enter a Groq API key and a URL. The app detects whether it’s a YouTube or general web link:
- **YouTube:** `YoutubeLoader` extracts transcripts.
- **Websites:** `UnstructuredURLLoader` fetches readable HTML text.

The loaded text is processed through a LangChain summarization chain (`stuff` type) with a custom prompt, then summarized using `ChatGroq`.

## Stack
- **LangChain** for LLM orchestration  
- **Groq** Gemma-7B-It for summarization  
- **Streamlit** for the web interface  
- **Unstructured** and **YouTube loaders** for text extraction  



