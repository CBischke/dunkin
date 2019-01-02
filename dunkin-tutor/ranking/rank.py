from nltk.tokenize import sent_tokenize
from lexrank import STOPWORDS, LexRank
from path import Path
import numpy as np
import sys
import nltk.data


class Rank():

    def __init__(self, training_dir=None):
        self.training_dir = training_dir
        self.lxr = None

    def train(self):
        documents = []
        documents_dir = Path(self.training_dir)

        for file_path in documents_dir.files('*.txt'):
            with file_path.open(mode='rt', encoding='utf-8') as fp:
                documents.append(fp.readlines())

        self.lxr = LexRank(documents, stopwords=STOPWORDS['en'])

    def remove_new_line(self, text):
        """
        Removes all new lines chars in text
        """
        return text.replace('\n', ' ')

    def setence_tokenize(self, text):
        """
        sentence tokenize
        """
        return sent_tokenize(text)

    def sort_rankings(self, scores_sents):
        idx = np.argsort(scores_sents[0])[::-1]
        scores = np.array(scores_sents[0])[idx]
        sentences = np.array(scores_sents[1])[idx]
        return list(zip(scores, sentences))


    def rank(self, text):
        sentences = text
        sentences = self.remove_new_line(sentences)
        sentences = self.setence_tokenize(sentences)
        sentences = self.lxr.get_summary(sentences, summary_size=6, threshold=.85)

        scores_cont = self.lxr.rank_sentences(
            sentences,
            threshold=None,
            fast_power_method=True,
        )

        return self.sort_rankings((scores_cont, sentences))
    
