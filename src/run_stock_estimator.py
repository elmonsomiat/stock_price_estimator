import yfinance as yf
import os
from src.finance_utils import get_stock_symbol, get_long_financials
from src.agent_utils import load_model
from src.utils import create_pdf_from_dict
def get_report(stock, model, financials_api_key):
    stock_symbol = get_stock_symbol(stock)
    print(stock_symbol)
    stock = yf.Ticker(stock_symbol)

    # Get industry and market cap
    industry = stock.info.get("industry", "N/A")
    market_cap = stock.info.get("marketCap", "N/A")
    eps = stock.info.get("trailingEps", "N/A")
    roe = stock.info.get("returnOnEquity", "N/A")
    pe_ratio = stock.info.get("trailingPE", "N/A")

    income_statement_report, balanced_sheet_report, cash_flow_report =  get_long_financials(stock_symbol, model, financials_api_key)

    ans = model.invoke(f'''Estimate a price range for this stock based on the following information:
                 - Industry: {industry}
                 - Market cap: {market_cap}
                 - Earnings per share: {eps}
                 - ROE: {roe}
                 - P/E Ratio: {pe_ratio}
                 - Income statement: {balanced_sheet_report}
                 - Balanced sheet: {balanced_sheet_report}
                 - Cash flow: {cash_flow_report}
                 
                 You must give a range where you think the stock price should be based on the above information
                 ''')

    return ans.content

if __name__=='__main__':
    FINANCIALS_API_KEY = os.getenv('FINANCIALS_API_KEY')
    MODEL = load_model()
    stock_list = ['Novo Nordisk', "Tesla", 'Cloudflare']
    output = {}
    for STOCK_NAME in stock_list:

        output[STOCK_NAME] = get_report(STOCK_NAME, MODEL, FINANCIALS_API_KEY)
    create_pdf_from_dict(output, f'/home/ana/Desktop/stock_output.pdf')

