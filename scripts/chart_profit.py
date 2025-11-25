import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.ticker import FuncFormatter

# 设置中文字体和样式
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.style.use('seaborn-v0_8')

def load_and_preprocess_data(file_path):
    """
    加载和预处理数据
    """
    try:
        # 读取Excel文件
        df = pd.read_excel(file_path)
        print("数据加载成功！")
        print(f"数据形状: {df.shape}")
        print(f"列名: {df.columns.tolist()}")
        
        # 显示前几行数据
        print("\n前5行数据:")
        print(df.head())
        
        # 筛选贵州茅台的数据
        maotai_df = df[df['股票简称'] == '贵州茅台'].copy()
        print(f"\n贵州茅台数据条数: {len(maotai_df)}")
        
        if len(maotai_df) == 0:
            print("未找到贵州茅台数据，请检查股票简称")
            return None
        
        # 确保年份列存在且为数值型
        if '年份' not in maotai_df.columns:
            print("未找到'年份'列，尝试从报告期提取...")
            maotai_df['年份'] = pd.to_datetime(maotai_df['报告期']).dt.year
        
        # 转换数值列
        numeric_columns = ['净利润', '营业总收入', '营业总支出-营业支出', 
                          '营业总支出-销售费用', '营业总支出-管理费用', 
                          '营业总支出-财务费用', '营业利润', '利润总额',
                          '净利润同比', '营业总收入同比']
        
        for col in numeric_columns:
            if col in maotai_df.columns:
                maotai_df[col] = pd.to_numeric(maotai_df[col], errors='coerce')
        
        # 按年份排序
        maotai_df = maotai_df.sort_values('年份')
        
        # 获取近10年数据
        recent_years = maotai_df['年份'].unique()
        if len(recent_years) > 10:
            recent_10_years = sorted(recent_years)[-10:]
            maotai_df = maotai_df[maotai_df['年份'].isin(recent_10_years)]
        
        print(f"\n近10年数据年份: {sorted(maotai_df['年份'].unique())}")
        
        return maotai_df
    
    except Exception as e:
        print(f"数据加载错误: {e}")
        return None

def calculate_financial_ratios(df):
    """
    计算财务比率
    """
    df_ratios = df.copy()
    
    # 计算关键财务比率
    df_ratios['毛利率'] = (df_ratios['营业总收入'] - df_ratios['营业总支出-营业支出']) / df_ratios['营业总收入'] * 100
    df_ratios['营业利润率'] = df_ratios['营业利润'] / df_ratios['营业总收入'] * 100
    df_ratios['净利率'] = df_ratios['净利润'] / df_ratios['营业总收入'] * 100
    
    # 计算费用率（注意财务费用可能为负）
    df_ratios['费用率'] = (df_ratios['营业总支出-销售费用'].fillna(0) + 
                          df_ratios['营业总支出-管理费用'].fillna(0) + 
                          df_ratios['营业总支出-财务费用'].fillna(0)) / df_ratios['营业总收入'] * 100
    
    # 计算销售费用率、管理费用率、财务费用率
    df_ratios['销售费用率'] = df_ratios['营业总支出-销售费用'] / df_ratios['营业总收入'] * 100
    df_ratios['管理费用率'] = df_ratios['营业总支出-管理费用'] / df_ratios['营业总收入'] * 100
    df_ratios['财务费用率'] = df_ratios['营业总支出-财务费用'] / df_ratios['营业总收入'] * 100
    
    return df_ratios

