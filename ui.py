# Streamlit-powered UI for chat and results

"""
Streamlit UI for the Simple AI Agent.
Provides a chat interface that connects to the FastAPI backend.
"""
import os
import requests
import streamlit as st
import json
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
API_HOST = os.environ.get("API_HOST", "localhost")
API_PORT = os.environ.get("API_PORT", "8000")
API_BASE_URL = f"http://{API_HOST}:{API_PORT}"

# Streamlit page configuration
st.set_page_config(
    page_title="Simple AI Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

def check_api_health() -> Dict[str, Any]:
    """Check if the API is running and healthy."""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return {"status": "error", "message": f"API returned status {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": f"Cannot connect to API: {str(e)}"}

def send_message(message: str) -> Dict[str, Any]:
    """Send a message to the agent via API."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/chat",
            json={"message": message},
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API error: {response.status_code} - {response.text}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}

def get_available_tools() -> Dict[str, Any]:
    """Get information about available tools."""
    try:
        response = requests.get(f"{API_BASE_URL}/tools", timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return {"tools": []}
    except requests.exceptions.RequestException:
        return {"tools": []}

# Main UI
def main():
    st.title("🤖 Simple AI Agent")
    st.markdown("A beginner-friendly AI agent that can fetch advice and search books!")

    # Sidebar with API status and tools info
    with st.sidebar:
        st.header("📊 System Status")

        # Check API health
        health = check_api_health()
        if health.get("status") == "ok":
            st.success("✅ API is running")
            st.info(f"Model: {health.get('model', 'Unknown')}")
            if health.get('agent_ready'):
                st.success("✅ Agent is ready")
            else:
                st.error("❌ Agent not ready")
        else:
            st.error("❌ API is not accessible")
            st.error(health.get("message", "Unknown error"))
            st.info("Make sure to run: `python api.py`")

        st.header("🛠️ Available Tools")
        tools_info = get_available_tools()
        for tool in tools_info.get("tools", []):
            with st.expander(tool["name"]):
                st.write(tool["description"])
                if tool["parameters"]:
                    st.write("Parameters:", tool["parameters"])

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            # Show tool usage info for assistant messages
            if message["role"] == "assistant" and "tool_info" in message:
                with st.expander("🔧 Tool Usage Details"):
                    tool_info = message["tool_info"]
                    if tool_info.get("used_tool"):
                        st.write(f"**Tool Used:** {tool_info['used_tool']}")
                        if tool_info.get("tool_result"):
                            st.json(tool_info["tool_result"])
                    else:
                        st.write("No tools were used for this response.")

    # Chat input
    if prompt := st.chat_input("Ask me anything! I can give advice or search for books."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get response from agent
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = send_message(prompt)

                if "error" in response:
                    st.error(f"Error: {response['error']}")
                    assistant_message = "Sorry, I encountered an error processing your request."
                    tool_info = None
                else:
                    assistant_message = response.get("answer", "I couldn't generate a response.")
                    tool_info = {
                        "used_tool": response.get("used_tool"),
                        "tool_result": response.get("tool_result")
                    }

                st.markdown(assistant_message)

                # Show tool usage details
                if tool_info and tool_info.get("used_tool"):
                    with st.expander("🔧 Tool Usage Details"):
                        st.write(f"**Tool Used:** {tool_info['used_tool']}")
                        if tool_info.get("tool_result"):
                            st.json(tool_info["tool_result"])

        # Add assistant response to chat history
        assistant_msg = {"role": "assistant", "content": assistant_message}
        if tool_info:
            assistant_msg["tool_info"] = tool_info
        st.session_state.messages.append(assistant_msg)

    # Clear chat button
    if st.sidebar.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    # Example queries
    st.sidebar.header("💡 Example Queries")
    example_queries = [
        "Give me some advice",
        "Find books about machine learning",
        "Search for books by Agatha Christie",
        "What's a good book recommendation?",
        "I need some motivation"
    ]

    for query in example_queries:
        if st.sidebar.button(query, key=f"example_{query}"):
            # Add to chat input
            st.session_state.messages.append({"role": "user", "content": query})
            st.rerun()

if __name__ == "__main__":
    main()
