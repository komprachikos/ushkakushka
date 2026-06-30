from brain.curiosity import generate_curiosity

conversation = """
Пользователь:
Мне кажется, стоицизм сильно отличается от экзистенциализма.

Жильберта:
Да, особенно в отношении контроля над жизнью.

Пользователь:
Я бы хотел позже поговорить о стоицизме подробнее.
"""

print(
    generate_curiosity(conversation)
)