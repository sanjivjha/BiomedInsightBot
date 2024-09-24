# MedResearchAI

## Description
MedResearchAI is a Streamlit-based application that leverages the power of PubMed and Google Scholar to provide up-to-date summaries and insights on medical research topics. It uses natural language processing and retrieval-augmented generation (RAG) to analyze recent research papers and present key findings.

## Features
- Query enhancement for both PubMed and Google Scholar searches
- Retrieval of recent research articles from both sources
- Generation of concise research summaries with citations
- Interactive Q&A based on the retrieved research
- Display of full citations for all referenced articles

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
