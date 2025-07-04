import os
import requests
import pandas as pd

from yahooquery import search

def get_stock_symbol(company_name):
    """Search for a stock symbol based on the company name"""
    result = search(company_name)
    quotes = result.get("quotes", [])
    if quotes:
        return quotes[0]["symbol"]
    return None
def get_financials_fmp(ticker, api_key):
    """
    Fetch financial statements (Income Statement, Balance Sheet, Cash Flow) for a company using FinancialModelingPrep API.

    Args:
        ticker (str): Stock ticker symbol (e.g., "AAPL").
        api_key (str): Your API key for FinancialModelingPrep.

    Returns:
        dict: A dictionary containing income statement, balance sheet, and cash flow data as Pandas DataFrames.
    """
    base_url = "https://financialmodelingprep.com/api/v3"

    # Fetch Income Statement
    income_statement = requests.get(f"{base_url}/income-statement/{ticker}?apikey={api_key}").json()

    # Fetch Balance Sheet
    balance_sheet = requests.get(f"{base_url}/balance-sheet-statement/{ticker}?apikey={api_key}").json()

    # Fetch Cash Flow Statement
    cash_flow = requests.get(f"{base_url}/cash-flow-statement/{ticker}?apikey={api_key}").json()

    # Convert to DataFrames
    income_df = pd.DataFrame(income_statement)
    balance_df = pd.DataFrame(balance_sheet)
    cash_flow_df = pd.DataFrame(cash_flow)

    return {
        "Income Statement": income_df,
        "Balance Sheet": balance_df,
        "Cash Flow": cash_flow_df
    }
def get_long_financials(stock_symbol, model, financials_api_key):
    financials = get_financials_fmp(stock_symbol, financials_api_key)
    if len(financials['Income Statement'])>0:
        print('Getting income statement')
        income_cols = ['date', 'reportedCurrency', 'cik', 'fillingDate',
               'acceptedDate', 'calendarYear', 'period', 'revenue', 'costOfRevenue',
               'grossProfit', 'grossProfitRatio', 'researchAndDevelopmentExpenses',
               'generalAndAdministrativeExpenses', 'sellingAndMarketingExpenses',
               'sellingGeneralAndAdministrativeExpenses', 'otherExpenses',
               'operatingExpenses', 'costAndExpenses', 'interestIncome',
               'interestExpense', 'depreciationAndAmortization', 'ebitda',
               'ebitdaratio', 'operatingIncome', 'operatingIncomeRatio',
               'totalOtherIncomeExpensesNet', 'incomeBeforeTax',
               'incomeBeforeTaxRatio', 'incomeTaxExpense', 'netIncome',
               'netIncomeRatio', 'eps', 'epsdiluted', 'weightedAverageShsOut',
               'weightedAverageShsOutDil']
        income_statement = financials["Income Statement"][income_cols].head(4).to_dict(orient='records')

        income_statement_report = model.invoke(f'''Write a full report summarising the income statement based on the following data \
        {str(income_statement)}. Just write a summary of the data, nothing else.
        ''').content

        print('Getting balanced sheet')
        balanced_sheet_cols = ['date','reportedCurrency', 'cik', 'fillingDate',
               'acceptedDate', 'calendarYear', 'period', 'cashAndCashEquivalents',
               'shortTermInvestments', 'cashAndShortTermInvestments', 'netReceivables',
               'inventory', 'otherCurrentAssets', 'totalCurrentAssets',
               'propertyPlantEquipmentNet', 'goodwill', 'intangibleAssets',
               'goodwillAndIntangibleAssets', 'longTermInvestments', 'taxAssets',
               'otherNonCurrentAssets', 'totalNonCurrentAssets', 'otherAssets',
               'totalAssets', 'accountPayables', 'shortTermDebt', 'taxPayables',
               'deferredRevenue', 'otherCurrentLiabilities', 'totalCurrentLiabilities',
               'longTermDebt', 'deferredRevenueNonCurrent',
               'deferredTaxLiabilitiesNonCurrent', 'otherNonCurrentLiabilities',
               'totalNonCurrentLiabilities', 'otherLiabilities',
               'capitalLeaseObligations', 'totalLiabilities', 'preferredStock',
               'commonStock', 'retainedEarnings',
               'accumulatedOtherComprehensiveIncomeLoss',
               'othertotalStockholdersEquity', 'totalStockholdersEquity',
               'totalEquity', 'totalLiabilitiesAndStockholdersEquity',
               'minorityInterest', 'totalLiabilitiesAndTotalEquity',
               'totalInvestments', 'totalDebt', 'netDebt']
        balanced_sheet = financials["Balance Sheet"][balanced_sheet_cols].head(4).to_dict(orient='records')
        balanced_sheet_report = model.invoke(f'''Write a full report summarising the balance sheet based on the following data \
        {str(balanced_sheet)}. Just write a summary of the data, nothing else.
        ''').content

        print('Getting cash flow')
        cash_flow_cols = ['date', 'reportedCurrency', 'cik', 'fillingDate',
               'acceptedDate', 'calendarYear', 'period', 'netIncome',
               'depreciationAndAmortization', 'deferredIncomeTax',
               'stockBasedCompensation', 'changeInWorkingCapital',
               'accountsReceivables', 'inventory', 'accountsPayables',
               'otherWorkingCapital', 'otherNonCashItems',
               'netCashProvidedByOperatingActivities',
               'investmentsInPropertyPlantAndEquipment', 'acquisitionsNet',
               'purchasesOfInvestments', 'salesMaturitiesOfInvestments',
               'otherInvestingActivites', 'netCashUsedForInvestingActivites',
               'debtRepayment', 'commonStockIssued', 'commonStockRepurchased',
               'dividendsPaid', 'otherFinancingActivites',
               'netCashUsedProvidedByFinancingActivities',
               'effectOfForexChangesOnCash', 'netChangeInCash', 'cashAtEndOfPeriod',
               'cashAtBeginningOfPeriod', 'operatingCashFlow', 'capitalExpenditure',
               'freeCashFlow']
        cash_flow = financials["Cash Flow"][cash_flow_cols].head(4).to_dict(orient='records')
        cash_flow_report = model.invoke(f'''Write a full report summarising the cash flow based on the following data \
        {str(cash_flow)}. Just write a summary of the data, nothing else.
        ''').content

        return income_statement_report, balanced_sheet_report, cash_flow_report
    return None, None, None
