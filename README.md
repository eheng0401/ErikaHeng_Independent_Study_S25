# ErikaHeng_Independent_Study_S25: Customized Music Search System

## Problem Statement
### Our Problem:
My initial plan was to create a better way of searching for music similar to your current favorites. Spotify has great algorithms and curated playlists for discovering new music based on your listening habits, including a song radio that creates a playlist based on any given song. However there are limits to these features, as they often give you songs you already listen to regularly, or the recommended songs aren’t similar to the target song in the way that you want. For example, you may like how it sounds but you don’t care as much about the lyrics, or vice versa. Spotify has a lot of metadata on songs that track features like danceability, speechiness, mood, etc. My goal was to create a song search engine that allows a user to specify their search preferences and create a better way to find new music when you know what you’re looking for. I wanted to create an application compatible with Spotify using its robust API.
### Setback:
Upon starting this project, I discovered that Spotify had depreciated essentially all of the important endpoints in their API due to security concerns with their metadata in the wake of AI. This was done to prevent external sources from training AI models on their proprietary song data. This served as a huge barrier to my project, as my entire plan rested on using a lot of the recommendation infrastructure in Spotify, as to not try to invent the wheel of recommendation algorithms, but to sharpen and optimize search capabilities.
### My New Goal: 
My new goal was to create a specified song search engine that allows users to specify and filter their results based on specific features of a song. Instead of using Spotify’s API, I used song metadata from external databases and imported search algorithm libraries to model the product in lieu of the original Spotify-backed product.

## Song Database
I obtained a sample dataset for this application from an existing discontinued public database by AcousticBrainz that contains millions of songs with metadata extracted from songs using Essentia, which is a library used for music data analysis from audio files (AcousticBrainz; Essentia 2.1). My dataset contained around 100,000 songs of all genres. The data was initially downloaded as individual json files containing this metadata. I used python scripts to aggregate my desired data points from each song file into one CSV for easier application search. Out of the metadata in the original dataset, I extracted 60 features that were divided among the 5 filters, aside from Title and MusicBrainz Recording ID which were used for searching but not factored into the algorithm:

- **Danceability:** danceability quantified into one value on a 0-1 scale
- **Genre:** dataset contains results from 4 different algorithms that determine a song’s genre. Each algorithm contains a set of 0-1 scores indicating the level of compatibility with a genre label (e.g. electronic, hip-hip, jazz) as well as the top genre label for each algorithm
- **Mood:** quantified into the following 0-1 values computing compatibility with each mood label: acoustic, aggressive, electronic, happy, party, relaxed, sad
- **Sound:** 0-1 scores for a song’s timbre, tonal, and 10 sound category scores extracted from the sound algorithm
- **Lyrics:** song lyric were not provided in the AcousticBrainz dataset. I used the LyricsGenius python client library for the Genius lyrics API to obtain lyrics for songs and input them into the dataset (LyricsGenius). 