def plot_revenue_profit_trend(df):
    """
    绘制营业收入和利润趋势图
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # 营业收入趋势
    years = df['年份']
    ax1.plot(years, df['营业总收入'] / 1e8, marker='o', linewidth=3, 
             markersize=8, color='#2E86AB', label='营业收入')
    ax1.set_title('贵州茅台营业收入趋势(近10年)', fontsize=16, fontweight='bold', pad=20)
    ax1.set_ylabel('营业收入(亿元)', fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=12)
    
    # 添加数据标签
    for i, (year, revenue) in enumerate(zip(years, df['营业总收入'] / 1e8)):
        ax1.annotate(f'{revenue:.1f}', (year, revenue), 
                    xytext=(0, 10), textcoords='offset points', 
                    ha='center', fontsize=9)
    
    # 利润趋势
    ax2.plot(years, df['营业利润'] / 1e8, marker='s', linewidth=3, 
             markersize=8, color='#A23B72', label='营业利润')
    ax2.plot(years, df['净利润'] / 1e8, marker='^', linewidth=3, 
             markersize=8, color='#F18F01', label='净利润')
    ax2.set_title('贵州茅台利润趋势(近10年)', fontsize=16, fontweight='bold', pad=20)
    ax2.set_ylabel('利润金额(亿元)', fontsize=12)
    ax2.set_xlabel('年份', fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.legend(fontsize=12)
    
    # 添加数据标签
    for i, (year, profit) in enumerate(zip(years, df['营业利润'] / 1e8)):
        if i % 2 == 0:  # 避免标签重叠
            ax2.annotate(f'{profit:.1f}', (year, profit), 
                        xytext=(0, 10), textcoords='offset points', 
                        ha='center', fontsize=9, color='#A23B72')
    
    for i, (year, net_profit) in enumerate(zip(years, df['净利润'] / 1e8)):
        if i % 2 == 1:  # 交错显示
            ax2.annotate(f'{net_profit:.1f}', (year, net_profit), 
                        xytext=(0, -15), textcoords='offset points', 
                        ha='center', fontsize=9, color='#F18F01')
    
    plt.tight_layout()
    return fig

def plot_profitability_ratios(df):
    """
    绘制盈利能力比率图
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    years = df['年份']
    
    # 主要利润率指标
    ax1.plot(years, df['毛利率'], marker='o', linewidth=3, label='毛利率', color='#1f77b4')
    ax1.plot(years, df['营业利润率'], marker='s', linewidth=3, label='营业利润率', color='#ff7f0e')
    ax1.plot(years, df['净利率'], marker='^', linewidth=3, label='净利率', color='#2ca02c')
    ax1.set_title('主要利润率指标趋势(%)', fontsize=14, fontweight='bold')
    ax1.set_ylabel('比率(%)', fontsize=12)
    ax1.set_xlabel('年份', fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # 添加数据标签
    for ratio in ['毛利率', '营业利润率', '净利率']:
        for i, (year, value) in enumerate(zip(years, df[ratio])):
            if i == len(years) - 1:  # 只显示最后一年标签避免重叠
                ax1.annotate(f'{value:.1f}%', (year, value), 
                           xytext=(5, 5), textcoords='offset points', 
                           fontsize=8)
    
    # 费用率分析
    ax2.bar(years, df['销售费用率'], label='销售费用率', alpha=0.8, color='#d62728')
    ax2.bar(years, df['管理费用率'], bottom=df['销售费用率'], label='管理费用率', alpha=0.8, color='#9467bd')
    ax2.bar(years, df['财务费用率'], 
            bottom=df['销售费用率'] + df['管理费用率'], 
            label='财务费用率', alpha=0.8, color='#8c564b')
    
    ax2.set_title('费用率结构分析(%)', fontsize=14, fontweight='bold')
    ax2.set_ylabel('费用率(%)', fontsize=12)
    ax2.set_xlabel('年份', fontsize=12)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

def plot_growth_analysis(df):
    """
    绘制增长分析图
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    years = df['年份']
    
    # 同比增长率
    ax1.plot(years, df['营业总收入同比'], marker='o', linewidth=3, 
             label='营业收入同比', color='#1f77b4', markersize=8)
    ax1.plot(years, df['净利润同比'], marker='s', linewidth=3, 
             label='净利润同比', color='#ff7f0e', markersize=8)
    ax1.axhline(y=0, color='red', linestyle='--', alpha=0.5)
    ax1.set_title('营业收入与净利润同比增长率(%)', fontsize=14, fontweight='bold')
    ax1.set_ylabel('同比增长率(%)', fontsize=12)
    ax1.set_xlabel('年份', fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # 添加数据标签
    for i, (year, growth) in enumerate(zip(years, df['营业总收入同比'])):
        ax1.annotate(f'{growth:.1f}%', (year, growth), 
                    xytext=(0, 10), textcoords='offset points', 
                    ha='center', fontsize=9)
    
    for i, (year, growth) in enumerate(zip(years, df['净利润同比'])):
        ax1.annotate(f'{growth:.1f}%', (year, growth), 
                    xytext=(0, -15), textcoords='offset points', 
                    ha='center', fontsize=9)
    
    # 利润率与增长关系
    scatter = ax2.scatter(df['营业总收入同比'], df['净利润同比'], 
                         c=df['毛利率'], s=df['营业总收入']/1e8, 
                         alpha=0.7, cmap='viridis')
    
    ax2.set_xlabel('营业收入同比增长率(%)', fontsize=12)
    ax2.set_ylabel('净利润同比增长率(%)', fontsize=12)
    ax2.set_title('增长质量分析(气泡大小=营收规模)', fontsize=14, fontweight='bold')
    ax2.axhline(y=0, color='red', linestyle='--', alpha=0.5)
    ax2.axvline(x=0, color='red', linestyle='--', alpha=0.5)
    ax2.grid(True, alpha=0.3)
    
    # 添加颜色条
    cbar = plt.colorbar(scatter, ax=ax2)
    cbar.set_label('毛利率(%)', rotation=270, labelpad=15)
    
    # 添加年份标注
    for i, year in enumerate(years):
        ax2.annotate(str(year), (df['营业总收入同比'].iloc[i], df['净利润同比'].iloc[i]),
                    xytext=(5, 5), textcoords='offset points', fontsize=8)
    
    plt.tight_layout()
    return fig

def plot_expense_analysis(df):
    """
    绘制费用分析图
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    years = df['年份']
    
    # 费用绝对值趋势
    ax1.plot(years, df['营业总支出-销售费用'] / 1e8, marker='o', 
             linewidth=3, label='销售费用', color='#d62728')
    ax1.plot(years, df['营业总支出-管理费用'] / 1e8, marker='s', 
             linewidth=3, label='管理费用', color='#9467bd')
    ax1.plot(years, df['营业总支出-财务费用'] / 1e8, marker='^', 
             linewidth=3, label='财务费用', color='#8c564b')
    
    ax1.set_title('各项费用变化趋势(亿元)', fontsize=14, fontweight='bold')
    ax1.set_ylabel('费用金额(亿元)', fontsize=12)
    ax1.set_xlabel('年份', fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # 费用结构饼图（最新年份）
    latest_year = df.iloc[-1]
    expenses = [
        latest_year['营业总支出-销售费用'],
        latest_year['营业总支出-管理费用'],
        max(latest_year['营业总支出-财务费用'], 0)  # 财务费用可能为负
    ]
    labels = ['销售费用', '管理费用', '财务费用']
    colors = ['#d62728', '#9467bd', '#8c564b']
    
    # 过滤掉为0的费用
    non_zero_expenses = []
    non_zero_labels = []
    non_zero_colors = []
    for i, expense in enumerate(expenses):
        if expense > 0:
            non_zero_expenses.append(expense)
            non_zero_labels.append(labels[i])
            non_zero_colors.append(colors[i])
    
    ax2.pie(non_zero_expenses, labels=non_zero_labels, colors=non_zero_colors, 
            autopct='%1.1f%%', startangle=90)
    ax2.set_title(f'{latest_year["年份"]}年费用结构分布', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    return fig

def create_summary_dashboard(df):
    """
    创建综合仪表板
    """
    # 计算关键指标的最新变化
    latest = df.iloc[-1]
    prev_year = df.iloc[-2] if len(df) > 1 else latest
    
    summary_data = {
        '指标': ['营业收入', '净利润', '毛利率', '营业利润率', '净利率'],
        f'{latest["年份"]}值': [
            f'{latest["营业总收入"]/1e8:.1f}亿元',
            f'{latest["净利润"]/1e8:.1f}亿元',
            f'{latest["毛利率"]:.1f}%',
            f'{latest["营业利润率"]:.1f}%',
            f'{latest["净利率"]:.1f}%'
        ],
        '同比增长': [
            f'{latest["营业总收入同比"]:.1f}%',
            f'{latest["净利润同比"]:.1f}%',
            f'{latest["毛利率"] - prev_year["毛利率"]:.1f}个百分点',
            f'{latest["营业利润率"] - prev_year["营业利润率"]:.1f}个百分点',
            f'{latest["净利率"] - prev_year["净利率"]:.1f}个百分点'
        ]
    }
    
    summary_df = pd.DataFrame(summary_data)
    
    fig, ax = plt.subplots(figsize=(12, 3))
    ax.axis('tight')
    ax.axis('off')
    
    table = ax.table(cellText=summary_df.values,
                    colLabels=summary_df.columns,
                    cellLoc='center',
                    loc='center',
                    bbox=[0, 0, 1, 1])
    
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 2)
    
    ax.set_title('贵州茅台财务表现摘要', fontsize=16, fontweight='bold', pad=20)
    
    return fig

def main():
    """
    主函数
    """
    file_path = r"C:\Users\Zeke\Desktop\jinkuang\利润表_1993至今.xlsx"
    
    # 加载数据
    df = load_and_preprocess_data(file_path)
    if df is None:
        print("数据加载失败，请检查文件路径和数据格式")
        return
    
    # 计算财务比率
    df_ratios = calculate_financial_ratios(df)
    
    print("\n计算后的财务比率数据:")
    print(df_ratios[['年份', '毛利率', '营业利润率', '净利率', '费用率']].tail(10))
    
    # 创建所有图表
    print("\n生成可视化图表...")
    
    # 营业收入和利润趋势
    fig1 = plot_revenue_profit_trend(df_ratios)
    fig1.savefig('贵州茅台_收入利润趋势.png', dpi=300, bbox_inches='tight')
    
    # 盈利能力比率
    fig2 = plot_profitability_ratios(df_ratios)
    fig2.savefig('贵州茅台_盈利能力比率.png', dpi=300, bbox_inches='tight')
    
    # 增长分析
    fig3 = plot_growth_analysis(df_ratios)
    fig3.savefig('贵州茅台_增长分析.png', dpi=300, bbox_inches='tight')
    
    # 费用分析
    fig4 = plot_expense_analysis(df_ratios)
    fig4.savefig('贵州茅台_费用分析.png', dpi=300, bbox_inches='tight')
    
    # 综合仪表板
    fig5 = create_summary_dashboard(df_ratios)
    fig5.savefig('贵州茅台_财务摘要.png', dpi=300, bbox_inches='tight')
    
    # 显示图表
    plt.show()
    
    print("\n可视化分析完成！所有图表已保存为PNG文件")
    
    # 输出关键洞察
    print("\n=== 关键财务洞察 ===")
    latest = df_ratios.iloc[-1]
    print(f"最新年份({latest['年份']})财务表现:")
    print(f"- 营业收入: {latest['营业总收入']/1e8:.1f}亿元")
    print(f"- 毛利率: {latest['毛利率']:.1f}%")
    print(f"- 营业利润率: {latest['营业利润率']:.1f}%")
    print(f"- 净利润同比增长: {latest['净利润同比']:.1f}%")

if __name__ == "__main__":
    main()