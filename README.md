# Customized Music Search System

## Problem Statement
### Our Problem:
My initial plan was to create a better way of searching for music similar to your current favorites. Spotify has great algorithms and curated playlists for discovering new music based on your listening habits, including a song radio that creates a playlist based on any given song. However there are limits to these features, as they often give you songs you already listen to regularly, or the recommended songs aren’t similar to the target song in the way that you want. For example, you may like how it sounds but you don’t care as much about the lyrics, or vice versa. Spotify has a lot of metadata on songs that track features like danceability, speechiness, mood, etc. My goal was to create a song search engine that allows a user to specify their search preferences and create a better way to find new music when you know what you’re looking for. I wanted to create an application compatible with Spotify using its robust API.
### Setback:
Upon starting this project, I discovered that Spotify had depreciated essentially all of the important endpoints in their API due to security concerns with their metadata in the wake of AI. This was done to prevent external sources from training AI models on their proprietary song data. This served as a huge barrier to my project, as my entire plan rested on using a lot of the recommendation infrastructure in Spotify, as to not try to invent the wheel of recommendation algorithms, but to sharpen and optimize search capabilities.
### My New Goal: 
My new goal was to create a specified song search engine that allows users to specify and filter their results based on specific features of a song. Instead of using Spotify’s API, I used song metadata from external databases and imported search algorithm libraries to model the product in lieu of the original Spotify-backed product.

## The Product
This app is supported using flask/python. I created a simple front-end interface for this application using basic HTML and CSS. The application takes song titles for search, as well as 5 selectable filters. The user must select a minimum of one filter and a maximum of all 5. Upon search, the application will display the top 5 search results based on the chosen filters as well as a distance/compatibility score with the lowest numbers meaning a closer match.

## Song Database
I obtained a sample dataset for this application from an existing discontinued public database by AcousticBrainz that contains millions of songs with metadata extracted from songs using Essentia, which is a library used for music data analysis from audio files (AcousticBrainz; Essentia 2.1). My dataset contained around 100,000 songs of all genres. The data was initially downloaded as individual json files containing this metadata. I used Python scripts to aggregate my desired data points from each song file into one CSV for easier application search. Out of the metadata in the original dataset, I extracted 60 features that were divided among the 5 filters, aside from Title and MusicBrainz Recording ID which were used for searching but not factored into the algorithm:

- **Danceability:** danceability quantified into one value on a 0-1 scale
- **Genre:** dataset contains results from 4 different algorithms that determine a song’s genre. Each algorithm contains a set of 0-1 scores indicating the level of compatibility with a genre label (e.g. electronic, hip-hop, jazz) as well as the top genre label for each algorithm
- **Mood:** quantified into the following 0-1 values computing compatibility with each mood label: acoustic, aggressive, electronic, happy, party, relaxed, sad
- **Sound:** 0-1 scores for a song’s timbre, tonal, and 10 sound category scores extracted from the sound algorithm
- **Lyrics:** song lyric were not provided in the AcousticBrainz dataset. I used the LyricsGenius python client library for the Genius lyrics API to obtain lyrics for songs and input them into the dataset (LyricsGenius). 

## Searching Algorithm
### FAISS Search:
I used the FAISS (Facebook AI Similarity Search) to implement my song search algorithm (FAISS Documentation). FAISS is an open-source library developed by Meta AI for fast similarity search using high-dimensional vectors of numerical values. I determined that a KNN (K-nearest neighbor) type algorithm is most suitable type for my search function and dataset size, which finds the k most similar items based on feature distance. The FAISS library is actually an ANN (Approximate nearest neighbor) algorithm that uses vector indexing, clustering, and fast matrix math to compute distance scores. This is similar to KNN except it is even better for this specific application because it doesn’t compute exact scores or scan every single result, rather it computes “close enough” matches that produce very similar results to KNN with much faster speed and less computing power. Because users want an array of results that ideally will vary even upon the same search, an ANN algorithm is less concerned with finding the exact number of top k searches and instead provides several viable results for the user.
### Algorithm:
The FAISS Search takes in numerical values to create vector representations of songs and then compares their ‘distances’. The algorithm takes the 0-1 numerical values from the dataset to form these vectors and perform calculations. For lyrics that are non-numerical, the lyrics are tokenized and translated into TF-IDF values that are then used for vectorization. Then, based on the user’s selected filters, 0/1 weights are applied onto these values to determine which metadata points are factored into the vector for similarity calculation.	

## Future Directions
### Database scaling w/ Essentia:
With this version of the product, the application is currently only limited to songs in the database. Ideally with more access to resources like processing power and increased database storage capacity, this application could scale to include millions of songs. By utilizing Essentia to extract song metadata from audio files, users could potentially insert songs and add to their database instantly, making the application more usable in practice.
### Shuffling results, tracking unheard, displaying metadata:
Further improvements would include shuffling results to provide new suggestions even when searching the same song. This would involve further tracking of the number of searches each song gets and a system to take user feedback on whether they liked the recommended songs. I intentionally did not display the songs metadata exact values for simplicity reasons, as users don’t always care about those numeric values and can be unnecessary for the application’s UI, however this can easily be added
### Spotify Version using API:
If the Spotify API was largely available, this likely would have immensely improved both scaling capabilities, usability, and search results. My initial idea was to provide users a way to specifically filter their searches from Spotify’s already amazing music recommendation algorithms to optimize the song searching process when users have a specific idea of what they would like to hear, as it would be futile to try and completely recreate a recommendation algorithm from scratch to try and compete with Spotify. Using their API would allow access to the entire Spotify music library, better search recommendations, would improve search speed, and the quality of the metadata.

## Instructions for Running Program:
- Download data here: https://drive.google.com/file/d/1g0TlZg6ZRtpwGQtHm8kMkEePpOhkluRK/view?usp=sharing
- run faissSearch.py

## Sources
AcousticBrainz, acousticbrainz.org/.
“A Python Client for the Genius.Com API.” LyricsGenius, lyricsgenius.readthedocs.io/en/master/.
“Essentia 2.1-Beta6-Dev Documentation.” Overview - Essentia 2.1-Beta6-Dev Documentation, essentia.upf.edu/documentation.html.
“FAISS Documentation.” Welcome to Faiss Documentation - Faiss Documentation, faiss.ai/index.html.
