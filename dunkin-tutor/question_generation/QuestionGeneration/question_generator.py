#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 14:04:55 2017

@author: sneha
"""

import subprocess

class QuestionGenerator(object):
	"""
	Define a class that generates questions given an input text file
	or a db connection. Currently supported db connection is mongodb.
	"""
	def __init__(self, input_file=None, mongod_collection=None):
		"""
		Arguments:
			input_file: A text file containing input statements
			to be converted to questions. One statement per line.
			mongod_collection: The reference to the mongodb
			 collection object from which to retrieve the statements from.
		"""

		if self.input_file:
        	input_file=input_file
            print("Reading from file")

		if self.mongod_collection:
			self.connection=mongod_collection
			print("Reading from mongodb")

		# Change dir to the path containing QuestionGeneration
		os.chdir("/Users/sneha/Documents/dev/SmithHeilmann_fork/QuestionGeneration/")

	def generate_question(self, input_sentence):
		"""
		Arguments:
			input_sentence: The declarative statement to be converted to a question. Should be in bytes.

		"""
		# This commands requires the question_generation package.
		# command = "java -Xmx1200m -cp question-generation.jar \ edu/cmu/ark/QuestionAsker --verbose --model models/linear-regression-ranker-reg500.ser.gz --prefer-wh --max-length 30 --downweight-pro"

        # completed = subprocess.run(['bash', 'run.sh'], check=True)
        p = Popen(['bash', 'run.sh'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        stdout = p.communicate(input=input_sentence)[0]
        return stdout.decode()


if __name__=='__main__':
	q = QuestionGenerator()
	q.generate_question(b'Researchers at the Massachusetts Institute of Technology’s Computer Science and Artificial Intelligence Laboratory (CSAIL) are developing a variety of robotics applications')
