import pandas as pd
import lyricsgenius
import time

def fetch_lyrics(df, genius):
    if 'lyrics' not in df.columns:
        df['lyrics'] = ""

    for idx, row in df.iterrows():
        title = row.get('Title', '')
        if not title:
            continue

        try:
            song = genius.search_song(title)
            if song and song.lyrics:
                df.at[idx, 'lyrics'] = song.lyrics
            else:
                df.at[idx, 'lyrics'] = ""
        except Exception as e:
            print(f"Error fetching lyrics for '{title}': {e}")
            df.at[idx, 'lyrics'] = ""

        time.sleep(1)  # avoid hitting rate limits too fast

    return df

def main():
    GENIUS_ACCESS_TOKEN = 'UzZfc5yqC3RUtjl1A5XXV9I33zR2G3bvzsgnvFRvKMeZJ-wPmfglcW2SpZJrA4cQ'

    input_csv = "sample_data_1.csv"
    output_csv = "your_output_file_with_lyrics.csv"

    # Initialize Genius client
    genius = lyricsgenius.Genius(GENIUS_ACCESS_TOKEN, skip_non_songs=True, remove_section_headers=True)
    genius.timeout = 10
    genius.retries = 3

    try:
        df = pd.read_csv(input_csv)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return

    if 'Title' not in df.columns:
        print("Error: The CSV file must have a 'Title' column.")
        return

    df = fetch_lyrics(df, genius)

    try: # saving updated df
        df.to_csv(output_csv, index=False)
        print(f"Updated CSV saved as '{output_csv}'")
    except Exception as e:
        print(f"Error saving CSV file: {e}")

if __name__ == "__main__":
    main()
