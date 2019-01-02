import nltk
import re
from question_generation.question_generator import QuestionGenerator



def pos_tag(statement):
    tokenized = nltk.word_tokenize(statement)
    return nltk.pos_tag(tokenized)

def reduce_statement(tagged):
    return ' '.join([word for (word, pos) in tagged if pos in ['NN','NNP','NNS','NNPS', 'VB', 'VBD', 'VBG', 'VBN', 'VBN', 'VBP', 'VBZ', 'CD']])

def clean_up_statement(statement):
    return re.sub('\[.*?\]', '', statement)

class Axiom:
    def __init__(self, statement, score):
        self.statement = clean_up_statement(statement)
        self.score = score
        self.q  = QuestionGenerator()
        self.pos_statement = pos_tag(self.statement)
        print("converting...")
        self.question = self.statement_into_question(self.statement)
        print("done converting")
        self.statement_reduced = reduce_statement(self.pos_statement)

    def getQuestions(self):
        return self.question

    def statement_into_question(self, statement):
        q_a = self.q.generate_question(statement)
        final_qa = []
        for pair in q_a:
            print("pair: " + str(pair))
            question = pair['Q'].split(' ')
            first_answer = pair['A'].split(' ')
            s = set(question)
            temp3 = [x for x in first_answer if x not in s]
            modified_answer  = temp3
            final_qa.append({'Q': ' '.join(question), 'A': ' '.join(modified_answer)})
            print("MOD_ANSWER: " + str(modified_answer))
        return final_qa

    def __str__(self):
        return "(" + str(self.score) + ")" + str(self.statement) + \
        "\n question:" + str(self.question) + \
        "\n statement_reduced: " + str(self.statement_reduced) + \
        "\n pos_statement: " + str(self.pos_statement)

    def to_dict(self):
        return {
            "statement":self.statement,
            "score":self.score,
            "question": self.question,
            "statement_reduced": self.statement_reduced,
            "pos_statement": self.pos_statement
        }