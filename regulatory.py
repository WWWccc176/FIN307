import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from matplotlib.lines import Line2D
import seaborn as sns

# 1. 文件名与标签
files = {
    "Bitcoin": "Bitcoin_2023_2_1-2024_1_31_historical_data_coinmarketcap.csv",
    "Ethereum": "Ethereum_2023_2_1-2024_1_31_historical_data_coinmarketcap.csv",
    "PAXGold": "PAX Gold_2023_2_1-2024_1_31_historical_data_coinmarketcap.csv",
}

# 2. 读入并预处理
dfs = {}
for label, fn in files.items():
    df = pd.read_csv(fn, sep=";")
    df["timeOpen"] = pd.to_datetime(df["timeOpen"])
    df["close"] = (
        df["close"].astype(str).str.replace(r"[\$,]", "", regex=True).astype(float)
    )
    dfs[label] = df

# 3. 基准日期与偏移
base_dates = [
    datetime(2023, 4, 20),
    datetime(2023, 6, 5),
    datetime(2024, 1, 10),
]
offsets = [7, 14]  # 只画 ±7 天和 ±14 天
colors = ["red", "green"]  # 红 = ±7 天，绿 = ±14 天

plt.figure(figsize=(15, 8)) # 稍微调整尺寸以适应更多内容

# 定义每条线的颜色以便区分
line_colors = {
    "Bitcoin": "orange",
    "Ethereum": "dodgerblue",
    "PAXGold": "seagreen"
}

# 4. 循环绘制所有资产的折线图
for label, df in dfs.items():
    plt.plot(df['timeOpen'], df['close'], lw=2, label=label, color=line_colors[label])

# 5. 【核心修改】将Y轴设置为对数坐标
plt.yscale('log')

# 6. 绘制事件窗口的虚线 (保持不变)
for d, col in zip(offsets, colors):
    for base in base_dates:
        for sign in (-1, +1):
            x = base + timedelta(days=sign * d)
            plt.axvline(x, color=col, linestyle="--", alpha=0.7)

# 7. 创建图例
# 主图例 (资产)
leg1 = plt.legend(loc='upper left', title='Assets')
plt.gca().add_artist(leg1)

# 辅助图例 (事件窗口)
offset_handles = [Line2D([0], [0], color=col, linestyle="--", lw=1) for col in colors]
offset_labels = [f"±{d} days" for d in offsets]
leg2 = plt.legend(offset_handles, offset_labels, loc='upper right', title='Event Windows')

# 8. 美化与保存
plt.title('Historical Close Prices of Major Assets (Logarithmic Scale)')
plt.xlabel('Date')
plt.ylabel('Price (USD) - Log Scale')
# 为对数坐标添加更清晰的网格线

plt.tight_layout()
plt.savefig('Crypto_Prices_Log_Scale_Combined.png', dpi=300, bbox_inches='tight')

# 显示图表
plt.show()

df_pair = dfs["Bitcoin"][["timeOpen","close"]].rename(columns={"close":"Bitcoin"})
for label in ["Ethereum","PAXGold"]:
    tmp = dfs[label][["timeOpen","close"]].rename(columns={"close":label})
    df_pair = df_pair.merge(tmp, on="timeOpen", how="inner")

# 9.2 去掉 timeOpen，只保留数值列
df_pair = df_pair.drop(columns="timeOpen")

# 9.3 调用 pairplot
sns.set(style="whitegrid")
pp = sns.pairplot(df_pair,
                  kind="scatter",
                  diag_kind="hist",
                  plot_kws={"alpha": 0.6, "s": 20},
                  diag_kws={"color": "gray"},
                  corner=False)  # corner=True 只画半边矩阵也可以

# 9.4 保存并显示
pp.fig.suptitle("Pairwise Scatter & Marginal Histograms of Close Prices", y=1.02)
pp.fig.tight_layout()
pp.fig.savefig("Regu_Close_Pairplot.png", dpi=300, bbox_inches="tight")
plt.show()