import matplotlib.pyplot as plt
import regex as re
import pandas as pd
import datetime
import numpy as np
import sys , getopt
import traceback
import time
import yaml

from textblob import TextBlob
from langdetect import detect
from statsmodels.tsa.stattools import grangercausalitytests

########Use this only when you have put the stattoolsMod.py file in /lib/python3.6/site-packages/statsmodels/tsa#########
# from statsmodels.tsa.stattoolsMod import grangercausalitytests 

def configurables(TwitterIntermediate, TwitterOutput, threshold=0.1, ZScaling=7.5):
	"""
		input: Addresses to twitter files and configurables
		
		calculates Z-Scores for twitter data and makes the final .csv file
	
		returns: none
	"""	

	sentimentDataset = pd.read_csv(TwitterIntermediate,encoding='ISO-8859-1',error_bad_lines=False,low_memory=False,index_col=None)
	sentimentDataset = sentimentDataset[sentimentDataset['subjectivity'] >= threshold ]

	# Calculating Z-Scores
	mu = sentimentDataset['polarity'].mean()
	std = sentimentDataset['polarity'].std()

	sentimentDataset['Z Score'] = ZScaling*(sentimentDataset['polarity'] - mu)/std
	
	sentimentDataset.to_csv(TwitterOutput, encoding='utf-8',index=False)
	print("Output File Generated at:",TwitterOutput)


def prepare_data(TwitterInput, TwitterIntermediate):
	"""
	input:    TwitterInput: path to input database
			  TwitterIntermediate: path to intermediate database to be created

	Adds columns for language, polarity, subjectivity and Day, Does preprocessing and remove non-english or null tweets

	returns:  nothing  		
	"""


	#Reading File
	sentimentDataset = pd.read_csv(TwitterInput,encoding='utf-8',error_bad_lines=False,index_col=None,engine='python')

	# Making a new column for grouping and Sorting according to DateTime and add columns for language, polarity, subjectivity and day
	sentimentDataset['date'] = pd.to_datetime(sentimentDataset['date'])
	sentimentDataset['Date'] = sentimentDataset['date'].dt.date
	sentimentDataset = pd.concat([sentimentDataset,pd.DataFrame(columns=list(['lang', 'polarity', 'subjectivity', 'Day']))],axis=1, verify_integrity = True)
	sentimentDataset.reset_index()

	print("The Shape of the Database is:",sentimentDataset.shape)
	print(sentimentDataset.head)

	#Finding Sentiment and making a new column for polarity and language
	for index , rows in sentimentDataset.iterrows(): 	
		try:
			text = rows['text']
			date = rows['Date']

			text = preprocess_tweet(text)
			lang = detect(text)
			polarity, subjectivity = TextBlob(text).sentiment
			day = date.strftime("%A")

			sentimentDataset.loc[index,['lang', 'polarity', 'subjectivity', 'text', 'Day', 'Date']] = lang, polarity, subjectivity, text, day, date

			if index % 500 is 0:
				print("On row: ",index)
				print(text)
				print("Sentiment:\tPolarity:"+str(sentimentDataset.loc[index,'polarity'])+"\tSubjectivity:"+str(sentimentDataset.loc[index,'subjectivity']))
				print("Day is:",sentimentDataset.loc[index,'Day'],"on:",sentimentDataset.loc[index,'Date'])
				end = time.time()
				print("Time passed since starting:"+str(round(end-start))+"s")
				print("\n"*2)

		except Exception as e:
			traceback.print_exc()
			print("\n"*2)
			print("Something is wrong see above error for more details.")
			print("Action:Ignoring this row and continuing.")
			continue


	# Sort values according to date and drop unnecessary columns and duplicate rows 
	sentimentDataset.sort_values(by='Date',inplace=True)
	sentimentDataset = sentimentDataset[['Date','Day','text','lang','polarity','subjectivity']]
	sentimentDataset.drop_duplicates(subset=['text'],inplace=True)

	# removing non-english tweets and writing to the output file
	sentimentDataset.dropna(inplace=True)
	sentimentDataset = sentimentDataset[sentimentDataset['lang'] == 'en']
	sentimentDataset.set_index('Date',inplace=True)
	
	#Generating output
	print("Shape of Dataset Now is:",sentimentDataset.shape)
	sentimentDataset.to_csv(TwitterIntermediate, encoding='utf-8')
	print("intermediate File Generated at:",TwitterIntermediate)

	print(sentimentDataset)
	

def preprocess_tweet(tweetText):
	"""
		input: A Tweet

		Replaces username with USERNAME token and url with URL token
		Remove #, comma, full stop, digits, multiple alphabets in a word like woooooow to woow, multiple spaces

		returns: Processed tweet
	"""

	preprocessingTweet = re.sub( r'@([A-Za-z0-9_]+)' , "USERNAME" , tweetText )
	preprocessingTweet = re.sub( r"http\S+", 'URL' , preprocessingTweet )
	preprocessingTweet = re.sub( r"#" , '' , preprocessingTweet )
	preprocessingTweet = re.sub(r'[^\w\s]',' ',preprocessingTweet)
	preprocessingTweet = re.sub(r'(.)\1+', r'\1\1', preprocessingTweet)
	preprocessingTweet = re.sub(r'[0-9]+', '' , preprocessingTweet)
	preprocessingTweet = re.sub( r":([a-z0-9A-Z_]+)" , '' , preprocessingTweet )
	preprocessingTweet = re.sub(r"\b[pDo]\b", "", preprocessingTweet)
	preprocessingTweet = re.sub(r' +',' ',preprocessingTweet)

	preprocessedTweet = preprocessingTweet

	return preprocessedTweet


