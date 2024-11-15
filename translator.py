# translator.py
def translate(text, language):
    translations = {
        'Daily Spending Trend': {'en': 'Daily Spending Trend', 'hi': 'दैनिक खर्च प्रवृत्ति', 'mr': 'दैनंदिन खर्च प्रवृत्ती'},
        'Amount': {'en': 'Amount', 'hi': 'राशि', 'mr': 'रक्कम'},
        'Date': {'en': 'Date', 'hi': 'तारीख', 'mr': 'तारीख'},
        'Merchant': {'en': 'Merchant', 'hi': 'व्यापारी', 'mr': 'व्यापारी'},
        'Top 10 Merchants by Spending': {'en': 'Top 10 Merchants by Spending', 'hi': 'खर्च के अनुसार शीर्ष 10 व्यापारी', 'mr': 'खर्चानुसार शीर्ष १० व्यापारी'},
        'Transaction Distribution': {'en': 'Transaction Distribution', 'hi': 'लेनदेन वितरण', 'mr': 'व्यवहार वितरण'},
        'Total Spending': {'en': 'Total Spending', 'hi': 'कुल खर्च', 'mr': 'एकूण खर्च'},
        'Total Income': {'en': 'Total Income', 'hi': 'कुल आय', 'mr': 'एकूण उत्पन्न'},
        'Net Balance': {'en': 'Net Balance', 'hi': 'कुल शेष', 'mr': 'निव्वळ शिल्लक'},
        'Analysis Period': {'en': 'Analysis Period', 'hi': 'विश्लेषण अवधि', 'mr': 'विश्लेषण कालावधी'}
    }
    return translations.get(text, {}).get(language, text)
