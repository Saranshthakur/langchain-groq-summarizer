import validators, streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader


## Streamlit APP
st.set_page_config(page_title="LangChain Summarizer: YouTube & Web", page_icon="🦜")
st.title("LangChain Summarizer: YouTube & Web")
st.subheader("Summarize a URL")


## Get the Groq API Key and URL (YouTube or website) to be summarized
with st.sidebar:
    groq_token = st.text_input("Groq API Key", value="", type="password")

target_url = st.text_input("Paste URL here", label_visibility="collapsed")

## Gemma model using Groq API
chat_model = ChatGroq(model="Gemma-7b-It", groq_api_key=groq_token)

prompt_text = """
Summarize the content below in ~300 words. Be clear and concise.
Content: {text}
"""
prompt_tpl = PromptTemplate(template=prompt_text, input_variables=["text"])

if st.button("Generate Summary"):
    ## Validate inputs
    if not groq_token.strip() or not target_url.strip():
        st.error("Missing inputs: add your Groq key and a URL.")
    elif not validators.url(target_url):
        st.error("Invalid URL. Provide a valid YouTube or website link.")
    else:
        try:
            with st.spinner("Processing..."):
                ## Load website or YouTube data
                if "youtube.com" in target_url:
                    data_loader = YoutubeLoader.from_youtube_url(target_url, add_video_info=True)
                else:
                    data_loader = UnstructuredURLLoader(
                        urls=[target_url],
                        ssl_verify=False,
                        headers={
                            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
                        },
                    )
                documents = data_loader.load()

                ## Summarization chain
                summarize_chain = load_summarize_chain(chat_model, chain_type="stuff", prompt=prompt_tpl)
                summary_text = summarize_chain.run(documents)

                st.success(summary_text)
        except Exception as err:
            st.exception(f"Exception: {err}")