def plot_all( company , sentimentDataset , DJIA ):
	"""
		input: DJIA and twitter files 

		makes the plot

		returns: modified twitter dataframe
	"""

	DJIAdateList = DJIA['Date']
	sentimentDataset = sentimentDataset[sentimentDataset['Date'].isin(DJIAdateList)]
	sentimentPlot = sentimentDataset.groupby(['Date'])['Z Score'].mean().to_frame()


	print(sentimentPlot)

	# Plotting
	plt.figure(company)
	plt.plot(DJIA['Date'],DJIA['Z Score'],sentimentPlot)

	plt.xticks(rotation=30)
	plt.ylabel('Z-Scores')
	plt.legend(['DJIA','Sentiment'],loc='best')
	plt.title('Sentiment and DJIA Z-Scores vs Date')

	plt.show()

	return sentimentPlot

def write_DJIA_Z_scores(DJIAinput,DJIAoutput):
	"""
		input: address of files

		calculates Z-Scores for Adjusted Closing price of DJIA

		returns: DJIA dataframe
	"""

	DJIA = pd.read_csv( DJIAinput , low_memory = False , encoding = 'ISO-8859-1' , error_bad_lines = False , index_col = None )	
	mu = DJIA['Adj Close'].mean()
	std = DJIA['Adj Close'].std()
	DJIA['Z Score'] = (DJIA['Adj Close'] - mu)/std
	DJIA['Date'] = pd.to_datetime(DJIA['Date'])

	DJIA.to_csv(DJIAoutput,index=False)

	return DJIA


def run( configure , company = 'Accenture' , doTwitterPreprocessing = True , doDJIAPreprocessing = True , PlotGraphs = True ):
	"""
		input: Address of files

		runs functions according to parameters given by user in yaml file
		
		returns: none 
	"""

	#DJIA files
	DJIAinput = configure['inputFileDJIA'].format(company)
	DJIAoutput = configure['outputFileDJIA'].format(company)

	if doDJIAPreprocessing == True:
		print("Preparing DJIA...")
		write_DJIA_Z_scores(DJIAinput,DJIAoutput)
	
	DJIA = pd.read_csv( DJIAoutput, encoding = 'utf-8' , error_bad_lines = False , low_memory = False , index_col = None )


	# Twitter files
	TwitterInput = configure['inputFileTwitter'].format(company)
	TwitterIntermediate = configure['intermediateFileTwitter'].format(company)
	TwitterOutput = configure['outputFileTwitter'].format(company)


	if doTwitterPreprocessing == True:
		print("Preparing twitter data...")
		prepare_data(TwitterInput , TwitterIntermediate)

	
	if PlotGraphs == True:
		print("Plotting...")
		threshold , ZScaling = configure['threshold'] , configure['ZScaling']
		configurables(TwitterIntermediate,TwitterOutput,threshold,ZScaling)
		sentimentDataset = pd.read_csv( TwitterOutput , encoding = 'utf-8' , error_bad_lines = False , low_memory = False , index_col = None )
		sentimentPlot = plot_all(company,sentimentDataset,DJIA)

	# Granger Causality
	x1 = np.asarray(DJIA['Z Score'])[1:].reshape(19,1)#[1:] will not be needed if data is correct
	x2 = np.asarray(sentimentPlot['Z Score']).reshape(19,1)
	x = np.concatenate((x1,x2),axis=1)
	maxlag = 5

	grangercausalitytests(x, maxlag, addconst=True, verbose=True )

	########Use this only when you have put the stattoolsMod.py file in /lib/python3.6/site-packages/statsmodels/tsa#######
	# grangercausalitytests(x, maxlag, addconst=True, verbose=True, saveto=grangerResultsPath )



def main(argv):
	"""
		input: arguments from the command line
		
		processes command line input and takes input from yaml file and pass it to run function

		returns: none
	"""

	with open("../configure.yaml", "r") as file_descriptor:
		configure = yaml.load(file_descriptor)

	try:
		opts, args = getopt.getopt(argv, "", ("company=", "Zscale=", "threshold="))
		
	except getopt.GetoptError:
		traceback.print_exc()
		print("\n"*2)
		print("Something is wrong see above error for more details.")
		print("Action: exiting. Please make sure command is correct.")
		print('plotSent.py --company <company-name> --Zscale <z-scaling-factor> --threshold <subjectivity-threshold>')
		sys.exit(2)


	for opt, arg in opts:
		if opt == '--h' or opt == '-h':
			print('python3 plotSent.py --company <company-name> --Zscale <z-scaling-factor> --threshold <subjectivity-threshold>')
			sys.exit()
		elif opt == "--company":
			company = arg
		elif opt == "--Zscale":
			configure['ZScaling'] = float(arg)
		elif opt == "--threshold":
			configure['threshold'] = float(arg)

	try:
		run(configure=configure,company=company,doTwitterPreprocessing=configure['doTwitterPreprocessing'],doDJIAPreprocessing=configure['doDJIAPreprocessing'],PlotGraphs=configure['PlotGraphs'])

	except Exception as e:
		traceback.print_exc()
		print('\n'*2)
		print("Something is wrong see above error for more details.")
		print("Action:Running with default parameters.")
		print("Company: ",'Accenture')
		print("ZScaling: ",configure['ZScaling'])
		print("threshold: ",configure['threshold'])
		
		try:
			run(configure=configure,doTwitterPreprocessing=configure['doTwitterPreprocessing'],doDJIAPreprocessing=configure['doDJIAPreprocessing'],PlotGraphs=configure['PlotGraphs'])
		
		except Exception as e:
			traceback.print_exc()
			sys.exit(3)


if __name__ == '__main__':
	start = time.time()
	main(sys.argv[1:])