# Stock Prediction Of Popular Companies using Sentiment Analysis of Twitter
This model makes a plot between Z-Scores of DJIA & Twitter Sentiment Polarity and Date, Two plots are made on same figure to get an idea of the correlation. Historical DJIA data is used for Plotting Stock market Z-Scores and textblob is used for Twitter Sentiment Analysis. 

This repository is a part of my Minor-Project at my college and part of my ongoing efforts to write a paper on Sentiment Analysis.

## Content
* __Details__
* __Installation__
* __Usage__
* __Files and Folders__
* __How to get Data?__

## Details

Running this file will create a Plot that can be used to observe the effects of Twitter Sentiment on American Stock Market.

## Terms and Concept


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

*inputFileDJIA*:(String)The address to the raw input Data for DJIA obtained from [this website](https://finance.yahoo.com/quote/%5EDJI/history?p=%5EDJI)
*outputFileDJIA*:(String)The address to the output Data of DJIA generated after preprocessing, and is used to generate the DJIA plots.

*inputFileTwitter*:(String)The address to the raw input Data for Twitter obtained from [`GetOldTweets3` api](https://github.com/Mottl/GetOldTweets3)
*intermediateFileTwitter*:(String)The address to the intermediate Data file obtained after processing `inputFileTwitter`.
*outputFileTwitter*:(String)The address to the output Data of Twitter generated after complete preprocessing, and is used to generate the Twitter Sentiment plots.

*doTwitterPreprocessing*:(Boolean)Twitter Data Preprocessing is a computation intensive task, and you have to only do it once, so set This to `True` only the first time and once you are done, set this to `False` so you only generate plots without unnecessary preprocessing.
*doDJIAPreprocessing*:(Boolean) Set this to `True` only the first time and then set this to `False`.	

*PlotGraphs*:(Boolean) If you want to build the graph set this to `True` or If you want to just do the Preprocessing set this to `False`  

## How to get Data?
For the time being data is available on this [drive link](https://drive.google.com/open?id=1rrER_AEOgz7aHrqBxafxkZIgEHMfgdrP), The Twitter data was downloaded using the [`GetOldTweets3` api](https://github.com/Mottl/GetOldTweets3) and the DJIA data was downloaded from [this website](https://finance.yahoo.com/quote/%5EDJI/history?p=%5EDJI)
