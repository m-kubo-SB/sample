import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import japanize_matplotlib

st.title("販売チャネル別　営業利益シュミレーションサンプル！")
#日本語フォント設定
plt.rcParams['font.family'] = 'MS Gothic'

# -----------------------------
# サイドバーでパラメータ設定
# -----------------------------
st.sidebar.header("パラメータ設定")
# イーチケ
r_eticket = st.sidebar.number_input("イーチケ手数料率", value=0.05, step=0.01, format="%.2f")  # 手数料率 5%
PG_eticket = st.sidebar.number_input("PG固定費(円)/月", value=1_500_000, step=10_000)  # PG固定費 150万円
SB_eticket = st.sidebar.number_input("SB固定費(円)/月", value=6_500_000, step=10_000) #SB固定費　4人月（PM0.5削減、0.2は統合PFのため除外）
F_eticket = (PG_eticket + SB_eticket) * 12

# other
r_A1 = st.sidebar.number_input("直販手数料率", value=0.15, step=0.01, format="%.2f")  # 手数料率直販
r_A2 = st.sidebar.number_input("外販手数料率", value=0.08, step=0.01, format="%.2f")    # 手数料率外販
r_tyokuhan = st.sidebar.slider("売上比率（直販を指定）", 0.00, 1.00, 0.60)
#r_tyokuhan, r_gaihan = 0.6, 0.4  # 直販：外販　売上比率
F_A_month  = st.sidebar.number_input("外部固定費(円)/月", value=500_000, step=10_000)  # 固定費 50万円
F_A = F_A_month * 12

# 実効手数料率
r_A_eff =r_tyokuhan * r_A1 + (1-r_tyokuhan) * r_A2

# 売上レンジ
S = np.linspace(20_000_000,1_500_000_000, 400)  # 2000万~10億円まで200点

# -----------------------------
# 利益計算関数
# -----------------------------
def profit(S, r, F):
    return S * (1 - r) - F

# -----------------------------
# 軸のフォーマットをM円表記にする
# -----------------------------
def yen_in_millions(x, pos):
    return f"{x/1_000_000:.1f}"

formatter = FuncFormatter(yen_in_millions)
# -----------------------------
# 計算
# -----------------------------
profit_eticket = profit(S, r_eticket, F_eticket)
profit_A   = profit(S, r_A_eff, F_A)

# -----------------------------
# 可視化
# -----------------------------
fig, ax= plt.subplots(figsize=(10,6))
ax.plot(S, profit_eticket, label="公式サイト", linewidth=2)
ax.plot(S, profit_A, label="other", linestyle="--", linewidth=2)

ax.axhline(0, color="black", linewidth=0.8)  # 利益ゼロライン
ax.set_xlabel("売上 (M円)")
ax.set_ylabel("営業利益 (M円)")
ax.set_title("販売チャネル別 営業利益シミュレーション（年間）")
ax.legend()
ax.grid(True)
# 軸のフォーマット適用
###ax = plt.gca()
ax.xaxis.set_major_formatter(formatter)
ax.yaxis.set_major_formatter(formatter)

st.pyplot(fig)

# -----------------------------
# 公式サイトと外部サイトの利益が等しくなる交点
# -----------------------------
if r_A_eff != r_eticket:  # 手数料率が同じでなければ計算可能
    cross_S = (F_A - F_eticket) / ( r_eticket -r_A_eff)

    if cross_S > 0:
        ax.axvline(cross_S, color="green", linestyle=":", 
                   label=f"利益逆転点 {cross_S/1_000_000:.1f}M円")

        st.markdown(f"""
        ### 利益逆転点
        - 売上が **約 {cross_S/1_000_000:.1f} M円** を超えると、イーチケの利益が外部を上回ります。
        """)
    else:
        st.markdown("### 利益逆転点\n- この条件ではイーチケが外部を上回ることはありません。")
else:
    st.markdown("### 利益逆転点\n- 手数料率が同じなので交点は存在しません。")

st.write({
    "外部固定費": F_A,
    "イーチケ固定費" : F_eticket,
    "外部実質手数料率" : r_A_eff,
    "イーチケ手数料率" : r_eticket


})

