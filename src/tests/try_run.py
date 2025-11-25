import akshare as ak

stock_xjll_em_df = ak.stock_xjll_em(date="20240331")
stock_xjll_em_df.to_excel(r"C:\Users\Zeke\Desktop\小数据_report_cash_flow.xlsx")