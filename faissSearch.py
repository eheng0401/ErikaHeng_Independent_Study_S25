import pandas as pd
import numpy as np
import faiss
import lyricsgenius
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from flask import Flask, render_template, request

def load_data(csv_file):
    df = pd.read_csv(csv_file)
    return df

def preprocess_data(df, features):
    numeric_features = [col for col in features if col not in ["Title", "MusicBrainz Recording ID", "lyrics"]]
    song_features_numeric = df[numeric_features].copy()
    song_features_numeric = song_features_numeric.apply(pd.to_numeric, errors='coerce').fillna(0)
    
    scaler = MinMaxScaler()
    normalized_features = scaler.fit_transform(song_features_numeric)
    
    lyrics_data = df['lyrics'].fillna('')  # Process lyrics using TF-IDF
    lyrics_data = lyrics_data.replace(r'^\s*$', '', regex=True)  # Replace single spaces with empty string

    
    tfidf = TfidfVectorizer(max_features=100, token_pattern=r'(?u)\b\w+\b')# tfidf = TfidfVectorizer(max_features=100)  # limit features for performance
    tfidf_matrix = tfidf.fit_transform(lyrics_data)
    if tfidf_matrix.shape[1] > 20:
        svd = TruncatedSVD(n_components=20, random_state=42)
        lyrics_features = svd.fit_transform(tfidf_matrix)
    else:
        lyrics_features = tfidf_matrix.toarray()

   
    lyrics_features_scaled = MinMaxScaler().fit_transform(lyrics_features)  # Scale lyrics features to same range
    combined_features = np.hstack([normalized_features, lyrics_features_scaled]) # Combine numeric and lyrics features
    extended_numeric_features = numeric_features + [f'lyrics_feature_{i}' for i in range(lyrics_features_scaled.shape[1])] #add lyric features back

    return combined_features, extended_numeric_features

# applying song search filters based on user selection
def apply_boolean_filters(weights, danceability, genre, mood, sound, lyrics):
    bool_mappings = {
        danceability: [0],  # Danceability index
        genre: list(range(2, 37)),  # Genre indices
        mood: list(range(37, 44)),  # Mood indices
        sound: list(range(44, 58)),  # Sound indices
        lyrics: list(range(58, len(weights)))  # lyrics features are at the end
    }
    for boolean, indices in bool_mappings.items():
        if boolean:
            for index in indices:
                weights[index] = 1.0
                
    return weights

def create_faiss_index(normalized_features, numeric_features, weights):
    assert normalized_features.shape[1] == len(weights), "Mismatch between features and weights" #error handling
    weighted_features = normalized_features * weights
    index = faiss.IndexFlatL2(len(numeric_features))
    assert weighted_features.shape[1] == index.d, "FAISS expects a different number of features"
    index.add(weighted_features.astype('float32'))
    return index, weighted_features

def find_similar_songs(df, index, weighted_features, song_title, k=5):
    if song_title not in df["Title"].values:
        return ["Song not found in dataset."]
    
    song_index = df[df["Title"] == song_title].index[0]
    query_song = weighted_features[song_index].reshape(1, -1).astype('float32')
    extra = 10
    results = []
    seen_titles = set()
    
    while len(results) < k:
        distances, indices = index.search(query_song, k=k + extra)
        for rank, idx in enumerate(indices[0]):
            result_title = df.iloc[idx]['Title']
            if result_title == song_title or result_title in seen_titles:
                continue
            seen_titles.add(result_title)
            results.append(f"{len(results) + 1}. {result_title} (Distance: {distances[0][rank]:.4f})") #display results
            if len(results) == k:
                break
        if len(results) < k:
            extra += 5
    return results

app = Flask(__name__)   #hosting frontend in flask
@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    if request.method == 'POST':
        search_title = request.form.get('search_query', '')
        danceability = 'danceability' in request.form
        genre = 'genre' in request.form
        mood = 'mood' in request.form
        sound = 'sound' in request.form
        lyrics = 'lyrics' in request.form 
        results = main(search_title, danceability, genre, mood, sound, lyrics)
    return render_template('index.html', results=results)

def main(search_title, danceability=False, genre=False, mood=False, sound=False, lyrics=False):
    csv_file = "sample_data_1_updated.csv"
    df = load_data(csv_file)

    features = ["Title", "MusicBrainz Recording ID", "Danceability",
                "genre_dortmund", "dort_alternative", "dort_blues", "dort_electronic", "dort_folkcountry","dort_funksoulrnb", "dort_jazz", "dort_pop", "dort_raphiphop", "dort_rock", 
                "genre_electronic", "elec_amb", "elec_dnb", "elec_hou", "elec_tec", "elec_tra", 
                "genre_rosamerica", "rosa_cla", "rosa_dan", "rosa_hip", "rosa_jazz", "rosa_pop", "rosa_rhy", "rosa_roc", "rosa_spe", 
                "genre_tzanetakis", "tzan_blu", "tzan_cla", "tzan_cou", "tzan_dis", "tzan_hip", "tzan_jaz", "tzan_met", "tzan_pop", "tzan_reg", "tzan_roc", 
                "mood_acoustic", "mood_aggressive", "mood_electronic", "mood_happy", "mood_party", "mood_relaxed", "mood_sad",
                "timbre", "tonal", "ismi_cha", "ismi_jiv", "ismi_qui", "ismi_ram", "ismi_rin", "ismi_rmis", "ismi_sam", "ismi_tan", "ismi_vie", "ismi_wal", 
                "voice", "lyrics"]
    
    normalized_features, numeric_features = preprocess_data(df, features)
    weights = np.zeros(len(numeric_features))
    weights = apply_boolean_filters(weights, danceability, genre, mood, sound, lyrics)

    if not any([danceability, genre, mood, sound, lyrics]):
        return ["No filters selected. Please choose at least one filter before searching."]
    
    index, weighted_features = create_faiss_index(normalized_features, numeric_features, weights)
    return find_similar_songs(df, index, weighted_features, search_title, k=5)

if __name__ == "__main__":
    app.run(debug=True)
