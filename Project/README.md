# The power of 140 characters


## Abstract
As presidents lead their nation, we believe their actions could set an example and influence and encourage certain behaviors. We will investigate if there is a possible correlation between sentiment conveyed by such figures via social media and negative social behavior of a nation.

The presidency of Donald Trump has been marked with many controversies, including the rise of supremacist groups and numerous nation wide conflicts. By using Trump tweets, we would explore if there is a significant temporal correlation between sentiment expressed in the Tweet and the number of conflicts in the nation using GDELT dataset. To reduce the bias of such analysis, we would perform the same analysis with social media activity of his predecessor and compare the results, as well as adding the social-economic aspects which may affect such behaviors.

What is the power of a presidential tweet? We hope that we will have more insight on the answer of this question and raise awareness on the impact 140 characters can make.

## Research questions
* Do violent events or crimes occur more frequently after presidential tweets?
* Is the correlation higher with negative sentiment of the tweet?
* Does a significant difference exists between such correlation with Trump and Obama presidency?
* Is there a difference in sentiment expressed in tweets before and after Trump becoming a presidential candidate?
* How do social-economical aspects influence the correlation?
* Does the political regiment affect such negative behavior on a larger scale?

## Dataset

### Trump tweets
* Downloading the complete dataset locally and processing the JSON files
* We would use mainly the timestamps and tweet content for our analysis:
  * timestamps for temporal correlation with events
  * tweet content for sentiment analysis
* We could follow the impact of tweet by analyzing:
  * number of retweets
  * number of favorites
  * number of followers
### GDELT
* We would use GDELT Global Knowledge graph to gain insights on events:
  * geolocalized to USA
  * in specified timeframe, starting from 2013
  * specific events, such as protests or violent manifestations
  * will need knowledge on working on the cluster and accessing the data
### Wikidata
* Obtaining data for social-economical indicators:
  * for a specific period of time
  * for a specific region of the USA
  * data wrangling and processing

### Obama tweets *
Available at: http://obamawhitehouse.gov.archivesocial.com/

* It would enrich our analysis by providing an insight in differences between the two leaders
* We strive for a more complete and less biased analysis


## A list of internal milestones up until project milestone 2
* Learning how to process big data with frameworks such as Hadoop and Spark
* Getting to know the datasets in finer detail
* Discussing possible factors which may bias our conclusions
* Tweets wrangling and analysis

## Questions for TAa
- General feasability of this project?
- Should we generalize more and how far should we go?
- Are Tweets strong enough to make such statement and conclusion?
