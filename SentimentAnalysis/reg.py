import regex as re

def preprocess_tweet(tweetText):
	
	print("Initial tweet:\n",tweetText,"\n")

	# Removing usernames
	preprocessingTweet = re.sub( r'@([A-Za-z0-9_]+)' , "USERNAME" , tweetText )
	print("After removing usernames:\n" , preprocessingTweet , "\n")

	# Removing links
	preprocessingTweet = re.sub( r"http\S+", 'URL' , preprocessingTweet )
	print("After removing link:\n" ,preprocessingTweet,"\n")

	# Removing Hashtags
	preprocessingTweet = re.sub( r"#[A-Za-z0-9_]+" , 'HASHTAG' , preprocessingTweet )
	print("After removing link:\n", preprocessingTweet,"\n")

	preprocessedTweet = preprocessingTweet
	
	print("Final tweet:\n",preprocessedTweet,"\n")

	return preprocessedTweet

if __name__ == '__main__':
	
	tweet1 = "Mr Macky: Hey, @garrison did something happen with you when you were a child, did your @father321 do anything to you?"
	tweet2 = "Mr. Garrison: No @MrMacky don't, I don't want to remember that......... https://somehub.com/MrGarrsion/Father"
	tweet3 = "Mr. Macky: You will have to face it mmmmkay, you will have to go and talk to them mmkay."
	tweet4 = "Mr. Garrison: I think you are right Mr.Macky."
	tweet5 = "at Home: *dingdong* Hey @mom123 we need to talk about my childhood. Did you know @dad456 never loved me"
	tweet6 = "Father: No @s0N I loved you with all my heart."
	tweet7 = "Mr. Garrison: You know @mom he never harrassed me when i was a child thats because he never loved me"
	tweet8 = "Mom: (gasps)Oh my god!!! I am sorry @s0N, I never knew that, that is why you were so quiet all the time."
	tweet9 = "RT @deantak: bosch enters remote healthcare electronics monitoring business, competing with intel and GE http://tinyurl.com/dkea7r"
	tweet10 = "IVT Intros Bluetooth 3.0 Commercial Stack for Intel Moblin and Google Android Platforms http://tmcnet.com/7563.1"
	tweet11 = "Intel folk 4 work 4 better again RT @bobduffy Use Twitter to make difference. Follow & tweet @TysonFoods for hunger relief #BlogWell"
	tweet12 = "@EricCartman69 can be considered as one of the greatest heroes of humanity #FuckYouGingers #AntiSemite123 #eternalracists #rightwingers http://gotohell.org"

	# print("somehub")
	print(preprocess_tweet(tweet12))