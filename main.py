# app.py
import streamlit as st
import os
from dotenv import load_dotenv
from fpdf import FPDF
import base64

# Load environment variables
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent, tool
from langchain import hub
from langchain_community.utilities import SerpAPIWrapper
from langchain_community.tools import Tool

# --- API Keys ---
openai_api_key = os.getenv("OPENAI_API_KEY")
serpapi_api_key = os.getenv("SERPAPI_API_KEY")

if not openai_api_key or not serpapi_api_key:
    st.error("Missing OPENAI_API_KEY or SERPAPI_API_KEY in .env.")
    st.stop()

# --- LLM Setup ---
llm = ChatOpenAI(model="gpt-4o", temperature=0.7, openai_api_key=openai_api_key)

# --- Tools ---
serpapi_wrapper = SerpAPIWrapper(serpapi_api_key=serpapi_api_key)
search_tool = Tool(
    name="Web Search",
    description="Search current events or detailed info from the web.",
    func=serpapi_wrapper.run
)

@tool
def generate_image(prompt: str) -> str:
    """Generate image using OpenAI's DALL·E 3."""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=openai_api_key)
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        return f"🖼️ **Image generated:** [Click to view]({image_url})"
    except Exception as e:
        return f"❌ Error generating image: {e}"

tools = [search_tool, generate_image]

# --- Agent Setup ---
prompt = hub.pull("hwchase17/react")
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

# --- Streamlit UI ---
st.set_page_config(page_title="Smart AI Agent", page_icon="🤖", layout="centered")
st.title("🤖 Smart AI Agent with Multi-View PDF Export")

st.markdown("Ask your question below and view the result in different styles. You can download any format as PDF.")

# Chat history memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    elif msg["role"] == "agent":
        st.markdown(f"**Agent:** {msg['content']}")

# Input box
user_input = st.text_input("💬 Ask me something smart:", key="input", placeholder="e.g. Future of AI in healthcare")

if user_input:
    with st.spinner("Thinking..."):
        try:
            # Run base agent response
            base_prompt = f"Please answer this in a helpful and elaborate way:\n{user_input}"
            result = agent_executor.invoke({"input": base_prompt})
            full_response = result["output"]

            # Save conversation
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.session_state.messages.append({"role": "agent", "content": full_response})

            # Generate 3 versions
            detailed = llm.predict(f"Give a brief summary in 2–3 lines for: {full_response}")
            bullets = llm.predict(f"Convert this into bullet points only:\n{full_response}")
            full_description = full_response

            # PDF creation function
            def create_pdf(text: str) -> bytes:
                pdf = FPDF()
                pdf.add_page()
                pdf.set_auto_page_break(auto=True, margin=15)
                pdf.set_font("Arial", size=12)
                for line in text.split('\n'):
                    pdf.multi_cell(w=190, h=10, txt=line)
                return bytes(pdf.output(dest="S"))

            # --- Collapsible views ---
            with st.expander("🔍 View in Detail (Short Summary)"):
                st.write(detailed)
                pdf = create_pdf(detailed)
                b64_pdf = base64.b64encode(pdf).decode()
                st.markdown(f'<a href="data:application/pdf;base64,{b64_pdf}" download="response_detail.pdf">💾 Download as PDF</a>', unsafe_allow_html=True)

            with st.expander("📌 View in Bullet Points"):
                st.write(bullets)
                pdf = create_pdf(bullets)
                b64_pdf = base64.b64encode(pdf).decode()
                st.markdown(f'<a href="data:application/pdf;base64,{b64_pdf}" download="response_bullets.pdf">💾 Download as PDF</a>', unsafe_allow_html=True)

            with st.expander("📘 View in Full Description"):
                st.write(full_description)
                pdf = create_pdf(full_description)
                b64_pdf = base64.b64encode(pdf).decode()
                st.markdown(f'<a href="data:application/pdf;base64,{b64_pdf}" download="response_full_description.pdf">💾 Download as PDF</a>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ Error: {e}")
