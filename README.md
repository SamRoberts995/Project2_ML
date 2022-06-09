# Project 2 
 - - -

* Data Cleanup & Model Training
- - -
  * We focused on the prices of Bitcoin, Ethereum, Ripple, Binance coin, Solana, Cardano, Polygon, Sandbox, Decentraland, Algorand
Used the Binance Python package with the Klines function to gather the close price for each coin and to convert the timestamp to DateTime format
Data retrieved every minute price change from the 6th Jun 2022 to the present, which gave us a sufficient data to train
  
  *Process:
retrieve tweets from data source
clean tweets and determine their individual sentiment polarity score
remove stopwords, retweets and tweets with a sentiment score of 0.0000
resample collected dataframe into 1 minute averages
Libraries Used:
Twitter Api
amount of data collected was not ideal
Snscrape
can scrape an unlimited amount of tweets in reverse chronological order (got 75000 raw tweets)
- - -
* Machine Learning Modle
 - - 
  * Random Forest Model - Uses ensemble learning method for regression. Ensemble learning method is a technique that combines predictions from multiple machine learning algorithms to make a more accurate prediction than a single model.
   - - -
  *Native Bayes Model - set of supervised learning algorithms based on applying Bayes’ theorem with the “naive” assumption of conditional independence between every pair of features given the value of the class variable.
  - - -
  *Logistic Regression Model - estimates the probability of an event occurring, such as voted or didn't vote, based on a given dataset of independent variables.
  - - -
  *Support Vector Model - find a hyperplane in an N-dimensional space(N — the number of features) that distinctly classifies the data points. 
  
* Discussion

  * After several promising tests our bot starting throwing runtime errors 
To show a proof of concept/minimum viable product we created an input/output interface to deliver exactly what the discord bot would have
Basic algorithm can be applied to virtually anything including discord bots and sagemaker chatbots


- - -
