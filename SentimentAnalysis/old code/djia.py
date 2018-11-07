import matplotlib.pyplot as plt 
import datetime
import pandas as pd

def write_z_scores(input_file,output_file):
	DJIA = pd.read_csv(input_file,low_memory=False,encoding='ISO-8859-1',error_bad_lines=False)	
	mu = DJIA['Adj Close'].mean()
	std = DJIA['Adj Close'].std()
	DJIA['Z Score'] = (DJIA['Adj Close'] - mu)/std
	DJIA['Date'] = pd.to_datetime(DJIA['Date'])

	DJIA.to_csv(output_file)

	return DJIA


def DJIA_plot(DJIA):
	# plt.plot(DJIA['Date'],DJIA['Adj Close'])
	# plt.figure()
	plt.plot(DJIA['Date'],DJIA['Z Score'])
	plt.show()


if __name__ == '__main__':
	
	input_file = '../Datasets/DJIA/facebook.csv'
	output_file = '../Datasets/DJIA/newfacebook.csv'

	DJIA = write_z_scores(input_file,output_file)
	DJIA_plot(DJIA)