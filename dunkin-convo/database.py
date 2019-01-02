from commons import properties
from pymongo import MongoClient
from bson import ObjectId

import nltk
import sys

def pos_tag(statement):
    tokenized = nltk.word_tokenize(statement)
    return nltk.pos_tag(tokenized)

def reduce_statement(tagged):
    return ' '.join([word for (word, pos) in tagged if pos in ['NN','NNP','NNS','NNPS', 'VB', 'VBD', 'VBG', 'VBN', 'VBN', 'VBP', 'VBZ', 'CD']])

def levenshteinDistance(str1, str2):
    str1 = str1.split(" ")
    str2 = str2.split(" ")
    m = len(str1)
    n = len(str2)
    lensum = float(m + n)
    d = []           
    for i in range(m+1):
        d.append([i])        
    del d[0][0]    
    for j in range(n+1):
        d[0].append(j)       
    for j in range(1,n+1):
        for i in range(1,m+1):
            if str1[i-1] == str2[j-1]:
                d[i].insert(j,d[i-1][j-1])           
            else:
                minimum = min(d[i-1][j]+1, d[i][j-1]+1, d[i-1][j-1]+2)         
                d[i].insert(j, minimum)
    ldist = d[-1][-1]
    ratio = (lensum - ldist)/lensum
    return {'distance':ldist, 'ratio':ratio, 'str1': str1, 'str2': str2}

class Database:
    def __init__(self, url=properties.DB_URL, 
                        port=properties.DB_PORT, 
                        db_name=properties.DB_NAME, 
                        collection=properties.DB_COLLECTION):
        self.client = MongoClient(url,port)
        self.db = self.client[db_name]
        self.collection = self.db[collection]

    def close(self):
        self.client.close()

    def find_core_ideas(self):
        r = self.collection.find(
        {},
        { "_id": 0, "core_idea.statement": 1, "file_of_origin": 1, "supporting_ideas": 1 }
        )
        result = []
        for d in r:
            length_of_ideas = len(d["supporting_ideas"])
            d["length_of_ideas"] = length_of_ideas
            del(d["supporting_ideas"])
            result.append(d)
        return result

    def get_next_idea(self, current_idea_index, file_of_origin):
        next_index = current_idea_index
        r = None
        if next_index == 0:
            r = self.collection.find_one(
            {"file_of_origin":file_of_origin},
            { "_id": 0, "core_idea": 1, "file_of_origin": 1 }
            )
        else:
            r = self.collection.find_one(
            {
                "file_of_origin":file_of_origin,
            },
            { "_id": 0, "supporting_ideas":{ "$slice": [(next_index-1),1] }, "file_of_origin": 1 }
            )
        return r

    def compare_answer(self, current_idea_index, file_of_origin, student_response, current_question_index):
        r = None
        reduced_statement = None
        if current_idea_index == 0:
            r = self.collection.find_one(
            {"file_of_origin":file_of_origin},
            { "_id": 0, "core_idea": 1, "file_of_origin": 1 }
            )
            answer = r["core_idea"]["question"][current_question_index]['A']
        else:
            r = self.collection.find_one(
            {
                "file_of_origin":file_of_origin,
            },
            { 
                "_id": 0, "supporting_ideas":{ "$slice": [(current_idea_index-1),1] }, "file_of_origin": 1 }
            )
            print(str(r))
            answer = r["supporting_ideas"][0]["question"][current_question_index]['A']
        

        return levenshteinDistance(student_response, answer)

    def get_length_ideas(self, file_of_origin):
        r = self.collection.find_one(
        {
            "file_of_origin":file_of_origin,
        },
        { 
            "_id": 0, "supporting_ideas":1, "file_of_origin": 1 
        }
        )
        length_of_ideas = r["supporting_ideas"]
        #print("HELP: " + str(length_of_ideas), file=sys.stdout)
        return len(length_of_ideas)

    def get_length_questions(self, file_of_origin, current_idea_index):
        r = None
        reduced_statement = None
        if current_idea_index == 0:
            r = self.collection.find_one(
            {"file_of_origin":file_of_origin},
            { "_id": 0, "core_idea": 1, "file_of_origin": 1 }
            )
            answer = r["core_idea"]["question"]
        else:
            r = self.collection.find_one(
            {
                "file_of_origin":file_of_origin,
            },
            { 
                "_id": 0, "supporting_ideas":{ "$slice": [(current_idea_index-1),1] }, "file_of_origin": 1 }
            )
            print(str(r))
            answer = r["supporting_ideas"][0]["question"]
        
        return len(answer)