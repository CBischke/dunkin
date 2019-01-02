from requester import Requester
from commons import properties
from user import User

import json
import random
import math
import sys

def find_values(id, json_repr):
  results = []

  def _decode_dict(a_dict):
    try:
      results.append(a_dict[id])
    except KeyError:
      pass
    return a_dict

  json.loads(json_repr, object_hook=_decode_dict)  # Return value ignored.
  return results

class Tutor:
    def __init__(self):
        self.topics_requester = Requester(properties.CONVO_URL_TOPICS)
        self.answer_requester = Requester(properties.CONVO_URL_ANSWER)
        self.question_requester = Requester(properties.CONVO_URL_QUESTION)
        self.question_length_requester = Requester(properties.CONVO_URL_LENGTH)
        self.topic_commands = ["topic", "topics", "t"]
        self.current_topic = None
        self.current_level = None
        self.users = {}
        pass
    
    def respond(self, message, u_id):

        if u_id not in self.users:
            self.users[u_id] = User(u_id)

        user = self.users[u_id]

        if message == "!exit":
            user.isWaitingForAnswer = False
            return "help for list of commands. <br /> try topics to show a list of learning material"
        
        if user.isWaitingForAnswer:
            return self.compare_answer(message, user)

        if message in self.topic_commands:
            return self.get_topics()
        elif "ask" in message:
            message = message.split(" ")
            self.set_topic(user, message[1])
            return self.ask_question(user)
        elif "help" in message:
            return "topics <br /> ask [topic] <br /> !exit - to stop asking questions"
        return "not a valid command"

    def ask_question(self, u):
        u.isWaitingForAnswer = True
        resp = find_values('Q', self.question_requester.call(headers={
            'student-response':'None',
            'file-of-origin': u.current_topic,
            'current-idea-index':str(u.current_level)
        }))
        print(str(resp))
        if not resp:
            return "something went wrong.."
        message = "\n\n"
        choice = random.randint(0, (len(resp) - 1))
        u.current_question_index = choice
        message = message + resp[choice] + "\n"
        return message

    def compare_answer(self, student_resp, u):
        u.isWaitingForAnswer = False
        print("HELP: " + str(u.current_question_index), file=sys.stdout)
        resp = find_values('ratio', self.answer_requester.call(headers={
            'student-response': student_resp,
            'file-of-origin': u.current_topic,
            'current-idea-index':str(u.current_level),
            'current-question-index':str(u.current_question_index)
        }))[0]
        answer_score = float(resp)
        print("HELP: " + str(answer_score), file=sys.stdout)
        if answer_score > .25: #correct ()
            if str(u.current_level) == str(u.total_topics):
                return "Try asking a new topic. <br />" + self.get_topics()
            else:
                self.away_from_core(u)
                resp = self.ask_question(u)
        else: #incorrect
            if u.current_level == 0:
                u.current_level = u.current_level + 1
            else:
                self.towards_core(u)
            resp = self.ask_question(u)
        if not resp:
            return "something went wrong."
        return resp


    def get_topics(self):
        resp = find_values('file_of_origin', self.topics_requester.call())
        message = ""
        for topics in resp:
            message = message + topics + "<br />"
        return message

    def removeUser(self, u):
        del self.users[u.uid]

    def set_topic(self, u, topic):
        u.current_topic = topic
        u.total_topics = int(self.question_length_requester.call(headers={
            'file-of-origin': u.current_topic,
        }).strip())
        u.current_level = str(math.trunc(u.total_topics/2))
        print("HELP: " + u.current_level)

    def away_from_core(self, u):
        u.current_level = str(int(u.current_level) + 1)

    def towards_core(self, u):
        u.current_level = str(int(u.current_level) - 1)
