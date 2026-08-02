def render_state(state):
    if not state:
        return ""

    focus = state.get("focus")
    beliefs = state.get("beliefs", [])
    thoughts = state.get("thoughts", [])

    if not focus and not beliefs and not thoughts:
        return ""

    parts = ["=== МОИ ТЕКУЩИЕ МЫСЛИ ==="]

    if focus:
        parts.append(f"Сейчас я особенно сосредоточена на: {focus}")

    if beliefs:
        parts.append("\nМои устоявшиеся убеждения (это часть меня):")
        for belief in beliefs:
            parts.append(f"• {belief['topic']}: {belief['opinion']}")

    if thoughts:
        parts.append("\nПрямо сейчас у меня возникают такие ассоциации:")
        for thought in thoughts:
            reason = thought.get("reason", "ассоциация")
            parts.append(f"• {thought['topic']} (через {reason}): {thought['opinion']}")

    parts.append("\nИспользуй эти убеждения и ассоциации как основу своего ответа.")
    parts.append("Не придумывай связи с жизнью пользователя.")
    parts.append("=== КОНЕЦ МЫСЛЕЙ ===")

    if state.get("recent_context"):
        parts.append(f"\nКонтекст текущего разговора:\n{state['recent_context']}")

    return "\n".join(parts)