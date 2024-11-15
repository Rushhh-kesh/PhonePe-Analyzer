# transaction_analyzer.py
import pdfplumber
from datetime import datetime
import streamlit as st

class TransactionAnalyzer:
    def __init__(self, pdf_path: str, language: str = 'en'):
        self.transactions = self._parse_transactions(pdf_path)
        self.language = language

    def _parse_date(self, date_str: str) -> datetime:
        try:
            date_str = date_str.strip()
            return datetime.strptime(date_str, '%b %d, %Y')  # Adjust format as needed
        except ValueError:
            st.warning(f"Warning: Unable to parse date '{date_str}'.")
            return None

    def _parse_transactions(self, pdf_path: str) -> list:
        transactions = []
        with pdfplumber.open(pdf_path) as pdf:
            for page_number, page in enumerate(pdf.pages):
                text = page.extract_text()
                if not text:
                    st.warning(f"Warning: Page {page_number + 1} is empty.")
                    continue
                
                for line in text.split('\n'):
                    try:
                        date_str = line[:12].strip()
                        amount_index = line.rfind('₹')
                        if amount_index == -1:
                            continue
                        amount_str = line[amount_index + 1:].strip().replace(',', '')
                        description = line[12:amount_index].strip()
                        transaction_type = 'CREDIT' if 'CREDIT' in line.upper() else 'DEBIT'
                        amount = float(amount_str)
                        date = self._parse_date(date_str)
                        if date:
                            transactions.append({
                                'date': date,
                                'description': description,
                                'type': transaction_type,
                                'amount': amount
                            })
                    except Exception:
                        st.warning(f"Failed to process line '{line}' on page {page_number + 1}.")
                        continue
        return sorted(transactions, key=lambda x: x['date'], reverse=True) if transactions else []

    def get_total_spending(self):
        return sum(t['amount'] for t in self.transactions if t['type'] == 'DEBIT')

    def get_total_income(self):
        return sum(t['amount'] for t in self.transactions if t['type'] == 'CREDIT')

    def get_balance(self):
        return self.get_total_income() - self.get_total_spending()

    def get_merchant_analysis(self) -> list:
        from collections import defaultdict
        merchant_spending = defaultdict(float)
        for t in self.transactions:
            if t['type'] == 'DEBIT':
                merchant_spending[t['description']] += t['amount']
        return sorted(merchant_spending.items(), key=lambda x: x[1], reverse=True)
