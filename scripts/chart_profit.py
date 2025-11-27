import matplotlib.pyplot as plt
import numpy as np

# 1. 解决中文乱码问题
plt.rcParams['font.sans-serif'] = ['SimHei', 'Heiti TC', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 2. 实际计算数据 (基于表格)
years = np.array([2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024])

# 营业收入 (亿元) - 左侧Y轴，将元转换为亿元
income = np.array([
    155.03, 167.18, 270.79, 352.04, 412.06, 466.97, 524.60, 627.17, 747.34, 862.28
])

# 费率/利润率 (%) - 右侧Y轴 (使用百分比)
expense_rate = np.array([
    24.59, 25.05, 17.36, 15.13, 14.97, 14.54, 16.11, 14.37, 13.02, 10.80
])

gross_profit_rate = np.array([
    83.63, 79.60, 78.07, 81.44, 81.93, 82.52, 82.90, 83.90, 84.11, 84.00
])

operating_profit_rate = np.array([
    14.19, 14.33, 14.31, 14.44, 14.27, 14.18, 14.21, 14.00, 13.87, 13.88
])

# 3. 创建图表和双Y轴
fig, ax1 = plt.subplots(figsize=(12, 7))

# 设置标题
plt.title('2015—2024年贵州茅台营业利润率趋势', fontsize=16)

# --- 绘制柱状图 (营业收入) ---
bar_color = '#60a5fa' # 蓝色
ax1.bar(years, income, color=bar_color, label='营业收入', width=0.8)
ax1.set_ylabel('亿元', color='black', fontsize=12)
ax1.tick_params(axis='y', labelcolor='black', labelsize=10)

# 设置左侧Y轴刻度 (根据最大值调整)
max_income = income.max()
ax1.set_ylim(0, np.ceil(max_income / 100) * 100)
ax1.set_yticks(np.arange(0, np.ceil(max_income / 100) * 100 + 1, 100))

# 设置X轴刻度
ax1.set_xticks(years)
ax1.set_xticklabels(years, rotation=45, fontsize=10) # 倾斜45度，更易读

# --- 绘制折线图和面积图 (费率/利润率) ---
ax2 = ax1.twinx()

ax2.set_ylabel('%', color='black', fontsize=12, rotation=0, ha='left', va='center')
ax2.tick_params(axis='y', labelcolor='black', labelsize=10)
ax2.set_ylim(0, 100)
ax2.set_yticks(np.arange(0, 101, 10))
ax2.set_yticklabels([f'{i:.1f}%' for i in np.arange(0, 101, 10)])

# 定义颜色
area_color_1 = '#1f2937' # 费用率 (面积图颜色)
line_color_2 = '#20B2AA' # 毛利率
line_color_3 = '#1f2937' # 营业利润率

# 费用率 - 使用面积图表示
# fill_between(x, y1, y2=0, where=None, **kwargs)
ax2.fill_between(years, expense_rate, 0, color=area_color_1, alpha=0.3, label='费用率 (面积)')

# 毛利率 - 绘制折线
line2, = ax2.plot(years, gross_profit_rate, color=line_color_2, linestyle='-', label='毛利率', linewidth=2.5)
# 营业利润率 - 绘制折线
line3, = ax2.plot(years, operating_profit_rate, color=line_color_3, linestyle='-', marker='o', markersize=6, label='营业利润率', linewidth=1.5)

# --- 添加图例 (修改费用率的图例句柄) ---

# 费用率的图例句柄：使用一个填充的矩形来表示面积
area_legend_handle = plt.Rectangle((0, 0), 1, 1, fc=area_color_1, alpha=0.3, label='费用率')

legend_handles = [
    # 营业收入 (使用方形marker模拟柱状图)
    plt.Line2D([0], [0], marker='s', color='w', markerfacecolor=bar_color, markersize=10, label='营业收入'),
    # 费用率 (使用面积图句柄)
    area_legend_handle, 
    # 毛利率
    line2,
    # 营业利润率
    line3
]
legend_labels = ['营业收入', '费用率', '毛利率', '营业利润率']

# 将图例放置在图的下方中央
ax1.legend(
    handles=legend_handles, 
    labels=legend_labels, 
    loc='upper center', 
    bbox_to_anchor=(0.5, -0.2), 
    ncol=len(legend_handles), 
    fontsize=10,
    frameon=False 
)

# 4. 显示图表
ax1.grid(False)
ax2.grid(False)

# 调整布局以容纳位于下方的图例
plt.tight_layout(rect=[0, 0.1, 1, 1]) 
plt.show()