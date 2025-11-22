import pandas as pd
import akshare as ak
import time
from tqdm import tqdm
import re

def extract_stock_code(symbol):
    """
    从股票代码中提取纯数字部分
    例如: 
    - "SH600938" -> "600938"
    - "SZ000550" -> "000550"
    - "600009" -> "600009" (保持不变)
    """
    # 使用正则表达式提取所有数字
    numbers = re.findall(r'\d+', str(symbol))
    if numbers:
        return numbers[0]  # 返回第一个连续数字序列
    else:
        return str(symbol).strip()  # 如果没有数字，返回原始值

def get_stock_dividend_data():
    """
    读取Excel文件中的股票代码，获取分红数据并保存到Excel
    """
    try:
        # 读取Excel文件中的股票代码
        file_path = r"C:\Users\Zeke\Desktop\stock_history_dividend.xlsx"
        df_symbols = pd.read_excel(file_path)
        
        # 检查是否存在symbol_full字段
        if 'symbol_full' not in df_symbols.columns:
            print("错误：Excel文件中未找到'symbol_full'字段")
            print("可用字段：", df_symbols.columns.tolist())
            return
        
        # 获取股票代码列表并提取数字部分
        symbols = df_symbols['symbol_full'].dropna().unique().tolist()
        print(f"找到 {len(symbols)} 个股票代码")
        
        # 显示一些转换示例
        print("股票代码转换示例:")
        for i in range(min(5, len(symbols))):
            original = symbols[i]
            extracted = extract_stock_code(original)
            print(f"  {original} -> {extracted}")
        
        # 存储所有分红数据的列表
        all_dividend_data = []
        
        # 遍历每个股票代码，获取分红数据
        for i, symbol in enumerate(tqdm(symbols, desc="获取分红数据")):
            try:
                # 提取股票代码的数字部分
                symbol_clean = extract_stock_code(symbol)
                
                # 使用akshare获取分红数据
                dividend_df = ak.stock_dividend_cninfo(symbol=symbol_clean)
                
                if dividend_df is not None and not dividend_df.empty:
                    # 添加原始股票代码和清理后的股票代码
                    dividend_df['symbol_full'] = symbol  # 原始代码
                    dividend_df['symbol_clean'] = symbol_clean  # 清理后的代码
                    
                    # 使用实际的中文列名进行重命名
                    column_mapping = {
                        '实施方案公告日期': 'announcement_date',
                        '分红类型': 'dividend_type',
                        '送股比例': 'bonus_share_ratio',
                        '转增比例': 'conversion_ratio',
                        '派息比例': 'dividend_ratio',
                        '股权登记日': 'registration_date',
                        '除权日': 'ex_rights_date',
                        '派息日': 'payment_date',
                        '股份到账日': 'share_arrival_date',
                        '实施方案分红说明': 'dividend_description',
                        '报告时间': 'report_period'
                    }
                    
                    # 只重命名实际存在的列
                    actual_mapping = {}
                    for cn_col, en_col in column_mapping.items():
                        # 检查列是否存在（处理可能的空格差异）
                        actual_cols = [col for col in dividend_df.columns if col.strip() == cn_col]
                        if actual_cols:
                            actual_mapping[actual_cols[0]] = en_col
                    
                    # 重命名列
                    dividend_df = dividend_df.rename(columns=actual_mapping)
                    
                    # 选择需要的字段
                    required_columns = [
                        'symbol_full', 'symbol_clean', 'announcement_date', 'dividend_type',
                        'bonus_share_ratio', 'conversion_ratio', 'dividend_ratio',
                        'registration_date', 'ex_rights_date', 'payment_date',
                        'share_arrival_date', 'dividend_description', 'report_period'
                    ]
                    
                    # 只保留存在的字段
                    available_columns = [col for col in required_columns if col in dividend_df.columns]
                    dividend_df = dividend_df[available_columns]
                    
                    # 添加到总数据列表
                    all_dividend_data.append(dividend_df)
                    
                    print(f"成功获取 {symbol_clean} 的分红数据，共 {len(dividend_df)} 条记录")
                
                else:
                    print(f"股票 {symbol_clean} 未找到分红数据")
                
                # 添加延迟，避免请求过快
                if (i + 1) % 10 == 0:
                    time.sleep(1)
                    
            except Exception as e:
                print(f"获取股票 {symbol} 的分红数据时出错: {str(e)}")
                continue
        
        # 合并所有数据
        if all_dividend_data:
            final_df = pd.concat(all_dividend_data, ignore_index=True)
            
            # 添加系统字段
            final_df['created_at'] = pd.Timestamp.now()
            final_df['updated_at'] = pd.Timestamp.now()
            
            # 格式化日期字段
            date_columns = ['announcement_date', 'registration_date', 'ex_rights_date', 
                           'payment_date', 'share_arrival_date']
            
            for col in date_columns:
                if col in final_df.columns:
                    final_df[col] = pd.to_datetime(final_df[col], errors='coerce').dt.date
            
            # 保存到Excel文件
            output_file = r"C:\Users\Zeke\Desktop\stock_dividend_results.xlsx"
            final_df.to_excel(output_file, index=False, engine='openpyxl')
            
            print(f"\n数据获取完成！共获取 {len(final_df)} 条分红记录")
            print(f"结果已保存到: {output_file}")
            
            # 显示数据预览
            print("\n数据预览:")
            print(final_df.head())
            print(f"\n数据形状: {final_df.shape}")
            
        else:
            print("未获取到任何分红数据")
            
    except FileNotFoundError:
        print(f"文件未找到: {file_path}")
    except Exception as e:
        print(f"程序执行出错: {str(e)}")

