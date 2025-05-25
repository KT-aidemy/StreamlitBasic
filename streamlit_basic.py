import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

st.set_page_config(page_title="CSV可視化アプリ", layout="wide")
st.title("CSVファイルアップロードと可視化アプリ")

# CSVファイルアップロード
uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type=["csv"])

if uploaded_file is not None:
    # データ読み込み
    df = pd.read_csv(uploaded_file)
    st.subheader("アップロードされたデータプレビュー")
    st.dataframe(df)

    # 可視化手法選択
    chart_type = st.selectbox(
        "可視化手法を選択してください",
        [
            "折れ線グラフ (時系列)",
            "棒グラフ (カテゴリ比較)",
            "散布図 (2変数の関係)",
            "ヒストグラム (分布)",
            "相関行列ヒートマップ"
        ]
    )

    # 可視化の実行
    if chart_type == "折れ線グラフ (時系列)":
        date_col = st.selectbox("日付列を選択", df.columns)
        value_cols = st.multiselect("表示する値の列を選択", df.columns)
        if date_col and value_cols:
            df[date_col] = pd.to_datetime(df[date_col])
            df_sorted = df.sort_values(date_col)
            st.line_chart(df_sorted.set_index(date_col)[value_cols])

    elif chart_type == "棒グラフ (カテゴリ比較)":
        cat_col = st.selectbox("カテゴリ列を選択", df.columns)
        num_col = st.selectbox("数値列を選択", df.select_dtypes(include=["number"]).columns)
        if cat_col and num_col:
            agg = df.groupby(cat_col)[num_col].sum()
            st.bar_chart(agg)

    elif chart_type == "散布図 (2変数の関係)":
        x_col, y_col = st.selectbox("X軸", df.columns), st.selectbox("Y軸", df.columns)
        if x_col and y_col:
            chart = alt.Chart(df).mark_circle().encode(
                x=x_col, y=y_col, tooltip=list(df.columns)
            ).interactive()
            st.altair_chart(chart, use_container_width=True)

    elif chart_type == "ヒストグラム (分布)":
        num_col = st.selectbox("数値列を選択", df.select_dtypes(include=["number"]).columns)
        bins = st.slider("ビン数", min_value=5, max_value=50, value=20)
        if num_col:
            hist = pd.cut(df[num_col], bins=bins)
            freq = hist.value_counts().sort_index()
            st.bar_chart(freq)

    elif chart_type == "相関行列ヒートマップ":
        corr = df.corr()
        fig = px.imshow(
            corr,
            text_auto=True,
            aspect="auto",
            labels=dict(x="変数", y="変数", color="相関係数")
        )
        st.plotly_chart(fig, use_container_width=True)

else:
    st.info("左側のアップローダーから CSV ファイルを選択してください。")
