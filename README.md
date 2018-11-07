# Stock Prediction Of Popular Companies using Sentiment Analysis of Twitter
This model makes a plot between Z-Scores and Date, Two plots are made on same figure to get and idea of the correlation. DJIA data is used for Stock market and textblob is used for twitter sentiment analysis. 

This repository is a part of my Minor-Project at my college and part of my ongoing efforts to write a paper on Sentiment Analysis.

## Description

Running this file will create a graph that can be used to observe the effects of twitter sentiment on stock market.

### Usage
To run use: ```python3 plotSent.py <company-name> <subjectivity-threshold> <scaling-factor>```.

For example, for `Accenture` with `scaling-factor` of `5` and `subjectivity-threshold of 0.1` use:

```python3 plotSent.py Accenture 0.1 5```




### Files and Folders:
* __*plotSent.py*__: Main file containing the code for preprocessing and plotting.

[link to Data](https://drive.google.com/open?id=1qx6us2Iv4E2_Ff8NZnNPrJ-nWGdcVulL)
