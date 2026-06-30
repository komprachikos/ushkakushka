def render_state(state):
    if not state:
        return ""
    
    focus = state.get("focus")
    beliefs = state.get("beliefs", [])
    thoughts = state.get("thoughts", [])
    
    
    if not focus and not beliefs and not thoughts:
        return ""
    
    parts = []
    parts.append("=== CURRENT STATE ===")
    parts.append("")
    
    if focus:
        parts.append("Current focus:")
        parts.append(focus)
        parts.append("")
    
    if beliefs:
        parts.append("Your long-term beliefs:")
        parts.append("")
        
        for belief in beliefs:
            parts.append(f"Topic: {belief['topic']}")
            parts.append(f"Summary: {belief['summary']}")
            parts.append(f"You genuinely believe: {belief['opinion']}")
    
    if thoughts:
        parts.append("")
        parts.append("=== ВНУТРЕННЕЕ РАЗМЫШЛЕНИЕ ===")
        parts.append("Прежде чем ответить, обдумай эти мысли:")
        parts.append("")
    
        for thought in thoughts:
            parts.append(f"Тема: {thought['topic']}")
            parts.append(f"Причина: {thought['reason']}")
            parts.append(f"Мысль: {thought['opinion']}")
            parts.append("")
    
        parts.append("Используй эти размышления, чтобы сформировать свой ответ.")
        parts.append("Но не упоминай их явно — отвечай естественно.")
    
    parts.append("=== END OF STATE ===")
    
    return "\n".join(parts)