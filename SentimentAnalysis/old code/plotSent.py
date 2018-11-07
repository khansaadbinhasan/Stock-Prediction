import matplotlib.pyplot as plt
import pandas as pd
import datetime
from textblob import TextBlob
from langdetect import detect
import numpy as np
import sys

def prepare_data( companyDataAddress , outputCompanyDataAddress ):
	
	#Reading File
	print("Reading File....")
	sentimentDataset = pd.read_csv(companyDataAddress,encoding='utf-8',error_bad_lines=False,low_memory=False,index_col=None)
	print("Read File, Shape of File is:",sentimentDataset.shape)

	print(sentimentDataset.head)

	#Dropping Duplicates and taking only one tweet per minute to avoid bias of certain events
	sentimentDataset.rename(columns={"date":"DateTime"},inplace=True)
	sentimentDataset = sentimentDataset[['DateTime','text']]
	print("Renamed date to DateTime")
	print("Dropping Duplicates....")
	sentimentDataset.drop_duplicates(subset=['text'],inplace=True)
	# sentimentDataset.drop_duplicates(subset=['DateTime'],inplace=True)
	print("Dropped Duplicates.")
	print("Dropped Tweet Duplicates.")


	# Making a new column for grouping and Sorting according to DateTime
	
	print("Making New Columns  and Sorting Data....")
	sentimentDataset['DateTime'] = pd.to_datetime(sentimentDataset['DateTime'])
	sentimentDataset['Date'] = sentimentDataset['DateTime'].dt.date
	sentimentDataset.sort_values(by='DateTime',inplace=True)
	sentimentDataset.reset_index()

	print("The Shape of the file now is:",sentimentDataset.shape)


	#Finding Sentiment and making a new column for polarity and language
	print("Finding Sentiment of tweets and making new Columns:")
	print(sentimentDataset.head)

	for index , rows in sentimentDataset.iterrows(): 	
		try:
			i = index
			text = rows['text']
			date = rows['Date']

			lang = detect(text)
			sentimentDataset.loc[i,'lang'] = lang

			analysis = TextBlob(text)
			polarity = analysis.sentiment[0]
			subjectivity = analysis.sentiment[1]
			sentimentDataset.loc[i,'polarity'] = polarity
			sentimentDataset.loc[i,'subjectivity'] = subjectivity

			day = date.strftime("%A")
			sentimentDataset.loc[i,'Day'] = day
			sentimentDataset.loc[i,'Date'] = date

			if i % 500 is 0:
				print("On row: ",i)
				print(text)
				print("\tSentiment:"+str(sentimentDataset.loc[i,'polarity']))
				print("Day is:",sentimentDataset.loc[i,'Day'],"on:",sentimentDataset.loc[i,'Date'])
				print("\n\n")

		except:
			continue

	sentimentDataset.sort_values(by='Date',inplace=True)

	# removing non-english tweets and writing to the output file
	sentimentDataset.dropna()
	print("Removing Non-English Tweets....")
	sentimentDataset = sentimentDataset[sentimentDataset['lang'] == 'en']
	sentimentDataset = sentimentDataset[sentimentDataset['subjectivity'] > 0.1 ]
	sentimentDataset = sentimentDataset[~( sentimentDataset['text'].str.contains('http') | sentimentDataset['text'].str.contains('https') )]
	# sentimentDataset = sentimentDataset[sentimentDataset['polarity'] != 0]
	sentimentDataset = sentimentDataset[sentimentDataset['Day'] != 'Sunday']
	sentimentDataset = sentimentDataset[sentimentDataset['Day'] != 'Saturday']
	# print(sentimentDataset)
	print("Dropping Datetime Column and lang column, Setting Date as index")
	sentimentDataset.set_index('Date',inplace=True)
	sentimentDataset.drop(columns=['DateTime'],inplace=True)
	sentimentDataset.drop_duplicates(subset=['text'],inplace=True)
	
	# Calculating Z-Scores
	mu = sentimentDataset['polarity'].mean()
	std = sentimentDataset['polarity'].std()

	sentimentDataset['Z Score'] = 5*(sentimentDataset['polarity'] - mu)/std

	#Generating output
	print("Shape of Dataset Now is:",sentimentDataset.shape)
	print("Generating output file:...")
	sentimentDataset.to_csv(outputCompanyDataAddress, encoding='utf-8')
	print("Output File Generated at:",outputCompanyDataAddress)


	# print(sentimentDataset['Day'] != 'Sunday')

	print(sentimentDataset)
	

def plot_all( company , sentimentDataset , DJIA ):
	# sentimentMean = sentimentDataset.groupby(['Date'])['polarity'].mean().to_frame()
	dateList = DJIA['Date']
	sentimentDataset = sentimentDataset[sentimentDataset['Date'].isin(dateList)]
	sentimentPlot = sentimentDataset.groupby(['Date'])['Z Score'].mean().to_frame()


	print(sentimentPlot)

	# Plotting
	plt.figure(company)

	plt.plot(DJIA['Date'],DJIA['Z Score'],sentimentPlot)
	plt.plot(sentimentPlot)

	plt.xticks(rotation=30)
	plt.ylabel('Z-Scores')
	plt.legend(['DJIA','Sentiment'],loc='best')
	plt.title('Sentiment and DJIA Z-Scores vs Date')

	plt.show()



def write_z_scores(input_file,output_file):
	DJIA = pd.read_csv(input_file,low_memory=False,encoding='ISO-8859-1',error_bad_lines=False)	
	mu = DJIA['Adj Close'].mean()
	std = DJIA['Adj Close'].std()
	DJIA['Z Score'] = (DJIA['Adj Close'] - mu)/std
	DJIA['Date'] = pd.to_datetime(DJIA['Date'])

	DJIA.to_csv(output_file,index=False)

	return DJIA


def run( company , doTwitterPreprocessing = True , doDJIAPreprocessing = True , PlotGraphs = True ):

	#DJIA 
	input_file = '../Datasets/DJIA/{}.csv'.format(company)
	output_file = '../Datasets/DJIA/new{}.csv'.format(company)

	if doDJIAPreprocessing == True:
		print("Preparing DJIA...")
		write_z_scores(input_file,output_file)
	
	DJIA = pd.read_csv(output_file, encoding='utf-8',error_bad_lines=False,low_memory=False)


	# Twitter preparing
	companyDataAddress = '../Datasets/Companies 2017/{}.csv'.format(company)
	outputCompanyDataAddress = '../Datasets/New Companies/{}.csv'.format(company)

	if doTwitterPreprocessing == True:
		print("Preparing twitter data...")
		prepare_data(companyDataAddress , outputCompanyDataAddress)
	
	ds = pd.read_csv(outputCompanyDataAddress, encoding='utf-8',error_bad_lines=False,low_memory=False )


	if PlotGraphs == True:
		print("Plotting...")
		plot_all(company,ds,DJIA)


if __name__ == '__main__':
	company = str(sys.argv[1])
	# print("Working on data for: ",company)
	run(company,doTwitterPreprocessing=True,doDJIAPreprocessing=True,PlotGraphs=True)
	# run(company,doTwitterPreprocessing=False,doDJIAPreprocessing=False,PlotGraphs=True)