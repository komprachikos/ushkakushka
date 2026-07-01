import streamlit as st
from config import MODEL
from ollama import chat

from core.memory import load_memory, save_memory
from core.profile_memory import load_profile
from mind.current_state import build_current_state
from mind.state_prompt import render_state


st.set_page_config(page_title="Жильберта", page_icon="🤖", layout="centered")


@st.cache_resource
def get_system_prompt():
    """Загружается один раз и кэшируется."""
    profile = load_profile()
    profile_text = f"""Информация о пользователе:

Имя: {profile.get('name', 'Сергей')}
Факты:
{chr(10).join(profile.get('facts', []))}
"""
    with open("prompts/personality.txt", "r", encoding="utf-8") as f:
        personality = f.read()
    return personality + "\n\n" + profile_text


# Заголовок
st.title("🤖 Жильберта")
st.caption("Локальный ИИ с собственной внутренней моделью мышления")

# Инициализация истории сообщений
if "messages" not in st.session_state:
    saved = load_memory() or []
    st.session_state.messages = [m for m in saved if m["role"] in ["user", "assistant"]]

# Переключатель отладочного режима
if "debug_mode" not in st.session_state:
    st.session_state.debug_mode = False


# Отображение истории
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# Поле ввода
if prompt := st.chat_input("Напиши сообщение..."):
    # 1. Добавляем сообщение пользователя
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Строим внутреннее состояние Жильберты
    with st.spinner("Жильберта думает..."):
        state = build_current_state(prompt)
        state_text = render_state(state)

        # 3. Формируем промпт
        system_prompt = get_system_prompt()
        if state_text:
            system_prompt += "\n\n" + state_text

        chat_messages = [{"role": "system", "content": system_prompt}]
        chat_messages.extend(st.session_state.messages[-10:])

        # 4. Сохраняем состояние для отладочной панели
        st.session_state.last_state = state
        st.session_state.last_state_text = state_text
        st.session_state.last_full_prompt = system_prompt

        # 5. Вызов LLM
        response = chat(model=MODEL, messages=chat_messages)
        answer = response["message"]["content"]

    # 6. Показываем ответ
    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

    # 7. Сохраняем память
    save_memory(st.session_state.messages)


# Боковая панель с отладкой
with st.sidebar:
    st.header("⚙️ Управление")
    
    # Переключатель отладочного режима
    st.session_state.debug_mode = st.toggle("🔍 Режим отладки", value=st.session_state.debug_mode)
    
    st.divider()
    
    if st.button("🗑 Очистить диалог"):
        st.session_state.messages = []
        if "last_state" in st.session_state:
            del st.session_state.last_state
            del st.session_state.last_state_text
            del st.session_state.last_full_prompt
        save_memory([])
        st.rerun()
    
    st.divider()
    st.caption(f"Модель: {MODEL}")
    st.caption(f"Сообщений в памяти: {len(st.session_state.messages)}")
    
    # Отладочная панель
    if st.session_state.debug_mode:
        st.divider()
        st.header("🧠 Внутреннее состояние")
        
        if "last_state" in st.session_state:
            state = st.session_state.last_state
            
            # Фокус разговора
            with st.expander("🎯 Текущий фокус", expanded=True):
                focus = state.get("focus", "Не определён")
                st.write(f"**{focus}**")
            
            # Долгосрочные убеждения
            with st.expander("💭 Долгосрочные убеждения", expanded=False):
                beliefs = state.get("beliefs", [])
                if beliefs:
                    for item in beliefs:
                        st.write(f"**{item.get('topic', '')}:**")
                        st.write(item.get('opinion', ''))
                        st.divider()
                else:
                    st.write("Нет убеждений по текущей теме")
            
            # Временные мысли
            with st.expander("💡 Временные мысли", expanded=False):
                thoughts = state.get("thoughts", [])
                if thoughts:
                    for t in thoughts:
                        st.write(f"**Тема:** {t.get('topic', '')}")
                        st.write(f"**Мысль:** {t.get('thought', '')}")
                        st.divider()
                else:
                    st.write("Нет временных мыслей")
            
            # Наблюдения из журнала
            with st.expander("📝 Наблюдения за собеседником", expanded=False):
                observations = state.get("observations", [])
                if observations:
                    for obs in observations:
                        st.write(f"• {obs.get('text', '')}")
                else:
                    st.write("Нет наблюдений")
            
            # Полный промпт
            with st.expander("📄 Полный промпт для модели", expanded=False):
                st.code(st.session_state.last_full_prompt, language="text")
            
            # Сырое состояние (JSON)
            with st.expander("🔧 Сырое состояние (JSON)", expanded=False):
                st.json(state)
        
        else:
            st.info("Отправь сообщение, чтобы увидеть внутреннее состояние Жильберты")