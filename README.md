# Smart AI Agent — GPT-4o Powered Conversational Assistant with Multi-View & PDF Export

Welcome to **Smart AI Agent**, a powerful web-based AI assistant that combines OpenAI's GPT-4o with live web search (via SerpAPI) to provide detailed, bullet-point, and full-description answers on demand. Plus, export any response as a professional PDF!

---

## 🚀 Features

- **Multi-View Responses**: Choose how you want to see answers — brief detail, bullet points, or full description.
- **Real-Time Web Search**: Stay updated with answers powered by live internet search using SerpAPI.
- **PDF Export**: Download any response format as a well-formatted PDF report.
- **Image Generation**: Generate creative images from text prompts with OpenAI’s DALL·E 3.
- **Conversation Memory**: Retain chat history for context-aware interactions.
- **User-Friendly Interface**: Streamlit app with clean, interactive UI.

---

## 🛠️ Technologies Used

- Python 3.13+
- [OpenAI GPT-4o](https://openai.com/)
- [LangChain](https://python.langchain.com/)
- [SerpAPI](https://serpapi.com/)
- [Streamlit](https://streamlit.io/)
- [FPDF](https://pyfpdf.github.io/fpdf2/)
- python-dotenv for environment variable management

---

## 📥 Getting Started

### Prerequisites

- Python 3.13 or newer
- OpenAI API key
- SerpAPI key

### Installation Steps

1.Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

2.Install dependencies
python-dotenv
openai
langchain
langchain-community
langchain-openai
streamlit
brave-search-sdk
PyPDF2
fpdf2
pip install -r requirements.txt

3.Create a .env file in the root folder and add your API keys
OPENAI_API_KEY=your_openai_api_key_here
SERPAPI_API_KEY=your_serpapi_api_key_here

4.Run the app
streamlit run app.py

6.Open your browser at
http://localhost:8501

