def mentions_hashtags_in_period(tweets, from_date, to_date):
    '''
    A function to retrieve all mentions and hashtags from the tweets between specified dates.
    
    Parameters:
    tweets -- Twitter API based dataframe
    from_date -- starting date to consider (valid string or pandas timestamp)
    to_date -- ending date to consider (valid string or pandas timestamp)
    
    Returns:
    mentions -- python list of mentions entity objects
    hashtags -- python list of hashtags entity objects
    '''
    tweets_in_period = tweets.loc[(tweets.created_at>=pd.Timestamp(from_date)) & (tweets.created_at<=pd.Timestamp(to_date))]
    
    mentions = []
    hashtags = []
    
    for idx, tweet in tweets_in_period.iterrows():
        for mention in tweet.entities['user_mentions']:
            mentions.append(mention)
        
        for hashtag in tweet.entities['hashtags']:
            hashtags.append(hashtag)
    
    return mentions, hashtags


def find_news_with_topics(news, topic_list):
    '''
    Function for retrieving all the news that contain any of the topics specified in the list.
    
    Parameters:
    news -- news dataset dataframe
    topic_list -- python list of strings specifying topics
    
    Returns:
    ret_list -- python list containing rows of news dataframe
    '''
    ret_list = []
    
    for topic in topic_list:
        for idx, row in news.iterrows():
            if(topic in row['Topic List'].split(',')):
                ret_list.append(row)
                
    return ret_list


def find_news_with_topics_timeframe(news, topic_list, from_date, to_date):
    '''
    Function for retrieving all the news that contain any of the topics specified in the list, in the given timeframe.
    
    Parameters:
    news -- news dataset dataframe
    topic_list -- python list of strings specifying topics
    from_date -- starting date to consider (valid string or pandas timestamp)
    to_date -- ending date to consider (valid string or pandas timestamp)
    
    Returns:
    ret_list -- python list containing rows of news dataframe
    '''
    news_timeframe = news.loc[(news['Date of Airing (EST)']>=pd.Timestamp(from_date)) & (news['Date of Airing (EST)']<=pd.Timestamp(to_date))]
    
    return find_news_with_topics(news_timeframe, topic_list)


def get_tweets_mentions_hashtags(tweets, mentions, hashtags, text_parts):
    '''
    Function to get tweets with any of the names in the list of mentions, any of the names in hashtags and
    any of the text in textual parts of the tweet.
    
    Parameters:
    tweets -- Twitter API based dataframe
    mentions -- python list of strings of screen names to match
    hashtags -- python list of strings of hashtag texts to match
    text_parts -- python list of strings of part of tweet text to match
    
    Returns:
    ret_list -- python list of tweets dataframe rows satisfying any of the conditions
    '''
    ret_list = []
    
    for idx, tweet in tweets.iterrows():
        check = False
        for t in tweet.entities['hashtags']:
            if(t['text'] in hashtags):
                check = True
                break
        
        for t in tweet.entities['user_mentions']:
            if(t['screen_name'] in mentions):
                check = True
                break
        
        for t in text_parts:
            if(type(tweet.text)==str):
                if(t in tweet.text.lower()):
                    check = True
            else:
                if(t in tweet.full_text.lower()):
                    check = True
        
        if(check):
            ret_list.append(tweet)
    
    return ret_list    


def get_topics_tweet(extracted_tweets, news, days_delta):
    '''
    Function for finding the topics in the news in the date around the creation date of a tweet, 
    in a given timeframe of specified number of days.
    
    Parameters:
    extracted_tweets -- python list of Twitter API dataframe rows
    news -- dataframe of news
    days_delta -- maximum number of days to consider after the creation of the tweet 
    
    Returns:
    topics_tweet -- python list of string
    '''
    topics_tweet = []

    for et in extracted_tweets:
        start_date = et.created_at# - pd.Timedelta(days=days_delta) - be strict to have more confidence in results
        end_date = et.created_at + pd.Timedelta(days=days_delta)
        topics_tweet.append(get_topics_in_period(news, start_date, end_date))
        
    return topics_tweet


def get_news_topics_for_tweet_topics(news, tweets, mentions, hashtags, text_parts, max_days_apart):
    '''
    Gets topics from the news in the date around when tweets were published, +- max_days apart.
    We filter all the tweets to select by providing lists of mentions, hashtags or parts of text to contain.
    
    Parameters:
    news -- news dataframe
    tweets -- tweets dataframe
    mentions -- python list of strings
    hashtags -- python list of strings
    text_parts -- python list of strings
    max_days_apart -- integer
    
    Returns:
    aggregated_df -- returns a dataframe with aggregated topics and their counts summed
    selected_tweets -- python list of dataframe rows containing selected tweets with the given criteria
    '''
    selected_tweets = get_tweets_mentions_hashtags(tweets, mentions, hashtags, text_parts)
    
    topics = get_topics_tweet(selected_tweets, news, max_days_apart)
    
    topics_df = pd.DataFrame()
    
    for topic in topics:
        topics_df = topics_df.append(topic)
        
    aggregated_df = topics_df.groupby('topic').aggregate('sum').sort_values('count', ascending=False)
    
    return aggregated_df, selected_tweets


