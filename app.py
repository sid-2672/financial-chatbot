import streamlit as st
import pandas as pd
import os
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_google_genai import ChatGoogleGenerativeAI

# 1. Configuration & Setup
#This section sets up the Streamlit app and its title.
st.set_page_config(page_title="Fund Analytics Bot", layout="wide")
st.title("Financial RAG Chatbot")
st.markdown("""
This bot analyzes your **Holdings** and **Trades** using **Gemini 2.5 Flash**. 
Ask questions like:
- *What is the total number of holdings for the 'Garfield' fund?*
- *Which funds performed better based on Yearly P&L?*
""")

# 2. Sidebar - Configuration
# This section creates a sidebar for user inputs and displays loaded data status.
with st.sidebar:
    st.header("Configuration")
    google_api_key = st.text_input("Google API Key", type="password")
    st.markdown("[Get a Google API Key here](https://aistudio.google.com/app/api-keys)")
    st.markdown("---")
    st.markdown("**Data Loaded:**")
    st.text("✅ holdings.csv")
    st.text("✅ trades.csv")
# 3. Data Loading
# This section loads the CSV data into pandas DataFrames.
@st.cache_data
def load_data():
    try:
        holdings_df = pd.read_csv("holdings.csv", low_memory=False)
        trades_df = pd.read_csv("trades.csv", low_memory=False)
        return holdings_df, trades_df
    except FileNotFoundError:
        st.error("CSV files not found. Please ensure 'holdings.csv' and 'trades.csv' are in the directory.")
        return None, None
df_holdings, df_trades = load_data()
# 4. Agent Initialization
# This section defines a function to create the agent with custom instructions.
def get_agent(holdings, trades, key):
    if not key:
        return None
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        google_api_key=key,
        temperature=0,
        convert_system_message_to_human=True
    )
    # Custom Prompt Instructions for your chatbot add more guiderails as needed.
    prefix_prompt = """
    You are a high-level financial analyst. 
    You have access to two pandas dataframes: 
    1. `df1`: **Holdings Data** (Columns: PortfolioName, SecName, PL_YTD, MV_Base, etc.)
    2. `df2`: **Trades Data** (Columns: TradeTypeName, Quantity, Price, TradeDate, etc.)
    
    **GUIDELINES:**
    - If asked about 'funds', 'performance', or 'P&L', query `df1` (Holdings).
    - If asked about 'trades', 'transactions', or 'buy/sell', query `df2` (Trades).
    - You can perform aggregations (Sum, Count, Mean) using pandas code.
    
    **CRITICAL RULE:**
    - If the answer cannot be calculated from the data provided, OR if the data is missing, YOU MUST RESPOND WITH EXACTLY: 
      "Sorry can not find the answer".
    - Do NOT generate fake data. Do NOT search the internet. Do NOT hallucinate.
    - Always ensure your final answer is based solely on the data in the dataframes.
    - If the user greets you (e.g., "hello", "hi"), respond politely but mention you are a financial bot.
    """
    # Create the Agent
    agent = create_pandas_dataframe_agent(
        llm, 
        [holdings, trades], 
        agent_type="zero-shot-react-description",
        verbose=True,
        allow_dangerous_code=True,
        prefix=prefix_prompt,
        agent_executor_kwargs={"handle_parsing_errors": True} 
    )
    return agent
# 5. Chat Interface
# This section manages the chat interface and user interactions.
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I am ready to analyze your data with Gemini."}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
if prompt := st.chat_input("Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    if df_holdings is None or df_trades is None:
        st.error("Data not loaded. Please check CSV files.")
    elif not google_api_key:
        st.warning("Please enter your Google API Key in the sidebar.")
    else:
        with st.chat_message("assistant"):
            with st.spinner("Gemini is thinking..."):
                try:
                    agent = get_agent(df_holdings, df_trades, google_api_key)
                    response = agent.invoke({"input": prompt})
                    answer = response['output']
                    st.write(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                except Exception as e:
                    # Finally the safety net for errors.
                    error_str = str(e)
                    if "404" in error_str and "models/" in error_str:
                        error_msg = f"Error: Perhaps try switching to a different model? "
                    else:
                        error_msg = "Sorry can not find the answer (an error occurred)."
                    
                    st.write(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                    print(f"DEBUG ERROR: {e}")