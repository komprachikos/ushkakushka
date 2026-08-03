import streamlit as st
from config import MODEL
from core.llm_client import LLMError
from core.memory import load_memory, save_memory
from core.prompts_builder import build_system_prompt
from core.chat_engine import process_message
from core.embeddings import rebuild_index

@st.cache_resource
def _init_embeddings():
    rebuild_index()
    return True

_init_embeddings()

st.set_page_config(page_title="Жильберта", page_icon="🤖", layout="centered")

def get_system_prompt():
    # Без @st.cache_resource — build_system_prompt сам кэширует personality.txt
    # и читает актуальный профиль из диска
    return build_system_prompt()

st.title("🤖 Жильберта")
st.caption("Локальный ИИ с собственной внутренней моделью мышления")

if "messages" not in st.session_state:
    saved = load_memory() or []
    st.session_state.messages = [{"role": "system", "content": get_system_prompt()}]
    st.session_state.messages.extend([m for m in saved if m.get("role") in ("user", "assistant")])
    # Счётчик = количество сохранённых user/assistant сообщений
    st.session_state.message_counter = len([m for m in saved if m.get("role") in ("user", "assistant")])

if "debug_mode" not in st.session_state:
    st.session_state.debug_mode = False

# Отрисовка сообщений (system пропускаем)
for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Напиши сообщение..."):
    # НЕ добавляем user-сообщение здесь — process_message сделает это сам
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Жильберта думает..."):
        try:
            answer, updated_messages, state, state_text, full_system_prompt, new_counter, reflection, curiosity = process_message(
                st.session_state.messages, prompt, st.session_state.message_counter
            )
            st.session_state.messages = updated_messages
            st.session_state.message_counter = new_counter
            st.session_state.last_state = state
            st.session_state.last_state_text = state_text
            st.session_state.last_full_prompt = full_system_prompt

            # Показываем reflection/curiosity как info-блоки
            if reflection:
                st.info(f"💭 Размышление Жильберты: {reflection}")
            if curiosity:
                st.info(f"🔍 Жильберта заинтересовалась: **{curiosity['topic']}** — {curiosity['reason']}")

        except LLMError as e:
            answer = f"[ОШИБКА] {e}"
            st.session_state.last_state = {}
            st.session_state.last_state_text = ""
            st.session_state.last_full_prompt = ""

    with st.chat_message("assistant"):
        st.markdown(answer)

with st.sidebar:
    st.header("⚙️ Управление")
    st.session_state.debug_mode = st.toggle("🔍 Режим отладки", value=st.session_state.debug_mode)

    st.divider()

    if st.button("🗑 Очистить диалог"):
        st.session_state.messages = [{"role": "system", "content": get_system_prompt()}]
        st.session_state.message_counter = 0
        for key in ("last_state", "last_state_text", "last_full_prompt"):
            st.session_state.pop(key, None)
        save_memory([])
        st.rerun()

    st.divider()
    st.caption(f"Модель: {MODEL}")
    st.caption(f"Сообщений: {st.session_state.message_counter}")

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
                        st.write(f"**Мысль:** {t.get('opinion', '')}")
                        st.divider()
                else:
                    st.write("Нет временных мыслей")

            with st.expander("📄 Полный промпт для модели", expanded=False):
                st.code(st.session_state.last_full_prompt, language="text")

            with st.expander("🔧 Сырое состояние (JSON)", expanded=False):
                st.json(state)
        else:
            st.info("Отправь сообщение, чтобы увидеть внутреннее состояние Жильберты")