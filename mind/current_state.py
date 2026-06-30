from brain.recall import recall_memories
from mind.context_builder import build_internal_thought



def build_current_state(user_text):

    memories = recall_memories(user_text)

    state = {
        "focus": None,
        "beliefs": [],
        "thoughts": []
    }

    if memories["knowledge"]:
        state["focus"] = memories["knowledge"][0]["topic"]
        for item in memories["knowledge"]:

            state["beliefs"].append(
                {
                    "topic": item["topic"],
                    "summary": item["summary"],
                    "opinion": item["opinions"][-1]["text"]
                }
            )

        thought = build_internal_thought(state["focus"])

        if thought:
            state["thoughts"].append(thought)

    return state