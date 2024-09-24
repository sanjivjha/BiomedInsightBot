import streamlit as st
import sys
from metapub import PubMedFetcher
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA, LLMChain
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.chat_models import BedrockChat
import boto3
import concurrent.futures
from scholarly import scholarly

def fetch_pubmed_abstract(fetch, pmid):
    try:
        article = fetch.article_by_pmid(pmid)
        return {
            "title": article.title,
            "authors": ', '.join(article.authors),
            "journal": article.journal,
            "year": article.year,
            "pmid": pmid,
            "citation": f"{', '.join(article.authors)}. {article.title}. {article.journal}. {article.year};{article.volume}({article.issue}):{article.pages}.",
            "abstract": article.abstract,
            "source": "PubMed"
        }
    except:
        return None

def fetch_scholar_article(article):
    try:
        return {
            "title": article['bib']['title'],
            "authors": ', '.join(article['bib']['author']),
            "journal": article['bib'].get('journal', 'Journal not specified'),
            "year": article['bib'].get('pub_year', 'Year not specified'),
            "citation": article['bib']['citation'] if 'citation' in article['bib'] else f"{', '.join(article['bib']['author'])}. {article['bib']['title']}. {article['bib'].get('journal', 'Journal not specified')}. {article['bib'].get('pub_year', 'Year not specified')}.",
            "abstract": article['bib'].get('abstract', 'Abstract not available'),
            "source": "Google Scholar"
        }
    except:
        return None

def create_vector_store(articles):
    texts = [f"Title: {art['title']}\nAbstract: {art['abstract']}\nCitation: {art['citation']}" for art in articles]
    embeddings = HuggingFaceEmbeddings()
    vector_store = FAISS.from_texts(texts, embeddings)
    return vector_store

def get_bedrock_client():
    return boto3.client(service_name='bedrock-runtime', region_name='us-east-1')

def setup_llm():
    bedrock_client = get_bedrock_client()
    return BedrockChat(
        model_id="anthropic.claude-3-sonnet-20240229-v1:0",
        client=bedrock_client,
        model_kwargs={"temperature": 0.3, "max_tokens": 500}
    )

def enhance_pubmed_query(llm, user_query):
    enhance_prompt = PromptTemplate(
        input_variables=["query"],
        template="""Create a focused PubMed search query using simplified MeSH terms for the following topic. Prioritize recent research outcomes and clinical studies:

        Topic: {query}

        PubMed query:"""
    )
    enhance_chain = LLMChain(llm=llm, prompt=enhance_prompt)
    return enhance_chain.run(user_query).strip()

def enhance_scholar_query(llm, user_query):
    enhance_prompt = PromptTemplate(
        input_variables=["query"],
        template="Create a focused Google Scholar search query for recent medical research on: {query}\n\nScholar query:"
    )
    enhance_chain = LLMChain(llm=llm, prompt=enhance_prompt)
    return enhance_chain.run(user_query).strip()

