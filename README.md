# TwitterCrawler for Sentiment Analysis

This project regards the Web Science Coursework assignment at the University Of Glasgow level M

```
Author: Odysseas Polycarpou
GUID: 2210049p
 ```
We have created a Twitter Crawler which can fetch tweets based on emotion and process them to identify the new sentiment label and assign it on the tweet. Then based on the data fetched from Twitter we carry out a sentiment analysis for emotion labelling accuracy.

For this assignment we have used:

- TwitterAPI for fetching tweets
- MongDBCompass for storing data
- Word2Vec mode for tokenizing and processing data

# Intructions for running

The first thing to do is set up the environment with all the necessary libraries and modules that are needed to run the crawler. To do so, open an Anaconda prompt and navigate to the directory where you have saved the repository. Then run the following to create the environment:


```bash
$ conda env create -f environment.ym
```

Then run the following to activate the "web-science" environment you have just created:


```bash
$ conda activate web-science
```

Once you have set up the environment, you can now go ahead and execute the main body of the software. Before executing however, open the ```tweetStreamer.py``` from the main source folder of repository and set up your Tweeter Keys here:

```python
#===============Set your KEYS and TOKENS here==================#
CONSUMER_KEY = ""
CONSUMER_KEY_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""
#==============================================================#
```

Save and close.

Now execute the following modules in the order specified below to fetch, process and analyse the tweets. Please keep the console open to monitor the output. Also please note that the mongoDB Compass uses a local storage database to keep the collections. The credentials are already defined in ```connect_to_mongo()``` function.

```bash
$ python MainTweetCrawler.py

$ python MainTweetProcessor.py

$ python MainTweetCrawler.py

$ python createDataFrame.py

$ python DatabaseStatistics.py

$ python Analysis.py
```

The process will generate results in the results folder. The pre and post processed tweets are also saves as .csv files in the data folder and all can be examined there