def find_start_end_date(tweets):
    '''
    Helper function for finding the earliest and latest date of creation in list of tweets.
    
    Parameters:
    tweets -- python list of tweets (tweets dataframe rows)
    
    Returns:
    date_min -- pandas timestamp, earliest date among tweets
    date_max -- pandas timestamp, latest date among tweets
    '''
    date_min = tweets[0].created_at
    date_max = tweets[0].created_at
    
    for t in tweets:
        if(t.created_at<date_min):
            date_min = t.created_at
        if(t.created_at>date_max):
            date_max = t.created_at
            
    return date_min, date_max


def normalize_df(df):
    '''
    Function for normalization of dataframe counts - obtaining the percentage (ratios).
    
    Parameter:
    df -- dataframe with column named 'count' to obtain the ratios expressed as percentage
    
    Returns:
    ret_df -- dataframe with column named 'count' expressed as ratios in percentage
    '''
    s = df['count'].sum()
    
    ret_df = df.copy()
    
    ret_df['count'] = ret_df['count']/s*100
    
    return ret_df


def get_topics_percentage(topics):
    '''
    Helper function for getting the counts of topics as percentages.
    '''
    tmp = topics.groupby('topic').sum().sort_values(by='count',ascending=False)
    s= float(tmp['count'].sum())
    tmp['count'] = tmp['count']/s*100
    return tmp


def get_topic_count(topics):
    '''
    Helper function for getting the counts for topics.
    '''
    tmp = topics.groupby('topic').sum().sort_values(by='count',ascending=False)
    return tmp


def check_increase_in_mentions(general_topics, news_percentage):
    '''
    Function for obtaining the multiplier between the general topics in tweets and the topics provided from the news.
    '''
    tmp = general_topics.join(news_percentage, lsuffix='_topics', rsuffix='_tweets')
    
    tmp['multiplier'] = tmp['count_tweets']/tmp['count_topics']
    
    return tmp.sort_values(by=['multiplier'], ascending=False)


def check_delta_in_mentions(general_topics, news_percentage):
    '''
    Function for obtaining the difference between the general topics in tweets and the topics provided from the news.
    '''
    tmp = general_topics.join(news_percentage, lsuffix='_topics', rsuffix='_tweets')
    
    tmp['delta'] = tmp['count_tweets']-tmp['count_topics']
    tmp['ratio'] = tmp['count_tweets']/tmp['count_topics']
    
    return tmp.sort_values(by=['ratio','delta'], ascending=False)


def extract_hashtags_tweets(df):
    '''
    Helper function for extracting the hashtag text with counts from the dataframe, returning a combined dataframe.
    '''
    ret_ht = {}
    
    for idx, row in df.iterrows():
        for ht in row['hashtags']:
            if(ht['text'] in ret_ht):
                ret_ht[ht['text']] += 1
            else:
                ret_ht[ht['text']] = 1
    
    df = pd.DataFrame.from_dict(ret_ht, orient='index')
    df.columns = ['count']
    
    return df.sort_values(by=['count'],ascending=False)


def extract_mentions_tweets(df):
    '''
    Helper function for extracting the hashtag text with counts from the dataframe, returning a combined dataframe.
    '''
    ret_ht = {}
    
    for idx, row in df.iterrows():
        for ht in row['mentions']:
            if(ht['screen_name'] in ret_ht):
                ret_ht[ht['screen_name']] += 1
            else:
                ret_ht[ht['screen_name']] = 1
    
    df = pd.DataFrame.from_dict(ret_ht, orient='index')
    df.columns = ['count']
    
    return df.sort_values(by=['count'],ascending=False)


def get_news_with_topics(news, topics):
    '''
    Function used to obtain all the news containing at least one of the specified topics.
    
    Parameters:
    news -- news dataframe
    topics -- python list of strings, each string is a topic name
    
    Returns:
    n -- python list, news dataframe rows
    '''
    n = []
    
    for t in topics:
        for idx, row in news.iterrows():
            if(t in row['Topic List'].split(',')):
                n.append(row)
    
    return n


def find_mention_hashtag_around_date(tweets, date, days_delta):
    '''
    Function used to find mentions and hashtags from the tweets at specified date, +- days_delta.
    '''
    date_ts = pd.Timestamp(date)
    
    start_date = date_ts - pd.Timedelta(days=days_delta)
    end_date = date_ts + pd.Timedelta(days=days_delta)
    
    mentions, hashtags = mentions_hashtags_in_period(tweets, start_date, end_date)   
    
    return mentions, hashtags


def get_mentions_hashtags_news_topics(news_list, tweets, days_delta):
    '''
    Function used to link news with certain topics with tweets based on date of creation +-days_delta, adding mentions and hashtags. 
    '''
    ment_list = []
    hash_list = []
    
    ret_df = pd.DataFrame()
    
    for nl in news_list:
        m, h = find_mention_hashtag_around_date(tweets, nl['Date of Airing (EST)'], days_delta)
        
        tmp = {}
        
        tmp['news'] = nl
        tmp['mentions'] = m
        tmp['hashtags'] = h
        
        ret_df = ret_df.append(tmp, ignore_index = True)
    
    return ret_df


def get_mentions_hashtags_news_topics_wrapper(news, tweets, topics_list, days_delta):
    '''
    A wrapper function for getting all the news with tweet hashtags and mentions in the close period of creation.
    We specify the news and tweets dataframes, the topic list we are interested in, as well as the period +-days to look for.
    '''
    news_with_topics = get_news_with_topics(news, topics_list)
    
    return get_mentions_hashtags_news_topics(news_with_topics, tweets, days_delta)