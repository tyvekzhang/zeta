import akshare as ak

stock_lrb_em_df = ak.stock_lrb_em(date="19940930")
stock_lrb_em_df.to_excel(r"C:\Users\Zeke\Desktop\利润表_19940930.xlsx")
