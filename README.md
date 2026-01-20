# 📊 Financial Data Analyst Agent (RAG-Pandas)

**A production-grade Agentic RAG Chatbot designed for complex quantitative analysis on financial datasets.**

![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B)
![LangChain](https://img.shields.io/badge/Orchestration-LangChain-1C3C3C)
![Gemini](https://img.shields.io/badge/Model-Gemini%202.5%20Flash-4285F4)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB)

## Overview

This project implements a sophisticated Financial Data Analyst Agent capable of performing mathematical reasoning and data aggregation over structured financial data. Unlike traditional RAG (Retrieval-Augmented Generation) systems that rely on vector similarity—often struggling with quantitative tasks—this bot utilizes a LangChain Pandas Agent powered by Google's Gemini 2.5 Flash.

The agent functions as an intelligent reasoning engine: it interprets natural language queries, generates executable Python code to aggregate, filter, and analyze data across multiple DataFrames (Holdings and Trades), and delivers precise, data-backed answers.

## Key Features

*   **Agentic Workflow (ReAct):** Uses a "Reason-Act-Observe" loop to write and execute real Python code for calculations (Sum, Count, Mean, GroupBy), ensuring 100% mathematical accuracy.
*   **Multi-DataFrame Reasoning:** Intelligently routes queries to the correct dataset—analyzing `Holdings` for performance/P&L and `Trades` for transaction history.
*   **Strict Hallucination Guardrails:** Engineered with a custom prompt framework to enforce strict compliance. If data is missing or calculation is impossible, it defaults to a standardized fallback ("Sorry can not find the answer") rather than fabricating results.
*   **Production-Ready UI:** Built with Streamlit, featuring session state management for conversational context, data caching (`@st.cache_data`) for high performance, and robust error handling.
*   **Powered by Gemini 2.5 Flash:** Leverages the latest efficient vision-language model for high-speed reasoning at low latency.

## Tech Stack

*   **Frontend:** [Streamlit](https://streamlit.io/)
*   **LLM Orchestration:** [LangChain](https://www.langchain.com/) (Experimental Pandas Agent)
*   **Model Provider:** [Google Generative AI](https://ai.google.dev/) (`gemini-2.5-flash`)
*   **Data Processing:** [Pandas](https://pandas.pydata.org/)
*   **Environment:** Python 3.10+

## Project Structure

```bash
├── app.py                # Main application entry point (Streamlit UI & Agent Logic)
├── holdings.csv          # Dataset 1: Portfolio holdings and P&L data
├── trades.csv            # Dataset 2: Historical trade transactions
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

## Getting Started:

### Prerequisites

*   Python 3.10 or higher
*   A Google Cloud API Key (available detailed [here](https://aistudio.google.com/app/api-keys))

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/financial-analyst-agent.git
    cd financial-analyst-agent
    ```

2.  **Create a virtual environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    streamlit run app.py
    ```

## Usage Examples

Once the app is running, try asking questions that require data aggregation:

### 1. Complex Aggregation
> *"Which funds performed better depending on the yearly Profit and Loss?"*
*   **Logic:** The agent groups by `PortfolioName`, sums `PL_YTD` (Year-to-Date Profit/Loss), and sorts the results.

### 2. Counting & Filtering
> *"What is the total number of holdings for the 'Garfield' portfolio?"*
*   **Logic:** The agent filters the `Holdings` dataframe for 'Garfield' and counts the rows.

### 3. Cross-Validation
> *"Show me the top 3 trades by quantity."*
*   **Logic:** The agent queries the `Trades` dataframe and sorts by the `Quantity` column.

### 4. Guardrail Test
> *"What is the capital of France?"*
*   **Result:** *"Sorry can not find the answer"* (Correctly identifies the question is outside the dataset scope).

## How It Works?

1.  **User Input:** The user asks a question in natural language via the Streamlit chat interface.
2.  **LLM Reasoning:** The Gemini model analyzes the prompt and the schema of the loaded CSV files (`holdings.csv` and `trades.csv`).
3.  **Code Generation:** The model generates a snippet of Python pandas code to answer the question (e.g., `df_holdings.groupby('PortfolioName')['PL_YTD'].sum()`).
4.  **Execution:** The LangChain agent executes this code safely in a local Python sandbox.
5.  **Response:** The result of the code execution is fed back to the LLM, which formulates a concise natural language response for the user.

## License

Distributed under the MIT License. See `LICENSE` for more information.
