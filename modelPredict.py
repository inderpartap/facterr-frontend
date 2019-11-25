from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense, Flatten, LSTM, Conv1D, MaxPooling1D, Dropout, Activation
from keras.layers.embeddings import Embedding
import pickle
import pandas as pd
import tensorflow as tf


def classify(title,body):

	# with open ('data1row.txt', 'r') as file:
	# 	strdata = file.read().replace('\n', '')
	data = makewordembeddings(title,body)
	pred = makePredictions(data)
	result = []
	result.append('Fake')
	result.append(pred[0][0])
	if result[1] > 0.5:
		return result
	else:
		result[0] = 'Real'
		return result

def classify_single(body):
	data = makewordembeddings('title', body)
	pred = makePredictions(data)
	result = []
	result.append('Fake')
	result.append(pred[0][0])

	if result[1] > 0.5:
		response = {'category': result[0], 'status': 'ok', 'score': str(result[1]) }
	
	else:
		result[0] = 'Real'
		response = {'category': result[0], 'status': 'ok', 'score': str(result[1]) }
	# anything printed to the STDOUT will be stored in heroku's logs
	# print "TEXT: '{0}' :: RESPONSE : '{1}'" .format ( body.replace("\n", " ").replace("\r", " "), result)
	return response

def makewordembeddings(title,body):
	vocabulary_size = 2000
	with open('tokenizer.pickle', 'rb') as handle:
		tokenizer = pickle.load(handle)

	testDF = pd.DataFrame([body],columns=['text'])
	#title_sequences = tokenizer.texts_to_sequences(title)
	body_sequences = tokenizer.texts_to_sequences(testDF['text'])
	data = pad_sequences(body_sequences, maxlen=50)
	return data

def makePredictions(testdata):
	model_glove = tf.keras.models.load_model('fakenewsClassifier')
	pred = model_glove.predict(testdata)
	return pred


if __name__ == '__main__':
	classify(title,body)


