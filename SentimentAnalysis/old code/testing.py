import matplotlib.pyplot as plt
import pandas as pd
import datetime
from textblob import TextBlob
from langdetect import detect


def prepare_data( companyDataAddress , outputCompanyDataAddress ):
	
	#Reading File
	print("Reading File....")
	sentimentDataset = pd.read_csv(companyDataAddress,encoding='utf-8',error_bad_lines=False,low_memory=False)
	print("Read File, Shape of File is:",sentimentDataset.shape)



	#Dropping Duplicates and taking only one tweet per minute to avoid bias of certain events
	sentimentDataset.rename(columns={"date":"DateTime"},inplace=True)
	print("Renamed date to DateTime")
	print("Dropping Duplicates....")
	sentimentDataset.drop_duplicates(subset=['text'],inplace=True)
	sentimentDataset.drop_duplicates(subset=['DateTime'],inplace=True)
	print("Dropped Duplicates.")
	print("Dropped Tweet Duplicates.")


	# Making a new column for grouping and Sorting according to DateTime
	
	print("Making New Columns  and Sorting Data....")
	sentimentDataset['DateTime'] = pd.to_datetime(sentimentDataset['DateTime'])
	sentimentDataset['Date'] = sentimentDataset['DateTime'].dt.date
	sentimentDataset.sort_values(by='DateTime',inplace=True)

	print("The Shape of the file now is:",sentimentDataset.shape)


	#Finding Sentiment and making a new column for polarity and language
	print("Finding Sentiment of tweets and making new Columns:")
	print(sentimentDataset.head)

	i = 0
	for text , date in zip(sentimentDataset['text'],sentimentDataset['Date']):
		
		try:
			# print(date)
			lang = detect(text)
			sentimentDataset.loc[i,'lang'] = lang

			analysis = TextBlob(text)
			polarity = analysis.sentiment[0]
			sentimentDataset.loc[i,'polarity'] = polarity

			# print("here")
			# print(sentimentDataset.loc[i,'polarity'])
			# print((polarity))

			if date.strftime("%A") == 'Saturday' or date.strftime("%A") == 'Sunday':
				# print(date.strftime("%A"))
				sentimentDataset.drop(i,inplace=True)


			if i % 100 is 0:
				print("On row: ",i)
				print(text)
				print("On:"+str(date)+"\tSentiment:"+str(sentimentDataset.loc[i,'polarity']))
				# print("On:"+str(date)+"\tSentiment:"+str(polarity))
				print("\n\n")

			i = i + 1

		except:
			i = i + 1
			continue
			
		
	print(sentimentDataset.head)

	# removing non-english tweets and writing to the output file
	sentimentDataset.set_index('Date',inplace=True)
	sentimentDataset.dropna()
	# print("Removing Non-English Tweets....")
	# sentimentDataset = sentimentDataset[sentimentDataset['lang'] == 'en']
	print(sentimentDataset)
	print("Dropping Datetime Column and lang column, Setting Date as index")
	sentimentDataset.drop(columns=['DateTime','lang'],inplace=True)
	sentimentDataset.drop_duplicates(subset=['text'],inplace=True)
	print(sentimentDataset)

	#Generating output
	print("Shape of Dataset Now is:",sentimentDataset.shape)
	print("Generating output file:...")
	sentimentDataset.to_csv(outputCompanyDataAddress, encoding='utf-8')
	print("Output File Generated at:",outputCompanyDataAddress)

	print(sentimentDataset)
	
def plot_all( sentimentDataset , DJIA ):
	# Grouping by date and finding its mean to get sentiment on a particular date
	sentimentPlotData = sentimentDataset.groupby(['Date'])['polarity'].mean()

	# Plotting
	plt.figure("PLOTS")
	
	# Subplot of DJIA
	plt.subplot(211)
	plt.plot(DJIA['Date'],DJIA['Z Score'])
	plt.xticks(rotation=90)
	plt.ylabel('Z Score')
	plt.legend(loc='best')
	plt.title('DJIA')

	# Subplot of Sentiment
	plt.subplot(212)
	plt.plot(sentimentPlotData)
	plt.xticks(rotation=90)
	plt.ylabel('Polarity')
	plt.legend(loc='best')
	plt.title('Sentiment')

	plt.show()



def write_z_scores(input_file,output_file):
	DJIA = pd.read_csv(input_file,low_memory=False,encoding='ISO-8859-1',error_bad_lines=False)	
	mu = DJIA['Adj Close'].mean()
	std = DJIA['Adj Close'].std()
	DJIA['Z Score'] = (DJIA['Adj Close'] - mu)/std
	DJIA['Date'] = pd.to_datetime(DJIA['Date'])

	DJIA.to_csv(output_file)

	return DJIA



def run():
	input_file = '../Datasets/DJIA/Accenture.csv'
	output_file = '../Datasets/DJIA/newAccenture.csv'

	# print("Making Z Score column in DJIA")
	# write_z_scores(input_file,output_file)
	DJIA = pd.read_csv(output_file, encoding='utf-8',error_bad_lines=False,low_memory=False)

	companyDataAddress = 'testing.csv'
	outputCompanyDataAddress = 'newTesting.csv'

	print("Preparing twitter data...")
	prepare_data(companyDataAddress = companyDataAddress , outputCompanyDataAddress = outputCompanyDataAddress)
	ds = pd.read_csv(outputCompanyDataAddress, encoding='utf-8',error_bad_lines=False,low_memory=False )

	print(ds)

	print("Plotting...")
	plot_all(ds,DJIA)


if __name__ == '__main__':
	run()