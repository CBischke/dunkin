class User:
    def __init__(self, uid):
        self.uid = uid
        self.current_topic = None
        self.current_level = None
        self.current_question_index = None
        self.isWaitingForAnswer = False
        self.total_topics = -1