import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from matplotlib.lines import Line2D
import seaborn as sns

# 1. 文件名与标签（改成你新截屏里的那三个文件）
files = {
    "Bitcoin":    "Bitcoin_2025_1_1-2025_10_26_historical_data_coinmarketcap.csv",
    "Ethereum":   "Ethereum_2025_1_1-2025_10_26_historical_data_coinmarketcap.csv",
    
}

# 2. 读入并预处理
dfs = {}
for label, fn in files.items():
    df = pd.read_csv(fn, sep=";")
    df["timeOpen"] = pd.to_datetime(df["timeOpen"])
    # 清洗 close 列并转成 float
    df["close"] = (
        df["close"].astype(str)
                 .str.replace(r"[\$,]", "", regex=True)
                 .astype(float)
    )
    dfs[label] = df

# 3. 基准日期和偏移（可根据你需要再调整）
base_dates = [
    datetime(2025, 5, 31),
    datetime(2025, 10, 10),
]
offsets = [7, 14]
offset_colors = ["red", "green"]

# 4. 开一张对数折线图
plt.figure(figsize=(14, 7))

# 4.1 各资产绘制对数折线
line_colors = {"Bitcoin":"orange", "Ethereum":"dodgerblue", "Ethena_USDe":"seagreen"}
for label, df in dfs.items():
    plt.plot(df["timeOpen"], df["close"],
             lw=2, label=label, color=line_colors[label])
plt.yscale("log")

# 4.2 在每个基准日 ±7/14 天画虚线
for d, c in zip(offsets, offset_colors):
    for bd in base_dates:
        for s in (-1, 1):
            plt.axvline(bd + timedelta(days=s*d),
                        color=c, linestyle="--", alpha=0.7)

# 5. 图例：左资产，右偏移说明
leg1 = plt.legend(loc="upper left", title="Assets")
offset_handles = [Line2D([0],[0], color=c, linestyle="--") for c in offset_colors]
offset_labels  = [f"±{d} days" for d in offsets]
leg2 = plt.legend(offset_handles, offset_labels,
                  loc="upper right", title="Event Windows")
plt.gca().add_artist(leg1)

# 6. 美化与保存
plt.title("Counterparty Risk: Historical Close Prices (Log Scale)")
plt.xlabel("Date")
plt.ylabel("Close Price (USD, log scale)")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("CounterpartyRisk_Close_Log.png", dpi=300, bbox_inches="tight")
plt.show()

# 7. —— seaborn pairplot 散点图矩阵 —— 

# 7.1 合并三个资产的 close 数据，以 timeOpen 对齐
df_pair = dfs["Bitcoin"][["timeOpen","close"]].rename(columns={"close":"Bitcoin"})
for lbl in ["Ethereum"]:
    tmp = dfs[lbl][["timeOpen","close"]].rename(columns={"close":lbl})
    df_pair = df_pair.merge(tmp, on="timeOpen", how="inner")

# 7.2 丢弃 timeOpen，只保留数值列
df_pair = df_pair.drop(columns="timeOpen")

# 7.3 画 pairplot
sns.set(style="whitegrid")
pp = sns.pairplot(df_pair,
                  kind="scatter",
                  diag_kind="hist",
                  plot_kws={"alpha":0.6, "s":20},
                  diag_kws={"color":"gray"})

# 7.4 保存并展示
pp.fig.suptitle("Pairwise Scatter & Marginal Histograms of Close Prices", y=1.02)
pp.fig.tight_layout()
pp.fig.savefig("CounterpartyRisk_Close_Pairplot.png", dpi=300, bbox_inches="tight")
plt.show()