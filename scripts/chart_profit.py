import matplotlib.pyplot as plt
import numpy as np

# 1. 解决中文乱码问题
# 注意：在某些环境中，可能需要安装SimHei字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Heiti TC', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 2. 实际计算数据
years = np.array([2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024])

# 营业收入 (亿元) - 左侧Y轴，柱状图
income = np.array([
    334.47, 401.55, 610.63, 771.99, 888.54, 979.93, 1094.64, 1275.54, 1505.60, 1741.44
])

# 净利润 (亿元) - 左侧Y轴，柱状图 (修改为柱状图)
net_profit = np.array([
    155.03, 167.18, 270.79, 352.04, 412.06, 466.97, 524.60, 627.17, 747.34, 862.28
])

# 费率/利润率 (%) - 右侧Y轴 (使用百分比)
expense_rate = np.array([
    16, 15, 13, 10, 11, 10, 10, 10, 10, 9
])

gross_profit_rate = np.array([
    92.41, 91.50, 90.27, 91.55, 91.64, 91.68, 91.79, 92.09, 92.12, 92.08
])

operating_profit_rate = np.array([
    66, 60, 63, 66, 66, 68, 68, 69, 69, 69
])

# 3. 创建图表和双Y轴
fig, ax1 = plt.subplots(figsize=(12, 7))

# 设置标题
plt.title('2015—2024年贵州茅台营业收入、净利润及利润率趋势', fontsize=16)

# --- 绘制主Y轴 (左侧) 数据 (营业收入和净利润) ---

# 定义柱子宽度
bar_width = 0.4

# 柱状图 (营业收入) - 放在左侧
bar_color_income = '#60a5fa' # 蓝色
bar_income = ax1.bar(years - bar_width/2, income, color=bar_color_income, label='营业收入', width=bar_width)

# 柱状图 (净利润) - 放在右侧，与营业收入并排
bar_color_profit = '#ef4444' # 红色
bar_profit = ax1.bar(years + bar_width/2, net_profit, color=bar_color_profit, label='净利润', width=bar_width)


ax1.set_ylabel('亿元', color='black', fontsize=12)
ax1.tick_params(axis='y', labelcolor='black', labelsize=10)

# 设置左侧Y轴刻度 (根据最大值调整)
max_value = max(income.max(), net_profit.max())
ax1.set_ylim(0, np.ceil(max_value / 200) * 200) # 刻度间隔设为200亿元
ax1.set_yticks(np.arange(0, np.ceil(max_value / 200) * 200 + 1, 200))


# 设置X轴刻度
ax1.set_xticks(years)
ax1.set_xticklabels(years, rotation=45, fontsize=10) # 倾斜45度，更易读

# --- 绘制次Y轴 (右侧) 数据 (费率/利润率) ---
ax2 = ax1.twinx()

ax2.set_ylabel('%', color='black', fontsize=12, rotation=0, ha='left', va='center')
ax2.tick_params(axis='y', labelcolor='black', labelsize=10)
ax2.set_ylim(0, 100)
ax2.set_yticks(np.arange(0, 101, 10))
ax2.set_yticklabels([f'{i:.0f}' for i in np.arange(0, 101, 10)])

# 定义颜色
area_color_1 = '#1f2937' # 费用率 (面积图颜色)
line_color_2 = '#20B2AA' # 毛利率
line_color_3 = '#1f2937' # 营业利润率

# 费用率 - 使用面积图表示
ax2.fill_between(years, expense_rate, 0, color=area_color_1, alpha=0.3, label='费用率 (面积)')

# 毛利率 - 绘制折线
line2, = ax2.plot(years, gross_profit_rate, color=line_color_2, linestyle='-', marker='o', markersize=6, label='毛利率', linewidth=2)
# 营业利润率 - 绘制折线
line3, = ax2.plot(years, operating_profit_rate, color=line_color_3, linestyle='--', marker='^', markersize=6, label='营业利润率', linewidth=1.5)

# --- 添加图例 ---

# 营业收入的图例句柄
bar_legend_handle_income = plt.Line2D([0], [0], marker='s', color='w', markerfacecolor=bar_color_income, markersize=10, label='营业收入')
# 净利润的图例句柄 (更新为柱状图样式)
bar_legend_handle_profit = plt.Line2D([0], [0], marker='s', color='w', markerfacecolor=bar_color_profit, markersize=10, alpha=0.8,label='净利润')
# 费用率的图例句柄：使用一个填充的矩形来表示面积
area_legend_handle = plt.Rectangle((0, 0), 1, 1, fc=area_color_1, alpha=0.9, label='费用率')

legend_handles = [
    bar_legend_handle_income, # 营业收入
    bar_legend_handle_profit, # 净利润 (更新)
    area_legend_handle, # 费用率
    line2,        # 毛利率
    line3        # 营业利润率
]
legend_labels = ['营业收入', '净利润', '费用率', '毛利率', '营业利润率']

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