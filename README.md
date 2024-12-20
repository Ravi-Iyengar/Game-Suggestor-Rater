# Game-Suggestor-Rater
These group of Python Scripts use Random Forest methods to predict game ratings of a given user. Thanks to the IGBD database's friendly API features, this draws information on themes, genres and keywords to try and give expected ratings for games that are on a user's backlog by parsing through existing data on played items. Backloggd.com is required. Essentially predicting how much the model thinks you will like any given game; for example if you don't know what to play next, you can use these scripts to generate a CSV that has predicted ratings of all the games on your backlog and work your way through what it thinks are the best (or worst!) games for you.

Firstly, have your account on Backloggd.com setup and registered with games that you have played with their Ratings and Hours Played (ideally at least 50 for a good sample size; the more games available the better job the predictor does). Make sure you setup your API access token with Twitch on the IGBD website; they have a well documented page you can find on the API section.

Make sure all the python scripts are in one common root folder (i.e., no sub-folders; you can just make a folder on desktop called Predictor and store them all there and run them in the order below with your choice of IDLE)

Replace the yourusername section in the URL for the backlogscrapper and PlayedGamesScrapper; setup your API ID and secret on twitch and replace it in the API caller for IGDB and BacklogDataBasePuller; both of these are specific for you; I have not figured out a way to make this process automated yet so everyone doesn't have to make their own access codes/tokens by creating a full-blown application but I will update this if I am ever able to figure that out. 

Additonally double-check the amount of pages you want to parse in both PlayedGames and Backlogscrapper as this will vary per account.

IMPORTANT: THIS METHOD ASSUMES THE PLAYED GAME HAVE SOME HOURS SET AND SOME RATING GIVEN; without that set it will not work.

Run the Files in the following order: PlayedGamesScrapper -> API Caller for IGDB -> Cleaner -> backlogscrapper -> BacklogDataBasePuller -> BacklogCleaner. 

This should leave you with two big csvs called MergedGameDetails.csv and CleanedBacklogdata.csv; these are used in the final step.

Run Model Creator.py and it will give you a final output of PredictedBacklogRatings.csv that should be sorted from highest to lowest predicted rating, and will give you an idea on what to play next if you can't decide :D.

I'd like to extend this approach to books and movies at some point and create a full-web-application, but hopefully this is interesting for some.
