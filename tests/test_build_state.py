from mind.current_state import build_current_state

state = build_current_state("что ты думаешь о стоицизме?")

print("=== STATE ===")
print(state)

print()
print("=== BELIEFS ===")
print(state["beliefs"])

print()
print("=== THOUGHTS ===")
print(state["thoughts"])