import streamlit as st
st.title("Hello World Bot")
user_input = st.text_input("Скажи что-нибудь:")
if user_input:
    st.write("Бот отвечает: Hello World!")
