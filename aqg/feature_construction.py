from __init__ import *
from nltk.corpus import stopwords

class FeatureConstruction:
	def __init__(self):
		self.classifier = os.environ.get('CLASSIFIER_PATH')

	def _num_token_in_answer(self, row):
		"""Get number of tokens in answer 
		Args:
		    row(pandas.datafrane): current row vector
		Return:
		    row(pandas.datafrane): row vector with new feature 
		"""
		answer = row.Answer
		try:
			row['Num_Tokens_In_Answer'] = len(answer.split())
			return row
		except:
			row['Num_Tokens_In_Answer'] = 0
			return row

	def _num_token_in_sentence(self, row):
		"""Get number of tokens in question
		Args:
		    row(pandas.dataframe): current row vector
		Return:
		    row(pandas.dataframe): row vector with new feature 
		"""
		question = row.Question
		try:
			row['Num_Tokens_In_Sentence'] = len(question.split())
			return row
		except:
			row['Num_Tokens_In_Sentence'] = 0
			return row

	def _num_row_tokens_matching_in_out(self, row):
		"""Number of tokens in the answer that match tokens outside of the answer
		Args:
		    row(pandas.dataframe): input pandas dataframe
		Return:
		    row(pandas.dataframe): result a pandas dataframe with new feature
		"""
		answer = row.Answer 
		question = row.Question 
		try:
			interaction = [i for i in answer_tokens if i in question]
			row['Num_Token_Match_Question'] = len(interaction)
			return row
		except:
			row['Num_Token_Match_Question'] = 0
			return row

	def _percentage_token_in_answer(self, row):
		"""Percent of the sentence tokens that are in the answer
		Args:
		    row(pandas.dataframe): input pandas dataframe
		Return:
		    row(pandas.dataframe): result a pandas dataframe with new feature
		"""
		answer_len = row.Num_Tokens_In_Answer
		sentence_len = row.Num_Tokens_In_Sentence - answer_len
		try:
			row['Percentage_Token_In_Answer'] = float(answer_len)/sentence_len
			return row
		except:
			row['float(answer_len)/sentence_len'] = 0
			return row

	def _percentage_token_in_out_answer(self, row):
		"""Percent of the sentence tokens that are in the answer (exclude answer length)
		Args:
		    row(pandas.datafrane): input row vector 
		Return:
		    row(pandas.dataframe): output row vector with new feature 
		"""
		answer_len = row.Num_Tokens_In_Answer
		sentence_len = row.Num_Tokens_In_Sentence
		try:
			row['Percentage_Token_In_Out_Answer'] = float(answer_len)/sentence_len
			return row 
		except:
			row['float(answer_len)/sentence_len'] = 0
			return row 

	def _answer_capitalized_word_density(self, row):
		"""Percentage of tokens in the answer that are all caps
		Args:
		    row(pandas.dataframe): input row vector
		Return:
		    row(pandas.dataframe): ouput row vector with new features
		"""
		answer = row.Answer
		try:
			tokens = answer.split()
			num_tokens = len(tokens)
			cap_tokens = [i for i in tokens if i.isupper()==True]
			num_cap_tokens = len(cap_tokens)
			row['Answer_Capitalized_Word_Density'] = float(num_cap_tokens)/num_tokens
			return row 
		except:
			row['float(num_cap_tokens)/num_tokens'] = 0
			return row

	def _answer_pronun_density(self, row):
		"""Percentage of tokens in the answer that are pronouns
		Args:
		    row(pandas.dataframe): input row vector
		Return:
		    row(pandas.dataframe): result a row dataframe with new feature
		"""
		answer = row.Answer
		try:
			row['ANSWER_PRONOMINAL_DENSITY'] = self._identify_pronoun(answer)
			return row
		except:
			row['ANSWER_PRONOMINAL_DENSITY'] = 0
			return row

	def _identify_pronoun(self, answer):
		"""Calculate percentage of pronouns within answer
		Args:
		    answer(str): answer text
		Return:
		    percentage(float): ratio of pronouns in answer
		"""
		text = nltk.word_tokenize(answer)
		post = nltk.pos_tag(text)
		pronoun_list = ['PRP', 'PRP$', 'WP', 'WP$']
		#init variables
		num_pronouns = 0
		num_terms = len(post)
		percentage = 0
		for k, v in post:
			if v in pronoun_list:
				num_pronouns += 1
		try:
			percentage = float(num_pronouns)/num_terms
		except:
			percentage = 0
		return percentage

	def _answer_stop_word_density(self, row):
		"""Percentage of tokens in the answer are stopwords
		Args:
		    row(pandas.dataframe): input row vector
		Return:
		    row(pandas.dataframe): ouput vector with new feature 
		"""
		stop = stopwords.words('english')
		answer = row.Answer 
		try:
			tokens = answer.split()
			num_tokens = len(tokens)
			stop_word_in_answer = [i for i in tokens if i in stop]
			num_stop_word_in_answer = len(stop_word_in_answer)
			row['ANSWER_STOPWORD_DENSITY'] = float(num_stop_in_answer)/num_tokens
			return row 
		except:
			row['ANSWER_STOPWORD_DENSITY'] = 0
			return row

	def _answer_end_with_quantifier(self, row):
		"""Answer ends with a quantifier word (many, few, etc, 1 true, 0 false
		Args:
		    row(pandas.dataframe): input row vector 
		Return:
		    row(pandas.dataframe): output vector with new feature
		"""
		answer = row.Answer
		try:
			tokens = answer.split()
			answer_end_token = tokens[-1]
			if answer_end_token in ling.QUANTIFIER_WORDS:
				row['ANSWER_ENDS_WITH_QUANTIFIER'] = 1
				return row
			else:
				row['ANSWER_ENDS_WITH_QUANTIFIER'] = 0
				return row
		except:
			row['ANSWER_ENDS_WITH_QUANTIFIER'] = 0
			return row

	def _answer_start_with_quantifier(self, row):
		"""Answer start with a quantifier word (many, few etc) 1 true, 0 false
		Args:
		    row(pandas.dataframe): input row vector 
		Return:
		    row(pandas.dataframe): output vector with new feature
		"""
		answer = row.Answer
		try:
			tokens = answer.split()
			answer_start_token = tokens[0]
			if answer_start_token in ling.QUANTIFIER_WORDS:
				row['ANSWER_STARTS_WITH_QUANTIFIER'] = 1
				return row 
			else:
				row['ANSWER_STARTS_WITH_QUANTIFIER'] = 0
				return row
		except:
			row['ANSWER_STARTS_WITH_QUANTIFIER'] = 0
			return row

	def _answer_quantifier_density(self, row):
		"""Percentage of tokens in the answer that are quantifier words
		Args:
		    row(pandas.dataframe): input pandas dataframe
		Return:
		    row(pandas.dataframe): result a pandas dataframe with new feature
		"""
		answer = row.Answer 
		try:
			tokens = answer.split()
			answer_len = len(tokens)
			quantifier_tokens = [i for i in tokens if i in ling.QUANTIFIER_WORDS]
			quantifier_tokens_len = len(quantifier_tokens)
			row['ANSWER_QUANTIFIER_DENSITY'] = float(quantifier_tokens_len)/answer_len
			return row 
		except:
			row['ANSWER_QUANTIFIER_DENSITY'] = 0
			return row

	def _percentage_capitalized_word_in_answer(self, row):
		"""Percentage of capitalized words in the sentence that are in the answer
		Args:
		    row(pandas.dataframe): input pandas dataframe
		Return:
		    row(pandas.dataframe): result a pandas dataframe with new feature
		"""
		answer = row.Answer
		sentence = row.Sentence 
		try:
			tokens = sentence.split()
			num_tokens = len(tokens)
			cap_tokens = [i for i in tokens if i.isupper()==True]
			cap_tokens_in_answer = [i for i in cap_tokens if i in answer]
			row['PERCENT_CAPITALIZED_WORDS_IN_ANSWER'] = float(len(cap_tokens_in_answer))/num_tokens
			return row 
		except:
			row['PERCENT_CAPITALIZED_WORDS_IN_ANSWER'] = 0
			return row

	def _percentage_pronoun_in_answer(self, row):
		"""Percentage of pronouns in the sentence that are in the answer
		Args:
		    row(pandas.dataframe): input pandas dataframe
		Return:
		    row(pandas.dataframe): result a pandas dataframe with new feature
		"""
		answer = row.Answer
		sentence = row.Sentence
		try:
			pronoun_in_sentence, sentence_len = self._identify_pronoun2(sentence)
			pronoun_in_sentence_in_answer = [i for i in pronoun_in_sentence if i in answer]
			num_pronoun_in_sentence_in_answer = len(pronoun_in_sentence_in_answer)
			row['PERCENT_PRONOMINALS_IN_ANSWER'] = float(num_pronoun_in_sentence_in_answer)/sentence_len
			return row 
		except:
			row['PERCENT_PRONOMINALS_IN_ANSWER'] = 0
			return row

	def _identify_pronoun2(self, sentence):
		"""Calculate percentage of pronouns in the sentence that are in the answer
		Args:
		    sentence(str): question sentence 
		Return:
		    pronoun_in_sentence(list): pronouns in sentence 
		    sentence_len(int): length of current sentence 
		"""
		text = nltk.word_tokenize(sentence)
		post = nltk.pos_tag(text)
		pronoun_list = ['PRP', 'PRP$', 'WP', 'WP$']
		pronoun_in_sentence = []
		sentence_len = len(post)
		for k, v in post:
			if v in pronoun_list:
				pronoun_in_sentence.append(k)
		return pronoun_in_sentence, sentence_len






	def build_feature(self, candidates):
		"""Build feature dataframe
		Args:
		    candidates(list): candidate question answer pairs
		Return:
		    df(pandas.dataframe): dataframe of question, answer, sentence and features
		"""
		df = pd.DataFrame(candidates)
		print df
		for idx, row in df.iterrows():
			row = self._num_token_in_answer(row)
			row = self._num_token_in_sentence(row)
			row = self._num_row_tokens_matching_in_out(row)
			row = self._percentage_token_in_answer(row)
			row = self._percentage_token_in_out_answer(row)
			row = self._answer_capitalized_word_density(row)
			row = self._answer_stop_word_density(row)
			row = self._answer_end_with_quantifier(row)
			row = self._answer_start_with_quantifier(row)
			row = self._answer_quantifier_density(row)
			row = self._percentage_capitalized_word_in_answer(row)
			row = self._percentage_pronoun_in_answer(row)
			print row

















