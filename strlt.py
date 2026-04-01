import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Titanic Dashboard", page_icon="🚢", layout="wide")

DATA_URL = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"

@st.cache_data
def load_data():
    return pd.read_csv(DATA_URL)

df = load_data()

st.title("Дашбоард по Titanic")

st.sidebar.header("Параметры")
n_rows = st.sidebar.slider("Сколько первых строк показать", 1, len(df), 5)
selected_sex = st.sidebar.selectbox("Пол для интерактивного графика", df["Sex"].dropna().unique())

st.subheader("Описательная статистика")
st.write("Форма таблицы:", df.shape)

types_df = pd.DataFrame({
    "column": df.columns,
    "dtype": df.dtypes.astype(str).values
})
st.write("Столбцы и типы данных:")
st.dataframe(types_df, use_container_width=True)

st.subheader("Первые n строк таблицы")
st.dataframe(df.head(n_rows), use_container_width=True)

st.subheader("Графики")

col1, col2 = st.columns(2)

with col1:
    fig1 = px.histogram(
        df,
        x="Age",
        color="Sex",
        title="1. Распределение возраста"
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    pclass_counts = df["Pclass"].value_counts().sort_index().reset_index()
    pclass_counts.columns = ["Pclass", "count"]
    fig2 = px.bar(
        pclass_counts,
        x="Pclass",
        y="count",
        color="Pclass",
        title="2. Количество пассажиров по классу"
    )
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    survived_counts = df["Survived"].value_counts().reset_index()
    survived_counts.columns = ["Survived", "count"]
    fig3 = px.pie(
        survived_counts,
        names="Survived",
        values="count",
        title="3. Выжившие / невыжившие",
        color_discrete_sequence=px.colors.sequential.Rainbow
    )
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    fig4 = px.strip(
        df,
        x="Pclass",
        y="Fare",
        color="Pclass",
        title="4. Стоимость билетов по классам"
    )
    st.plotly_chart(fig4, use_container_width=True)

filtered_df = df[df["Sex"] == selected_sex]
fig5 = px.histogram(
    filtered_df,
    x="Age",
    color="Survived",
    barmode="overlay",
    title=f"5. Возраст пассажиров ({selected_sex}) — интерактивный график"
)
st.plotly_chart(fig5, use_container_width=True)
