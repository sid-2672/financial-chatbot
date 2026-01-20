https://github.com/user-attachments/assets/eaba25ee-251f-4ffb-a6a4-be724cb96bfc

# Financial Data Analyst Agent

This is a chatbot that actually does math on your financial data. Most chatbots just guess the next word, which is bad for numbers. This one is different—it writes and runs real Python code to give you accurate answers about your portfolio holdings and trades.

![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B)
![LangChain](https://img.shields.io/badge/Orchestration-LangChain-1C3C3C)
![Gemini](https://img.shields.io/badge/Model-Gemini%202.5%20Flash-4285F4)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB)

## What is this?

If you have a bunch of financial data in CSV files (like Holdings and Trades), you usually have to open Excel or write SQL to verify simple things. This project lets you just chat with that data.

It's built with Streamlit (for the website part), LangChain (to manage the logic), and Google Gemini 2.5 Flash (the brain).

## The Code: How it works?

Everythin happens in `app.py`. Here is the breakdown of what the code is actually doing:

1.  **Loading the Data**: First, we read your `holdings.csv` and `trades.csv` into Pandas DataFrames. Think of these as programmable Excel sheets living in the computer's memory.
2.  **Setting up the Agent**: We don't just ask the AI to "guess" the answer. We give it a tool—the ability to run Python code. We treat the dataframes as tools it can use.
3.  **The Reasoning Loop**:
    *   You ask a question: *"What is the total PL Year-to-Date for the Garfield portfolio?"*
    *   The Agent thinks: *"Okay, I need to look at the Holdings dataframe. I should filter for 'Garfield' and then sum up the 'PL_YTD' column."*
    *   **It writes code**: It generates real Python code like `df_holdings[df_holdings['PortfolioName'] == 'Garfield']['PL_YTD'].sum()`.
    *   **It runs the code**: It executes that line securely.
    *   **It gives the answer**: It takes the number it calculated (say, 41054.58) and tells you, *"The total PL YTD for Garfield is 41,054.58."*

This means if the math is wrong, it's because the data is wrong, not because the AI hallucinated a random number.

## The Output

The output you see in the chat window is the final natural language summary. But behind the scenes, the output is strict and data-driven.

*   If you ask for a list, it queries the dataframe and returns the exact rows.
*   If you ask for a sum or average, it performs the mathematical operation on the full dataset.
*   If you ask something out of scope (like "What is the capital of India?"), we have specific instructions in the code to return exactly "Sorry can not find the answer". We don't want it chatting about irrelevant topics.

## Project Structure

*   `app.py`: The brain and the body of the app.
*   `holdings.csv`: Your portfolio snapshots.
*   `trades.csv`: The history of what you bought and sold.
*   `requirements.txt`: The list of libraries needed to make this run.

## Getting Started

You need Python 3.10+ and a [Google API Key](https://aistudio.google.com/app/api-keys).

1.  **Get the code:**
    ```bash
    git clone https://github.com/sid-2672/financial-chatbot
    cd financial-chatbot
    ```

2.  **Set up your environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # or venv\Scripts\activate on Windows
    pip install -r requirements.txt
    ```

3.  **Run it:**
    ```bash
    streamlit run app.py
    ```

## Usage Examples

Here are some real questions you can ask and what happens inside the code:

**"Which funds performed better based on yearly P&L?"**
*   **Code Action:** The agent groups your holdings by 'PortfolioName', sums up the 'PL_YTD' for each, and sorts them to show you the winner.

**"Show me the top 3 trades by quantity."**
*   **Code Action:** It sorting the `trades` dataset by the 'Quantity' column and cuts off the top 3 rows.

**"What's the total cash in the Garfield portfolio?"**
*   **Code Action:** It filters for 'Garfield' and sums the 'MV_Base' (Market Value).

## License

Distributed under the MIT License.
