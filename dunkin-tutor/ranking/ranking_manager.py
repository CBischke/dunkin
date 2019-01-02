from ranking.rank import Rank
from model.topic import Topic
from commons import properties

import os
class Ranking_Manager():

    def __init__(self, training_directory=properties.RANKING_TRAINING_FOLDER,
                        inference_directory=properties.RANKING_INPUT_FOLDER):

        self.rank = Rank(training_dir=training_directory)
        self.rank.train()
        self.inference_folder=inference_directory
    
    def run_inference_on_folder(self):
        rankings = []
        for root, dirs, files in os.walk(self.inference_folder):  
            for filename in files:
                infile = open(root + filename, "r")
                sentences = infile.read()
                infile.close()
                rankings.append(self.save_to_topics(self.rank.rank(sentences), filename))
        return rankings

    def run_inference_on_material(self, material, file_name):
        return self.save_to_topics(self.rank.rank(material), file_name)

    def save_to_topics(self, rankings, file_name):
        """
        this method takes a tuple of rankings: (score, sentence) then saves it to the topic model
        """
        topic = Topic(file_name)
        foundCore = False
        for i in range(len(rankings)):
            score = rankings[i][0]
            sent = rankings[i][1]
            if not foundCore:
                if topic.set_idea(sent, score):
                    foundCore = True
                continue
            topic.add_supporting_idea(sent, score)
        topic.save_to_db()
        return topic
        