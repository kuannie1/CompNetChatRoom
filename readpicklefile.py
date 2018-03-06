import pickle

with open('data.pkl', 'rb') as f:
	messages = pickle.load(f)
print(messages)