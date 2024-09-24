# MedResearchAI

## Description
MedResearchAI is a Streamlit-based application that leverages the power of PubMed and Google Scholar to provide up-to-date summaries and insights on medical research topics. It uses natural language processing and retrieval-augmented generation (RAG) to analyze recent research papers and present key findings.

## Features
- Query enhancement for both PubMed and Google Scholar searches
- Retrieval of recent research articles from both sources
- Generation of concise research summaries with citations
- Interactive Q&A based on the retrieved research
- Display of full citations for all referenced articles

## Query Enhancement Process

MedResearchAI uses advanced query enhancement techniques to improve the relevance and comprehensiveness of search results from both PubMed and Google Scholar.

### PubMed Query Enhancement

For PubMed searches, we leverage the Medical Subject Headings (MeSH) system to create more effective queries:

1. **MeSH Term Identification**: The user's initial query is analyzed to identify relevant MeSH terms. This process uses the hierarchical structure of MeSH to find both broad and specific terms related to the query.

2. **Query Expansion**: The identified MeSH terms are added to the original query using appropriate PubMed search tags. For example:
   - Original query: "diabetes treatment"
   - Enhanced query: "diabetes treatment[Title/Abstract] OR Diabetes Mellitus/therapy[MeSH]"

3. **Recency Focus**: To prioritize recent research, we may add date restrictions to the query, such as:
   - Enhanced query: "(diabetes treatment[Title/Abstract] OR Diabetes Mellitus/therapy[MeSH]) AND ("last 5 years"[PDat])"

4. **Field-Specific Searches**: We may also include specific field searches to target titles, abstracts, or other relevant fields:
   - Example: "(diabetes[Title] AND (treatment[Title] OR therapy[Title]))"

This process helps ensure that the PubMed search captures relevant articles using standardized medical terminology while focusing on recent and pertinent research.

### Google Scholar Query Enhancement

For Google Scholar, which doesn't use a standardized vocabulary like MeSH, we employ different techniques to enhance the query:

1. **Keyword Expansion**: We analyze the user's query to identify key medical concepts and expand them with relevant synonyms or related terms.

2. **Phrase Formulation**: We may reformulate the query into specific phrases that are likely to appear in scholarly articles.

3. **Publication Type Targeting**: We might add terms to target specific types of publications, such as "clinical trial", "systematic review", or "meta-analysis".

4. **Date Restrictions**: Similar to PubMed, we may add date restrictions to focus on recent research.

5. **Domain-Specific Terms**: We may include domain-specific terminology that's commonly used in scholarly medical literature.

Example:
- Original query: "new diabetes treatments"
- Enhanced query: "novel diabetes therapies OR innovative glucose management clinical trials 2019..2024"

This enhancement process for Google Scholar aims to broaden the search to capture relevant articles while maintaining specificity to the medical domain and recency of the research.

By using these query enhancement techniques, MedResearchAI strives to provide comprehensive and relevant results from both PubMed and Google Scholar, offering users a well-rounded view of the current research landscape on their topic of interest.

## Requirements
- Python 3.7+
- AWS account with access to Amazon Bedrock
- NCBI API key (optional, but recommended for better PubMed access)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/MedResearchAI.git
   cd MedResearchAI
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up your AWS credentials for Bedrock access. You can do this by configuring the AWS CLI or setting environment variables.

5. (Optional) Set your NCBI API key as an environment variable:
   ```
   export NCBI_API_KEY=your_api_key_here
   ```

## Usage

1. Run the Streamlit app:
   ```
   streamlit run medical_research_assistant.py
   ```

2. Open your web browser and go to the URL provided by Streamlit (usually http://localhost:8501).

3. Enter a medical research topic in the sidebar and click "Investigate Topic".

4. Review the research summary and citations provided.

5. Ask specific questions about the research in the chat input at the bottom of the page.

## Community Contributions

We welcome and encourage contributions from the community! Whether you're a medical professional, a developer, or an enthusiast, your input can help improve MedResearchAI. Here are some ways you can contribute:

- **Enhance the implementation**: If you have ideas for improving the code, optimizing performance, or adding new features, please feel free to submit a pull request.
- **Expand the knowledge base**: Suggestions for better query formulation or improvements to the summarization process are always appreciated.
- **Improve user experience**: If you have ideas for making the interface more intuitive or accessible, we'd love to hear them.
- **Documentation**: Help us improve our documentation, add examples, or create tutorials to make MedResearchAI more accessible to others.
- **Bug reports and feature requests**: If you encounter any issues or have ideas for new features, please open an issue on our GitHub repository.

To contribute:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

We strive to create a welcoming and inclusive community. Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before contributing.

## Note
This application uses AI models and web scraping techniques. Please be mindful of usage limits and terms of service for PubMed, Google Scholar, and Amazon Bedrock.

## License
[MIT License](LICENSE)