def fetch_articles(pubmed_query, scholar_query, max_results=30):
    pubmed_fetch = PubMedFetcher()
    articles = []
    
    try:
        pmids = pubmed_fetch.pmids_for_query(pubmed_query, retmax=max_results // 2)
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_pmid = {executor.submit(fetch_pubmed_abstract, pubmed_fetch, pmid): pmid for pmid in pmids}
            for future in concurrent.futures.as_completed(future_to_pmid):
                article = future.result()
                if article:
                    articles.append(article)

        search_query = scholarly.search_pubs(scholar_query)
        for _ in range(max_results // 2):
            try:
                article = next(search_query)
                scholar_article = fetch_scholar_article(article)
                if scholar_article:
                    articles.append(scholar_article)
            except StopIteration:
                break

        return articles
    except Exception as e:
        st.error(f"An error occurred while fetching articles: {e}")
        return []

def setup_rag(vector_store, llm):
    prompt_template = """Provide a concise, technical response based on the given context from recent medical research articles. Focus on key findings, methodologies, and clinical implications. Use medical terminology appropriate for communication between doctors.

    Context:
    {context}

    Question: {question}
    Answer:"""
    
    PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(),
        chain_type_kwargs={"prompt": PROMPT}
    )

# [Previous imports and functions remain the same]

def generate_overview(qa, query):
    overview_prompt = f"""Provide a concise summary of the latest research findings on {query}. Format the response as follows:

    1. Present 3-5 key points.
    2. Each point should be a single, concise sentence.
    3. Include a citation after each point in parentheses (Author et al., Year).
    4. Start each point with a bullet point (•).
    5. Ensure each point is on a separate line.
    6. Focus on key discoveries, emerging trends, and potential clinical implications.

    Example format:
    • Key point 1. (Author1 et al., Year)
    • Key point 2. (Author2 et al., Year)
    • Key point 3. (Author3 et al., Year)

    Summary:"""
    
    return qa.invoke(overview_prompt)['result']

def main():
    st.set_page_config(page_title="Medical Research Assistant", page_icon="🧬", layout="wide")
    st.title("Medical Research Assistant")

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'qa' not in st.session_state:
        st.session_state.qa = None
    if 'llm' not in st.session_state:
        st.session_state.llm = setup_llm()
    if 'articles' not in st.session_state:
        st.session_state.articles = []
    if 'enhanced_queries' not in st.session_state:
        st.session_state.enhanced_queries = {}

    with st.sidebar:
        st.header("Explore New Research")
        user_query = st.text_input("Enter a medical research topic:")
        if st.button("Investigate Topic"):
            if user_query:
                with st.spinner("Processing..."):
                    enhanced_pubmed_query = enhance_pubmed_query(st.session_state.llm, user_query)
                    enhanced_scholar_query = enhance_scholar_query(st.session_state.llm, user_query)
                    st.session_state.enhanced_queries = {
                        "PubMed": enhanced_pubmed_query,
                        "Google Scholar": enhanced_scholar_query
                    }
                    
                    st.session_state.articles = fetch_articles(enhanced_pubmed_query, enhanced_scholar_query)
                    if st.session_state.articles:
                        vector_store = create_vector_store(st.session_state.articles)
                        st.session_state.qa = setup_rag(vector_store, st.session_state.llm)
                        overview = generate_overview(st.session_state.qa, user_query)
                        st.session_state.chat_history = [("assistant", overview)]
                    else:
                        st.error("No relevant research found.")
            else:
                st.warning("Please enter a research topic.")

        if st.session_state.enhanced_queries:
            st.subheader("Search Queries")
            for source, query in st.session_state.enhanced_queries.items():
                st.write(f"**{source}:** {query}")

        if st.session_state.articles:
            st.subheader("All Citations")
            for article in st.session_state.articles:
                st.write(f"- {article['citation']}")

    # Main content area
    if st.session_state.chat_history:
        st.subheader("Research Summary")
        overview = st.session_state.chat_history[0][1]
        # Split the overview into lines and display each line separately
        for line in overview.split('\n'):
            if line.strip():  # Check if the line is not empty
                st.markdown(line.strip())
        st.markdown("---")  # Add a separator after the overview

    for role, message in st.session_state.chat_history[1:]:  # Skip the overview in chat history
        with st.chat_message(role):
            st.write(message)

    if prompt := st.chat_input("Ask a specific question about the research:"):
        if st.session_state.qa:
            st.session_state.chat_history.append(("human", prompt))
            with st.chat_message("human"):
                st.write(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Analyzing..."):
                    response = st.session_state.qa.invoke(prompt)
                    st.write(response['result'])
                    st.session_state.chat_history.append(("assistant", response['result']))
        else:
            st.info("Please start by entering a research topic in the sidebar.")

if __name__ == "__main__":
    main()