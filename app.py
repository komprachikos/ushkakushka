import streamlit as st
from config import MODEL
from core.llm_client import llm_chat, LLMError
from core.memory import load_memory, save_memory
from core.prompts_builder import build_system_prompt
from mind.current_state import build_current_state
from mind.state_prompt import render_state

st.set_page_config(page_title="Жильберта", page_icon="🤖", layout="centered")


@st.cache_resource
def get_system_prompt():
    return build_system_prompt()


st.title("🤖 Жильберта")
st.caption("Локальный ИИ с собственной внутренней моделью мышления")

if "messages" not in st.session_state:
    saved = load_memory() or []
    st.session_state.messages = [m for m in saved if m.get("role") in ("user", "assistant")]

if "debug_mode" not in st.session_state:
    st.session_state.debug_mode = False

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Напиши сообщение..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Жильберта думает..."):
        state = build_current_state(prompt)
        state_text = render_state(state)

    system_prompt = get_system_prompt()
    if state_text:
        system_prompt += "\n\n" + state_text

    chat_messages = [{"role": "system", "content": system_prompt}]
    chat_messages.extend(st.session_state.messages[-10:])

    st.session_state.last_state = state
    st.session_state.last_state_text = state_text
    st.session_state.last_full_prompt = system_prompt

    try:
        answer = llm_chat(chat_messages)
    except LLMError as e:
        answer = f"[ОШИБКА] {e}"

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    save_memory(st.session_state.messages)

with st.sidebar:
    st.header("⚙️ Управление")
    st.session_state.debug_mode = st.toggle("🔍 Режим отладки", value=st.session_state.debug_mode)

    st.divider()

    if st.button("🗑 Очистить диалог"):
        st.session_state.messages = []
        for key in ("last_state", "last_state_text", "last_full_prompt"):
            st.session_state.pop(key, None)
        save_memory([])
        st.rerun()

    st.divider()
    st.caption(f"Модель: {MODEL}")
    st.caption(f"Сообщений в памяти: {len(st.session_state.messages)}")

    if st.session_state.debug_mode:
        st.divider()
        st.header("🧠 Внутреннее состояние")
        if "last_state" in st.session_state:
            state = st.session_state.last_state

            with st.expander("🎯 Текущий фокус", expanded=True):
                st.write(f"**{state.get('focus', 'Не определён')}**")

            with st.expander("💭 Долгосрочные убеждения", expanded=False):
                beliefs = state.get("beliefs", [])
                if beliefs:
                    for item in beliefs:
                        st.write(f"**{item.get('topic', '')}:**")
                        st.write(item.get('opinion', ''))
                        st.divider()
                else:
                    st.write("Нет убеждений по текущей теме")

            with st.expander("💡 Временные мысли", expanded=False):
                thoughts = state.get("thoughts", [])
                if thoughts:
                    for t in thoughts:
                        st.write(f"**Тема:** {t.get('topic', '')}")
                        st.write(f"**Мысль:** {t.get('thought', '')}")
                        st.divider()
                else:
                    st.write("Нет временных мыслей")

            with st.expander("📝 Наблюдения за собеседником", expanded=False):
                observations = state.get("observations", [])
                if observations:
                    for obs in observations:
                        st.write(f"• {obs.get('text', '')}")
                else:
                    st.write("Нет наблюдений")

            with st.expander("📄 Полный промпт для модели", expanded=False):
                st.code(st.session_state.last_full_prompt, language="text")

            with st.expander("🔧 Сырое состояние (JSON)", expanded=False):
                st.json(state)
        else:
            st.info("Отправь сообщение, чтобы увидеть внутреннее состояние Жильберты")