# 简化版本，直接使用数字股票代码
def simple_get_dividend_data():
    """
    简化版本，直接使用数字股票代码
    """
    try:
        # 读取股票代码
        df_symbols = pd.read_excel(r"C:\Users\Zeke\Desktop\stock_history_dividend.xlsx")
        symbols = df_symbols['symbol_full'].dropna().unique()
        print(f"找到 {len(symbols)} 个股票代码")
        
        all_data = []
        
        for i, symbol in enumerate(tqdm(symbols, desc="获取分红数据")):
            try:
                # 提取股票代码的数字部分
                symbol_clean = extract_stock_code(symbol)
                
                # 获取分红数据
                dividend_df = ak.stock_dividend_cninfo(symbol=symbol_clean)
                
                if dividend_df is not None and not dividend_df.empty:
                    # 添加股票代码
                    dividend_df['symbol_full'] = symbol  # 原始代码
                    dividend_df['symbol_clean'] = symbol_clean  # 数字代码
                    all_data.append(dividend_df)
                    
                # 添加延迟
                # if (i + 1) % 10 == 0:
                #     time.sleep(0.1)
                    
            except Exception as e:
                print(f"获取股票 {symbol} 的分红数据时出错: {str(e)}")
                continue
        
        # 合并数据
        if all_data:
            result_df = pd.concat(all_data, ignore_index=True)
            
            # 添加时间戳
            result_df['created_at'] = pd.Timestamp.now()
            result_df['updated_at'] = pd.Timestamp.now()
            
            # 保存结果
            output_file = r"C:\Users\Zeke\Desktop\stock_dividend_all.xlsx"
            result_df.to_excel(output_file, index=False)
            print(f"完成！共获取 {len(result_df)} 条记录")
            print(f"结果已保存到: {output_file}")
            
            # 显示数据信息
            print("\n数据列名:")
            print(result_df.columns.tolist())
            print("\n数据样例:")
            print(result_df.head())
        else:
            print("未获取到任何数据")
            
    except Exception as e:
        print(f"程序执行出错: {str(e)}")

if __name__ == "__main__":
    print("开始获取股票分红数据...")
    
    # 使用简化版本
    simple_get_dividend_data()