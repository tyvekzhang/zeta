import akshare as ak
import pandas as pd
from datetime import datetime
import time

def get_all_profit_statements():
    """
    获取从1993年至今的所有季度的资产负债表数据
    """
    all_data = pd.DataFrame()
    
    # 从1993年第一季度开始到现在
    start_year = 1993
    current_year = datetime.now().year
    current_quarter = (datetime.now().month - 1) // 3 + 1
    
    for year in range(start_year, current_year + 1):
        # 确定每年的季度数
        if year == current_year:
            quarters = range(1, current_quarter + 1)
        else:
            quarters = [1, 2, 3, 4]
        
        for quarter in quarters:
            # 构造日期参数
            date_str = f"{year}0331" if quarter == 1 else \
                      f"{year}0630" if quarter == 2 else \
                      f"{year}0930" if quarter == 3 else \
                      f"{year}1231"
            
            try:
                print(f"正在获取 {year}年Q{quarter} 的数据...")
                
                # 获取该季度的资产负债表数据
                quarter_data = ak.stock_zcfz_bj_em(date=date_str)
                
                # 添加报告期标识
                quarter_data['年份'] = year
                quarter_data['季度'] = quarter
                
                # 合并数据
                all_data = pd.concat([all_data, quarter_data], ignore_index=True)
                
                # 添加延迟，避免请求过于频繁
                time.sleep(0.5)
                
            except Exception as e:
                print(f"获取 {year}年Q{quarter} 数据失败: {e}")
                continue
    
    return all_data

# 获取所有数据
print("开始获取资产负债表数据...")
all_profit_data = get_all_profit_statements()

# 保存到Excel
output_path = r"C:\Users\Zeke\Desktop\北交所_资产负债表_1993至今.xlsx"
all_profit_data.to_excel(output_path, index=False)

print(f"数据获取完成！共获取 {len(all_profit_data)} 条记录")
print(f"数据已保存到: {output_path}")

# 显示数据基本信息
print("\n数据概览:")
print(f"时间范围: {all_profit_data['报告期'].min()} 到 {all_profit_data['报告期'].max()}")
print(f"公司数量: {all_profit_data['股票代码'].nunique()}")