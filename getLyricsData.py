import pandas as pd
import lyricsgenius

def get_lyrics(df, genius):
    if 'lyrics' not in df.columns:
        df['lyrics'] = ""
    for idx, row in df.iterrows():
        title = row.get('Title', '')
        try:
            song = genius.search_song(title)
            if song and song.lyrics:
                df.at[idx, 'lyrics'] = song.lyrics
            else:
                df.at[idx, 'lyrics'] = ""
        except Exception as e:
            print(f"error for '{title}': {e}")
            df.at[idx, 'lyrics'] = ""
    return df

def main():
    GENIUS_ACCESS_TOKEN = 'UzZfc5yqC3RUtjl1A5XXV9I33zR2G3bvzsgnvFRvKMeZJ-wPmfglcW2SpZJrA4cQ'
    datafile = "sample_data_1.csv"
    output_csv = "sample_data_1_lyrics.csv"

    genius = lyricsgenius.Genius(GENIUS_ACCESS_TOKEN, skip_non_songs=True, remove_section_headers=True)    
    df = pd.read_csv(datafile)
    df = get_lyrics(df, genius)
    df.to_csv(output_csv)

if __name__ == "__main__":
    main()
