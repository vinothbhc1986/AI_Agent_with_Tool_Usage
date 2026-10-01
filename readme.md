# In this project, our agent can:

**Fetch random advice from a public API.**

**Look up books from Google Books**

**Based on the User's prompt, decides which of the above 2 tools to be used with
the help of LLM reasoning.**

**Executes the appropriate tool (API).**

**Based on the tool's response, generates a friendly response for the user with the
help of LLM**

## So LLM is used at 2 steps here.

**To select the appropriate tool based on user query.**

**To Generate a text response based on the tool's response which will generally be
in JSON format.**

### For Example

***If the user says "I'm feeling depressed and lonely", then the agent will analyse the
user's query and it will decide that it should use the "get_advice" tool to answer this
query.***

***If the user says "Suggest some books to learn LLMs", then the agent will analyse
the user's query and it will decide that it should use the "search_books" tool to
answer this query***

#### Project Overview & Goals

**Who is this for?**

***Beginners in GenAI wanting to understand practical agentic reasoning***

**What does it do?**

***Uses a language model (“agent brain”) to pick between two tools: advice & book
search, then summarizes results for the user.***

**How is it built?**

***Modestly, with FastAPI (backend), Streamlit (UI)***

**Tools (External Capabilities)**

***Functions that extend the agent's capabilities beyond text generation. In this section
we have defined 2 different tools that our agent can use to answer user queries.***

#### Tool 1: get_advice

#### Tool 2: search_books


### Starting the Application

****Open Terminal 1 OR Command Prompt 1 and Start the API Server using the following
command:****

***uvicorn api:app --reload***
***or***
****python api.py***

****Open another Terminal OR Command Prompt and Start the UI Server using the
following command****

***streamlit run ui.py***

***OR**

***To rerun automatically when you save ui.py, start it with:***

***streamlit run ui.py --server.runOnSave true****

****You can now view your Streamlit app in your browser.****


***Type the following prompts in the chat window to test the agent's behaviour***

#### I'm feeling stressed about work. Any advice?

#### Find me books about artificial intelligence





