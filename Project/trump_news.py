def extract_unique_topics(topics):
    '''
    Function for extracting unique topics from the topic interable object (pandas.Series).

    Parameters:
    topics -- iterable object containing topics

    Returns:
    set -- set of topics appearing in the dataset
    '''
    container = []
    
    for topic in topics:
        tmp = topic.split(',')
        container.extend(tmp)

    return set(container)


def count_occurence(topic_name, topics):
    '''
    Helper function for counting the occurence of certain topic among topics.
    
    Parameters:
    topic_name -- string, topic for which to count occurence
    topics -- list of topics per news from the news dataset, topics are comma delimited
    
    
    Returns:
    count -- integer, number of occurences
    
    '''
    count = 0
    
    for topic in topics:
        tmp = topic.split(',')
        if(topic_name in tmp):
            count += 1

    return count

def get_occurence(topics_set, topics_series):
    '''
    Helper function to create a dictionary of topics (key) with occurence count (value).
    
    Parameters:
    topics_set -- python set, list of unique topics
    topics_series -- python list, complete list of topics from the news dataset
    
    Returns:
    occurences -- python dictionary, key - topic name, value - number of topic occurences
    '''
    occurences = {}
    
    for topic in topics_set:
        occurences[topic] = count_occurence(topic, topics_series)
        
    return occurences


def get_topics_in_period(news_df, start_date, end_date):
    '''
    A function for obtaining dataframe containing topics in the specified timeframe.
    
    Parameters:
    news_df -- news dataset dataframe
    start_date -- starting date to consider, pandas timestamp or valid string
    end_date -- ending date to consider, pandas timestamp or valid string
    
    Returns:
    topic_df -- dataframe containing a row of topics in selected period with their count
    '''
    # we filter the dataframe by dates
    news_copy = news_df.copy()
    news = news_copy.loc[(news_df['Date of Airing (EST)']>=pd.Timestamp(start_date)) &
                       (news_df['Date of Airing (EST)']<=pd.Timestamp(end_date))]
    
    # we get the topic list column
    topics = news['Topic List']

    # we replace the NA values with ''
    topics.fillna(value='', inplace=True)
    
    s = extract_unique_topics(topics)
    
    occurences = get_occurence(s, topics)
    
    topic_series = pd.Series(occurences)
    topic_df = pd.DataFrame(topic_series)

    topic_df.reset_index(inplace=True)
    topic_df.columns = ['topic','count']
    
    return topic_df


def show_top_topics(topic_df, number, year_title):
    '''
    A helper function for displaying selected number of top topics in given topic dataframe.
    
    Parameters:
    topic_df -- topic dataframe containing topic and count, from the news dataset
    number -- number of top topics to consider
    year_title -- year for which the chart is obtained 
    
    Returns:
    nothing
    '''
    topic_df_sorted = topic_df.sort_values(by='count', ascending=False)
    
    if(number>topic_df.shape[0]):
        number = topic_df.shape[0]
    
    top = topic_df_sorted[0:number]
    
    plt.figure(figsize=(15,8))

    p = sns.barplot(data=top, x='count', y='topic')
    p.set_title('Top '+str(number)+' topics in year '+str(year_title))
    
    
def show_top_topics_plotly(topic_df, number, year_title):
    '''
    A helper function for displaying selected number of top topics in given topic dataframe.
    
    Parameters:
    topic_df -- topic dataframe containing topic and count, from the news dataset
    number -- number of top topics to consider
    year_title -- year for which the chart is obtained 
    
    Returns:
    nothing
    '''
    topic_df_sorted = topic_df.sort_values(by='count', ascending=False)
    
    if(number>topic_df.shape[0]):
        number = topic_df.shape[0]
    
    top = topic_df_sorted[0:number]
    
    data = [go.Bar(
            y=top['topic'],
            x=top['count'],
            orientation='h'
    )]
    
    layout = go.Layout(
        title = 'Top '+str(number)+' topics in year '+str(year_title),
    )
    
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename='html/top_topics'+str(year_title)+'.html')
    display(IFrame('html/top_topics'+str(year_title)+'.html', "100%", "500px"))
    
    
