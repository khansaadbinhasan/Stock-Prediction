# Stock Prediction Of Popular Companies using Sentiment Analysis of Twitter
This model makes a plot between Z-Scores of DJIA & Twitter Sentiment Polarity and Date, Two plots are made on same figure to get an idea of the correlation. Historical DJIA data is used for Plotting Stock market Z-Scores and textblob is used for Twitter Sentiment Analysis. 

This repository is a part of my Minor-Project at my college and part of my ongoing efforts to write a paper on Sentiment Analysis.

## Content
* [__Details__](#details)
* [__Installation__](#installation)
* [__Usage__](#usage)
* [__Files and Folders__](#files-and-folders)
* [__How to get Data?__](#how-to-get-data)

## Details
The Concept behind this project is very simple, Quantify peoples' Sentiment about a certain company, Are they thinking positive about a company or negative, The idea is people talk about companies on twitter, when they talk positive then a positive air around the company is generated and people are likely to invest more in that company resulting in better stock prices, Or if company does something unpopular then it will have a negative sentiment among people and its stock will plummet.
For Stock Market we took `DJIA historical Data`([What is DJIA?](https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average)), Found the `Z-Scores`([What is Z-Score](https://en.wikipedia.org/wiki/Standard_score)) for the `Adjusted Closing Price` and plotted it with date on X-axis. For Twitter Data, we took tweets and then passed them through `textblob`([What is textblob](https://textblob.readthedocs.io/en/dev/)), thus getting values for their [polarity and subjectivity](https://textblob.readthedocs.io/en/dev/quickstart.html#sentiment-analysis), We then found the `Z-Scores` of `Polarity` on each day and filtered them according to `subjectivity`(hence `subjectivity threshold`) and plotted them alongside `DJIA` data. Since, we needed comparable graphs a `scaling factor` is incorporated which can be tuned to give more comparable graphs.
For more detailed discussion please read the accompanying [Blog](link to blog)

## Installation
Download then extract the zip file or use:
```bash
git clone https://github.com/khansaadbinhasan/Stock-Prediction
```                              
Download the Data From [this link](https://drive.google.com/open?id=1rrER_AEOgz7aHrqBxafxkZIgEHMfgdrP) or plug in your own and add it in `StockPrediction` Directory

`cd` to the git directory and run 
```bash
sudo -H pip3 install -r requirements.txt
```

`cd` to `SentimentAnalysis` directory and change `configuring.py` according to your needs.


## Usage
To run use: 
```bash
python3 plotSent.py --company <company-name> --Zscale <z-scaling-factor> --threshold <subjectivity-threshold>
```

For example, for `Accenture` with `scaling-factor` of `5` and `subjectivity-threshold of 0.1` use:

```bash
python3 plotSent.py --company Accenture --Zscale 5 --threshold 0.1
```

## Files and Folders:
* __*plotSent.py*__: Main file containing the code for preprocessing and plotting, Unless you need to do any changes to existing code you will not have to open it, use `configuring.py` to configure the parameters and use command line for tuning other parameters.
* __*configuring.py*__: Containing parameters that you can configure as per your needs. The configurable parameters in this file are:

__inputFileDJIA__(*string*): The address to the raw input Data for DJIA obtained from [this website](https://finance.yahoo.com/quote/%5EDJI/history?p=%5EDJI)
__outputFileDJIA__(*string*): The address to the output Data of DJIA generated after preprocessing, and is used to generate the DJIA plots.

__inputFileTwitter__(*string*): The address to the raw input Data for Twitter obtained from [`GetOldTweets3` api](https://github.com/Mottl/GetOldTweets3)
__intermediateFileTwitter__(*string*): The address to the intermediate Data file obtained after processing `inputFileTwitter`.
__outputFileTwitter__(*string*):The address to the output Data of Twitter generated after complete preprocessing, and is used to generate the Twitter Sentiment plots.

__doTwitterPreprocessing__(*boolean*): Twitter Data Preprocessing is a computation intensive task, and you have to only do it once, so set This to `True` only the first time and once you are done, set this to `False` so you only generate plots without unnecessary preprocessing.

__doDJIAPreprocessing__(*boolean*): Set this to `True` only the first time and then set this to `False`.	

__PlotGraphs__(*boolean*): If you want to build the graph set this to `True` or If you want to just do the Preprocessing set this to `False`  

## How to get Data?
For the time being data is available on this [drive link](https://drive.google.com/open?id=1rrER_AEOgz7aHrqBxafxkZIgEHMfgdrP), The Twitter data was downloaded using the [`GetOldTweets3` api](https://github.com/Mottl/GetOldTweets3) and the DJIA data was downloaded from [this website](https://finance.yahoo.com/quote/%5EDJI/history?p=%5EDJI)
