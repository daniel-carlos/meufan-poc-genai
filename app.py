import streamlit as st
from uuid import uuid4
import time
import persist
import config
from streamlit_local_storage import LocalStorage
import llm

localS = LocalStorage()

st.set_page_config(
    page_title=config.TITLE,
)

st.markdown("""
    <style>
        .stAppToolbar {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

def new_session():
    st.session_state.stage = "password"
    st.session_state.password_invalid = False
    st.session_state.chat_id = f"{uuid4()}"
    st.session_state.history = []

def confirm_password():
    if st.session_state.password == config.PASSWORD:
        st.session_state.password_invalid = False
        st.session_state.stage = "identity"
        localS.setItem("password_valid", "1")
        st.session_state.password = None
    else:
        st.session_state.password_invalid = True
        localS.setItem("password_valid", "0")

def save_chat():
    persist.save_chat(st.session_state.user_id, st.session_state.chat_id)
    localS.setItem("user_id", st.session_state.user_id)
    st.session_state.stage = "chat"

def convert_to_stream(text):
    for char in text:
        yield char
        time.sleep(0.01)

def save_feedback(index):
    st.session_state.history[index]["feedback"] = st.session_state[f"{index}"]
    persist.save_feedback(
        st.session_state.chat_id,
        st.session_state.history[index]["id"],
        st.session_state.history[index]["feedback"],
    )
    st.toast('Feedback registrado!')

if "stage" not in st.session_state:
    password_valid_saved = localS.getItem("password_valid")
    user_id_saved = localS.getItem("user_id")

    new_session()

    if password_valid_saved == "1":
        st.session_state.stage = "identity"

    if user_id_saved:
        st.session_state.user_id = user_id_saved
        st.session_state.stage = "chat"
        save_chat()

def logout():
    localS.deleteAll()
    del st.session_state["stage"]
    new_session()

st.title(config.TITLE)
st.subheader(config.SUBTITLE)

if st.session_state.stage == "chat":
    st.button("Sair", on_click=logout)

if st.session_state.stage == "password":
    password = st.text_input("Digite a senha para conseguir acessar o sistema", type='password')

    if password:
        st.session_state.password = password
        st.button("Confirmar", on_click=confirm_password)
        if st.session_state.password_invalid:
            st.error("Senha incorreta")

if st.session_state.stage == "identity":
    user_id = st.text_input("Se identifique para começar a conversar.")

    if user_id:
        st.session_state.user_id = user_id
        st.button("Começar", on_click=save_chat)

if st.session_state.stage == "chat":
    for i, message in enumerate(st.session_state.history):
        with st.chat_message(message["role"]):
            st.write(message["content"])
            if message["role"] == "assistant":
                feedback = message.get("feedback", None)
                st.session_state[f"feedback_{i}"] = feedback
                st.feedback(
                    "thumbs",
                    key=f"{i}",
                    disabled=feedback is not None,
                    on_change=save_feedback,
                    args=[i],
                )

    if prompt := st.chat_input("Diga alguma coisa"):
        with st.chat_message("user"):
            st.write(prompt)
        st.session_state.history.append({"id": f"{uuid4()}", "role": "human", "content": prompt})
        persist.save_message(
            st.session_state.chat_id,
            st.session_state.history[-1]["id"],
            st.session_state.history[-1]["role"],
            st.session_state.history[-1]["content"],
            0,
            0,
        )
        with st.chat_message("assistant"):
            response_data = llm.generate_response(prompt, st.session_state.history[:-1])
            # print(response_data)
            response = st.write_stream(convert_to_stream(response_data['content']))
            st.feedback(
                "thumbs",
                key=f"{len(st.session_state.history)}",
                on_change=save_feedback,
                args=[len(st.session_state.history)],
            )
        st.session_state.history.append({"id": f"{uuid4()}", "role": "assistant", "content": response_data['content']})
        persist.save_message(
            st.session_state.chat_id,
            st.session_state.history[-1]["id"],
            st.session_state.history[-1]["role"],
            st.session_state.history[-1]["content"],
            response_data['input_tokens'],
            response_data['output_tokens'],
        )