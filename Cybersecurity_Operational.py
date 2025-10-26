import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from matplotlib.lines import Line2D
import seaborn as sns   # ← 新增这一行

# 1. 文件名映射（按需修改路径）
files = {
    "Bitcoin":   "Bitcoin_2021_7_1-2022_4_30_historical_data_coinmarketcap.csv",
   "Ethereum":  "Ethereum_2021_7_1-2022_4_30_historical_data_coinmarketcap.csv",
    "Solana":    "Solana_2021_7_1-2022_4_30_historical_data_coinmarketcap.csv",
    "Litecoin":  "Litecoin_2021_7_1-2022_4_30_historical_data_coinmarketcap.csv",
}

# 2. 读取并预处理
dfs = {}
for label, fn in files.items():
    df = pd.read_csv(fn, sep=";")
    df["timeOpen"] = pd.to_datetime(df["timeOpen"])
    df["close"] = (
        df["close"].astype(str)
                 .str.replace(r"[\$,]", "", regex=True)
                 .astype(float)
    )
    dfs[label] = df

# 3. 基准日期与偏移量
base_dates    = [ datetime(2022,3,23), datetime(2021,8,10) ]
offsets       = [7, 14]
offset_colors = ["red","green"]

# 4. 绘主图
plt.figure(figsize=(12,6))
for label, df in dfs.items():
    plt.plot(df["timeOpen"], df["close"], lw=1.5, label=label)
plt.yscale("log")
for d, c in zip(offsets, offset_colors):
    for bd in base_dates:
        for s in (-1,1):
            plt.axvline(bd + timedelta(days=s*d), color=c, linestyle="--", alpha=0.7)

leg1 = plt.legend(loc="upper left", title="Cryptocurrencies")
handles = [ Line2D([0],[0], color=c, linestyle="--") for c in offset_colors ]
labels  = [ f"±{d} days" for d in offsets ]
leg2    = plt.legend(handles, labels, loc="upper right", title="Offsets")
plt.gca().add_artist(leg1)

plt.title("Historical Close Prices (log scale) & ±7/14-day Markers")
plt.xlabel("Date")
plt.ylabel("Close Price (USD, log scale)")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("historical_close_log.png", dpi=300, bbox_inches="tight")
plt.show()


# 7. —— 新增：Seaborn pairplot 散点矩阵 —— 

# 7.1 合并所有 close 价格到同一个 DataFrame（以 timeOpen 对齐）
df_pair = dfs["Bitcoin"][["timeOpen","close"]].rename(columns={"close":"Bitcoin"})
for lbl in ["Ethereum","Solana","Litecoin"]:
    tmp = dfs[lbl][["timeOpen","close"]].rename(columns={"close":lbl})
    df_pair = df_pair.merge(tmp, on="timeOpen", how="inner")

# 7.2 丢掉 timeOpen，只保留数值列
df_pair = df_pair.drop(columns="timeOpen")

# 7.3 调用 pairplot
sns.set(style="whitegrid")
pp = sns.pairplot(df_pair,
                  kind="scatter",
                  diag_kind="hist",
                  plot_kws={"alpha":0.6, "s":20},
                  diag_kws={"color":"gray"})

# 7.4 美化、保存并显示
pp.fig.suptitle("Pairwise Scatter & Marginal Histograms of Close Prices", y=1.02)
pp.fig.tight_layout()
pp.fig.savefig("crypto_close_prices_pairplot.png", dpi=300, bbox_inches="tight")
plt.show()