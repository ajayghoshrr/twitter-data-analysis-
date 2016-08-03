import pip


pip.main(['install','tweepy'])


# Import the required libraries.
import tweepy
import pandas as pd
import matplotlib.pyplot as plt


# Make the graphs prettier
pd.set_option('display.mpl_style', 'default')


consumerKey = 'iPIcJAmPTQYiEZ3FF01iuVcvI'
consumerSecret = '8P39msYkvZHdP4wxbhtl7GhFvUfAlJVSMPMTQJRAQr2ESDUbxR'

#Use tweepy.OAuthHandler to create an authentication using the given key and secret
auth = tweepy.OAuthHandler(consumer_key=consumerKey, 
 consumer_secret=consumerSecret)

#Connect to the Twitter API using the authentication
api = tweepy.API(auth)


#Perform a basic search query where we search for the'#KABALI2016' in the tweets
result = api.search(q='%23 KABALI 2016') #%23 is used to specify '#'

# Print the number of items returned by the search query to verify our query ran. Its 15 by default
len(result)

tweet = result[0] #Get the first tweet in the result

# Analyze the data in one tweet to see what we require
for param in dir(tweet):
#The key names beginning with an '_' are hidden ones and usually not required, so we'll skip them
 if not param.startswith("_"):
 print "%s : %s\n" % (param, eval('tweet.'+param))


results = []

     #Get the first 5000 items based on the search query
     for tweet in tweepy.Cursor(api.search, q='%23KABALI2016').items(5000):
     results.append(tweet)

    # Verify the number of items returned
    print len(results)


    # Create a function to convert a given list of tweets into a Pandas DataFrame.
    # The DataFrame will consist of only the values, which I think might be useful for analysis...


    def toDataFrame(tweets):

    DataSet = pd.DataFrame()	

    DataSet['tweetID'] = [tweet.id for tweet in tweets]
    DataSet['tweetText'] = [tweet.text for tweet in tweets]
    DataSet['tweetRetweetCt'] = [tweet.retweet_count for tweet 
    in tweets]
    DataSet['tweetFavoriteCt'] = [tweet.favorite_count for tweet 
    in tweets]
    DataSet['tweetSource'] = [tweet.source for tweet in tweets]
    DataSet['tweetCreated'] = [tweet.created_at for tweet in tweets]


    DataSet['userID'] = [tweet.user.id for tweet in tweets]
    DataSet['userScreen'] = [tweet.user.screen_name for tweet 
    in tweets]
    DataSet['userName'] = [tweet.user.name for tweet in tweets]
    DataSet['userCreateDt'] = [tweet.user.created_at for tweet 
    in tweets]
    DataSet['userDesc'] = [tweet.user.description for tweet in tweets]
    DataSet['userFollowerCt'] = [tweet.user.followers_count for tweet 
    in tweets]
    DataSet['userFriendsCt'] = [tweet.user.friends_count for tweet 
    in tweets]
    DataSet['userLocation'] = [tweet.user.location for tweet in tweets]
    DataSet['userTimezone'] = [tweet.user.time_zone for tweet 
    in tweets]

    return DataSet

    #Pass the tweets list to the above function to create a DataFrame
    DataSet = toDataFrame(results)


DataSet.head(5)


DataSet.tail(2)

DataSet = DataSet[DataSet.userTimezone.notnull()]

# Let's also check how many records are we left with now
len(DataSet)


tzs = DataSet['userTimezone'].value_counts()[:10]
print tzs


# Create a bar-graph figure of the specified size
plt.rcParams['figure.figsize'] = (15, 5)

# Plot the Time Zone data as a bar-graph
tzs.plot(kind='bar')


# Assign labels and title to the graph to make it more presentable
plt.xlabel('Timezones')
plt.ylabel('Tweet Count')
plt.title('Top 10 Timezones tweeting about #Oscars2015')
tweetPath = os.path.join("data_?les", "twitter")
tweetFiles = {
"time01": os.path.join(tweetPath, "statuses.*.gz")
 }
 frequencyMap = {}
 globalTweetCounter = 0
 timeFormat = "%a %b %d %H:%M:%S +0000 %Y"
 reader = codecs.getreader("utf-8")
 for (key, path) in tweetFiles.items():
 localTweetList = []
 for ?lePath in glob.glob(path):
 print ("Reading File:", ?lePath)
        
for line in gzip.open(?lePath, 'rb'):
# Try to read tweet JSON into object
 tweetObj = None
 try:
  tweetObj = json.loads(reader.decode(line)[0])
  except Exception as e:
  continue # Deleted status messages and protected status must be skipped
   if ( "delete" in tweetObj.keys() or “status_withheld" in tweetObj.keys() ):
   continue
   else:
    frequencyMap[currentTime] = {"count":1, “list":[tweetObj]}
    # Fill in any gaps
     times = sorted(frequencyMap.keys())
     ?rstTime = times[0]
     lastTime = times[-1]
     thisTime = ?rstTime
     timeIntervalStep = datetime.timedelta(0, 60)    # Time step in seconds
     while ( thisTime <= lastTime ):
     if ( thisTime not in frequencyMap.keys() ):
     frequencyMap[thisTime] = {"count":0, "list":[]}
        
     thisTime = thisTime + timeIntervalStep
     print ("Processed Tweet Count:", globalTweetCounter)
      # Try to extract the time of the tweet
     try:
     currentTime = datetime.datetime.strptime(tweetObj['created_at'], timeFormat)
     except:
     print (line)
     raise
     currentTime = currentTime.replace(second=0)
            
     # Increment tweet count
     globalTweetCounter += 1
            
     # If our frequency map already has this time, use it, otherwise add
     if ( currentTime in frequencyMap.keys() ):
     timeMap = frequencyMap[currentTime]
     timeMap["count"] += 1
  timeMap["list"].append(tweetObj)
             
  import matplotlib.pyplot as plt
  ?g, ax = plt.subplots()6
  ?g.set_size_inches(18.5,10.5)
  plt.title("Tweet Frequency")
  # Sort the times into an array for future use
 sortedTimes = sorted(frequencyMap.keys())
 # What time span do these tweets cover?
 print ("Time Frame:", sortedTimes[0], sortedTimes[-1])
 # Get a count of tweets per minute
postFreqList = [frequencyMap[x]["count"] for x in sortedTimes]
# We'll have ticks every thirty minutes (much more clutters the graph)
smallerXTicks = range(0, len(sortedTimes), 30)
plt.xticks(smallerXTicks, [sortedTimes[x] for x in smallerXTicks], rotation=90)
# Plot the post frequency
ax.plot(range(len(frequencyMap)), [x if x > 0 else 0 for x in postFreqList], color="blue", label="Posts")
ax.grid(b=True, which=u'major')
ax.legend()
plt.show()
