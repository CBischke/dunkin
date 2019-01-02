from tutor import Tutor

import json

class ConversationManager:

    def __init__(self):
        self.tutor = Tutor()

    def get_response(self, msg, u_id):
        return self.tutor.respond(msg, u_id)
