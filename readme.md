# Get Financials for stocks from Morningstar.com

app uses list of stocks in sp500-symbols-list (contains list of all S&P 500 companies as of 2021-01-26)

- opens the link in firefox
balance sheet, cashflow statement and income statement selected for period 10y
10y is only for premium, so it will wait until you login
and go to the correct page for download again

key ratios are free for 10y (no login needed)

- execute script for export

- saves file in subfolder /download

successfuly downloaded are added to file success.txt
failed are added to error.txt with link and exception message

This is working at Mar 2021
@jakubCF