import pandas as pd
from textblob.classifiers import NaiveBayesClassifier

inputAddress = 'training.1600000.processed.noemoticon.csv1.csv'
outputAddress = 'sent140.csv'

# sent140 = pd.read_csv(inputAddress,encoding='ISO-8859-1',error_bad_lines=False,low_memory=False,names= ['target', 'ids', 'date', 'flag', 'user', 'text','sentiment'])
# print(sent140.head)

# sent_new = sent140[['text', 'target','sentiment']]

# print(sent140.head)
# sent_new.to_csv(outputAddress, encoding='ISO-8859-1')

newAddress = 'sentiment.csv'

# sent_new = pd.read_csv(outputAddress,encoding='ISO-8859-1',error_bad_lines=False,low_memory=False)
# sent_new.loc[sent_new['target']==0,'sentiment'] = 'neg'
# sent_new.loc[sent_new['target']==4,'sentiment'] = 'pos'
# sent_new = sent_new[['text','sentiment']]	
# sent_new.to_csv(newAddress, encoding='ISO-8859-1',index=False)

print("here")

with open(newAddress, 'r') as fp:
	cl = NaiveBayesClassifier(fp, format="csv")

print("here")


sent_new.reset_index()	
sent_new = sent_new[sent_new.index<10000 && sent_new.index > 800000 && sent_new.index < 810000]