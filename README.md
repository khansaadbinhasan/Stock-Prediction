# Stock Prediction Of Popular Companies using Sentiment Analysis of Twitter
This model makes a plot between Z-Scores and Date, Two plots are made on same figure to get and idea of the correlation. DJIA data is used for Stock market and textblob is used for twitter sentiment analysis. 

This repository is a part of my Minor-Project at my college and part of my ongoing efforts to write a paper on Sentiment Analysis.

## Content
* Description
* Installation
* Usage
* Files and Folders
* How to get Data?

## Description

Running this file will create a graph that can be used to observe the effects of twitter sentiment on stock market.

## Installation
Download then extract the zip file or use ```git clone https://github.com/khansaadbinhasan/Stock-Prediction```                              
Download the Data From [this link](https://drive.google.com/open?id=1rrER_AEOgz7aHrqBxafxkZIgEHMfgdrP) or plug in your own and add it in `StockPrediction` Directory

`cd` to the git directory and run ```sudo -H pip3 install -r requirements.txt```

`cd` to `SentimentAnalysis` directory and change `configuring.py` according to your needs

## Usage
To run use: `python3 plotSent.py --company <company-name> --Zscale <z-scaling-factor> --threshold <subjectivity-threshold>`.

For example, for `Accenture` with `scaling-factor` of `5` and `subjectivity-threshold of 0.1` use:

`python3 plotSent.py --company Accenture --Zscale 5 --threshold 0.1`


## Files and Folders:
* __*plotSent.py*__: Main file containing the code for preprocessing and plotting.
* __*configuring.py*__: Containing parameters that you can configure according to your own settings.


## How to get Data?
For the time being data is available on this [drive link](https://drive.google.com/open?id=1rrER_AEOgz7aHrqBxafxkZIgEHMfgdrP), The Twitter data was downloaded using the [`GetOldTweets3` api](https://github.com/Mottl/GetOldTweets3) and the DJIA data was downloaded from [this website](https://finance.yahoo.com/quote/%5EDJI/history?p=%5EDJI)
