from core.pipeline.base import Stage
from core.message_context import process_user_message


class ProcessUserStage(Stage):
    def run(self, state):
        process_user_message(state)

        state.message_counter += 1