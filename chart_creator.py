import plotly.graph_objects as go
import pandas as pd

def create_charts(analyzer):
    df = pd.DataFrame([{
        'date': t['date'].strftime('%Y-%m-%d') if t['date'] else "Invalid Date",
        'amount': t['amount'],
        'type': t['type'],
        'description': t['description']
    } for t in analyzer.transactions])
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Daily Spending Trend
    fig_daily = go.Figure()
    fig_daily.add_trace(go.Scatter(x=df[df['type'] == 'DEBIT']['date'], y=df[df['type'] == 'DEBIT']['amount'], mode='lines', name='Daily Spending'))
    fig_daily.update_layout(
        title="Daily Spending Trend",
        xaxis_title="Date",
        yaxis_title="Amount",
        xaxis_tickformat='%b %d',
        plot_bgcolor='white',
        font=dict(
            family="Roboto, sans-serif",
            size=14,
            color="black"
        )
    )

    # Transaction Category Bar Chart
    category_spending = df.groupby('type')['amount'].sum().reset_index()
    fig_categories = go.Figure()
    fig_categories.add_trace(go.Bar(x=category_spending['type'], y=category_spending['amount'], marker_color=['#4c78a8', '#e45756']))
    fig_categories.update_layout(
        title="Transaction Category Breakdown",
        xaxis_title="Transaction Type",
        yaxis_title="Total Amount",
        plot_bgcolor='white',
        font=dict(
            family="Roboto, sans-serif",
            size=14,
            color="black"
        )
    )

    # Top Merchants by Spending
    merchant_data = pd.DataFrame(analyzer.get_merchant_analysis(), columns=['Merchant', 'Amount'])
    fig_merchants = go.Figure()
    fig_merchants.add_trace(go.Bar(x=merchant_data['Merchant'].head(10), y=merchant_data['Amount'].head(10), marker_color='#6d904f'))
    fig_merchants.update_layout(
        title="Top 10 Merchants by Spending",
        xaxis_title="Merchant",
        yaxis_title="Amount",
        xaxis_tickangle=-45,
        plot_bgcolor='white',
        font=dict(
            family="Roboto, sans-serif",
            size=14,
            color="black"
        )
    )

    # Transaction Distribution Pie Chart
    fig_pie = go.Figure()
    fig_pie.add_trace(go.Pie(labels=df['type'].unique(), values=df.groupby('type')['amount'].sum(), hole=0.6))
    fig_pie.update_layout(
        title="Transaction Distribution",
        plot_bgcolor='white',
        font=dict(
            family="Roboto, sans-serif",
            size=14,
            color="black"
        )
    )

    return fig_daily, fig_categories, fig_merchants, fig_pie