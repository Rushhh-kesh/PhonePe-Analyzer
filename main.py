import streamlit as st
import pandas as pd
from auth import login, logout
from transaction_analyzer import TransactionAnalyzer
from chart_creator import create_charts
import tempfile
import os

def main_app():
    st.title("📊 Transaction Analyzer")
    st.write("Upload your PDF statement to analyze transactions")

    col1, col2, col3 = st.columns(3)
    selected_language = 'en'
    if col1.button('English'):
        selected_language = 'en'
    elif col2.button('हिन्दी'):
        selected_language = 'hi'
    elif col3.button('मराठी'):
        selected_language = 'mr'

    uploaded_file = st.file_uploader("Choose a PDF file", type=['pdf'])
    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(uploaded_file.read())
            pdf_path = tmp_file.name

        analyzer = TransactionAnalyzer(pdf_path, language=selected_language)
        if not analyzer.transactions:
            st.warning("No transactions were extracted. Please check the PDF format.")
            return

        tab1, tab2, tab3 = st.tabs(["📈 Overview", "💰 Transactions", "📊 Charts"])

        with tab1:
            st.metric("Total Spending", f"{analyzer.get_total_spending():,.2f}")
            st.metric("Total Income", f"{analyzer.get_total_income():,.2f}")
            st.metric("Net Balance", f"{analyzer.get_balance():,.2f}")

        with tab2:
            transactions_df = pd.DataFrame([{
                'Date': t['date'].strftime('%Y-%m-%d') if t['date'] else "Invalid Date",
                'Description': t['description'],
                'Type': t['type'],
                'Amount': f"{t['amount']:,.2f}"
            } for t in analyzer.transactions])
            st.dataframe(transactions_df, use_container_width=True)

            # Convert to CSV
            csv = transactions_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Transactions as CSV",
                data=csv,
                file_name="transactions.csv",
                mime="text/csv"
            )

            # Convert to TXT
            txt = transactions_df.to_string(index=False)
            st.download_button(
                label="Download Transactions as TXT",
                data=txt,
                file_name="transactions.txt",
                mime="text/plain"
            )

        with tab3:
            fig_daily, fig_categories, fig_merchants, fig_pie = create_charts(analyzer)
            st.plotly_chart(fig_daily, use_container_width=True)
            st.plotly_chart(fig_categories, use_container_width=True)
            st.plotly_chart(fig_merchants, use_container_width=True)
            st.plotly_chart(fig_pie, use_container_width=True)

        os.unlink(pdf_path)

def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['username'] = ""

    if not st.session_state['logged_in']:
        login()
    else:
        st.sidebar.title("Menu")
        st.sidebar.write(f"Logged in as: {st.session_state['username']}")
        if st.sidebar.button("Logout"):
            logout()
        else:
            main_app()

if __name__ == "__main__":
    main()
