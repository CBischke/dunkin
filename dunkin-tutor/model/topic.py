from model.idea import Idea
from model.database import Database

import json

class Topic():
    """
    Represents an idea to be taught this will have a main idea and support
    """
    def __init__(self, file_of_origin):
        self.KEY_CORE_IDEA="core_idea"
        self.KEY_SUPPORTING_IDEA="supporting_ideas"
        self.KEY_FILE_OF_ORIGIN="file_of_origin"
        self.core_idea = None
        self.supporting_ideas = []
        self.file_of_origin = file_of_origin
        self.learning_objective = self.file_of_origin
        self.db = Database()

    def set_idea(self, string_idea, score):
        self.core_idea = Idea(string_idea, score)
        if len(self.core_idea.getQuestions()) == 0:
            return False
        return True

    def add_supporting_idea(self, string_supporting_idea, score):
        currentIdea = Idea(string_supporting_idea, score)
        if len(currentIdea.getQuestions()) == 0:
            return False
        self.supporting_ideas.append(currentIdea)
        return True


    def save_to_db(self):
        self.db.save_to_db(
            self.toJson()
        )

    def toJson(self): 
        item_to_save = {}
        item_to_save[self.KEY_CORE_IDEA] = self.core_idea.to_dict()
        item_to_save[self.KEY_FILE_OF_ORIGIN] = self.file_of_origin
        item_to_save[self.KEY_SUPPORTING_IDEA] = []
        

        for idea in self.supporting_ideas:
            item_to_save[self.KEY_SUPPORTING_IDEA].append(
                idea.to_dict()
            )
        return item_to_save

    def __str__(self):
        message = self.KEY_FILE_OF_ORIGIN + ": " + self.file_of_origin + "\n"
        message = message + "core idea:\n"+ str(self.core_idea) + "\n\n\n" + "supporting ideas:\n" 
        for idea in self.supporting_ideas:
            message = message + str(idea) + "\n\n"
        
        return message
