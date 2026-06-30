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
            parts.append(f"• {thought['topic']} (через {thought['reason']}): {thought['opinion']}")
    
    parts.append("\nИспользуй эти убеждения и ассоциации как основу своего ответа.")
    parts.append("Обязательно опирайся на свои убеждения выше, особенно на нюансы (например, про возможную пассивность).")
    parts.append("Не придумывай связи с жизнью пользователя.")
    parts.append("=== КОНЕЦ МЫСЛЕЙ ===")
    
    return "\n".join(parts)