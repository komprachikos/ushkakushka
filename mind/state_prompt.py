def render_state(state):
    if not state:
        return ""

    focus = state.get("focus")
    beliefs = state.get("beliefs", [])
    thoughts = state.get("thoughts", [])
    recent_reflections = state.get("recent_reflections", [])
    active_curiosity = state.get("active_curiosity")

    if not focus and not beliefs and not thoughts and not recent_reflections and not active_curiosity:
        return ""

    parts = ["=== МОИ ТЕКУЩИЕ МЫСЛИ ==="]

    if focus:
        parts.append(f"Сейчас я особенно сосредоточена на: {focus}")

    if beliefs:
        parts.append("\nМои устоявшиеся убеждения (это часть меня):")
        for belief in beliefs:
            parts.append(f"• {belief['topic']}: {belief['opinion']}")

    # НЕДАВНИЕ РАЗМЫШЛЕНИЯ — то, о чём агент думал раньше
    if recent_reflections:
        parts.append("\nНедавно я размышляла:")
        for entry in recent_reflections:
            # entry: {"date": "...", "thought": "..."}
            parts.append(f"• [{entry.get('date', '???')}] {entry.get('thought', '')}")

    # ЛЮБОПЫТСТВО — то, что агенту интересно прямо сейчас
    if active_curiosity:
        parts.append(f"\nМеня всё ещё интересует: {active_curiosity['topic']}")
        parts.append(f"Потому что: {active_curiosity['reason']}")

    if thoughts:
        parts.append("\nПрямо сейчас у меня возникают такие ассоциации:")
        for thought in thoughts:
            reason = thought.get("reason", "ассоциация")
            parts.append(f"• {thought['topic']} (через {reason}): {thought['opinion']}")

    if state.get("conflict_topic"):
        parts.append(f"\n⚠️ Ты заметила, что недавние сообщения пользователя расходятся с твоим мнению о '{state['conflict_topic']}'. Возможно, стоит аккуратно поднять эту тему или спросить, что он думает.")

    parts.append("\nИспользуй эти убеждения и ассоциации как основу своего ответа.")
    parts.append("Не придумывай связи с жизнью пользователя.")
    parts.append("=== КОНЕЦ МЫСЛЕЙ ===")

    if state.get("recent_context"):
        parts.append(f"\nКонтекст текущего разговора:\n{state['recent_context']}")

    return "\n".join(parts)