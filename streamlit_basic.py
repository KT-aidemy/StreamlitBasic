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
            agg = df.groupby(cat_col)[num_col].sum().reset_index()
            fig = px.bar(agg, x=cat_col, y=num_col, labels={cat_col: "カテゴリ", num_col: "合計"})
            st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "散布図 (2変数の関係)":
        x_col = st.selectbox("X軸を選択", df.select_dtypes(include=["number"]).columns, key="x")
        y_col = st.selectbox("Y軸を選択", df.select_dtypes(include=["number"]).columns, key="y")
        if x_col and y_col:
            chart = alt.Chart(df).mark_circle(size=60).encode(
                x=x_col, y=y_col, tooltip=list(df.columns)
            ).interactive()
            st.altair_chart(chart, use_container_width=True)

    elif chart_type == "ヒストグラム (分布)":
        num_col = st.selectbox("数値列を選択", df.select_dtypes(include=["number"]).columns, key="hist")
        bins = st.slider("ビン数", min_value=5, max_value=100, value=20, key="bins")
        if num_col:
            fig = px.histogram(df, x=num_col, nbins=bins, labels={num_col: "値", "count": "頻度"})
            st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "相関行列ヒートマップ":
        corr = df.corr()
        fig = px.imshow(
            corr,
            text_auto=".2f",
            aspect="auto",
            labels=dict(x="変数", y="変数", color="相関係数"),
            color_continuous_scale="RdBu_r",  # diverging scale
            zmin=-1, zmax=1
        )
        fig.update_xaxes(side="top")
        st.plotly_chart(fig, use_container_width=True)

else:
    st.info("左側のアップローダーから CSV ファイルを選択してください。")

