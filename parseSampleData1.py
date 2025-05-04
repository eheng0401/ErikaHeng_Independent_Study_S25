from pathlib import Path
import json
import csv

mainFolderName = 'acousticbrainz-highlevel-json-20220623'

def process_json_files(mainFolderName, csv_filename):
    main_folder = Path(mainFolderName)
    
    # Open CSV file for writing
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "MusicBrainz Recording ID", "Danceability", 
                         "genre_dortmund", "dort_alternative", "dort_blues", "dort_electronic", "dort_folkcountry","dort_funksoulrnb", "dort_jazz", "dort_pop", "dort_raphiphop", "dort_rock", 
                         "genre_electronic", "elec_amb", "elec_dnb", "elec_hou", "elec_tec", "elec_tra",
                         "genre_rosamerica", "rosa_cla", "rosa_dan", "rosa_hip", "rosa_jazz", "rosa_pop", "rosa_rhy", "rosa_roc", "rosa_spe",
                         "genre_tzanetakis", "tzan_blu", "tzan_cla", "tzan_cou", "tzan_dis", "tzan_hip", "tzan_jaz", "tzan_met", "tzan_pop", "tzan_reg", "tzan_roc",
                         "mood_acoustic", "mood_aggressive", "mood_electronic", "mood_happy", "mood_party", "mood_relaxed", "mood_sad",
                         "timbre", "tonal", "ismi_cha", "ismi_jiv", "ismi_qui", "ismi_ram", "ismi_rin", "ismi_rmis", "ismi_sam", "ismi_tan", "ismi_vie", "ismi_wal",
                         "voice"])  # Write header

    
        for json_file in main_folder.rglob("*.json"):  # Searches all JSON files in subdirectories
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)  # Parse JSON content

                tags = data["metadata"]["tags"]  # metadata and tags always exist
                highLevel = data["highlevel"]

    
                if "title" in tags and "musicbrainz_recordingid" in tags:   # Ensure both 'title' and 'musicbrainz_recordingid' exist
                    row = []
                    title = tags["title"]
                    songId = tags["musicbrainz_recordingid"]
    
                    if isinstance(title, list) and title:   # Convert lists to strings if necessary
                        title = title[0]
                    row.append(title) # add title
                    if isinstance(songId, list) and songId:
                        songId = songId[0]
                    row.append(songId) # add songid


                    ### DANCEABILITY ###
                    if "danceability" in highLevel:  # get danceability
                        danceability = highLevel["danceability"]["all"]["danceable"]
                        row.append(danceability)
                    else:
                        row.append(-0.1)

                    ### GENRE ###
                    if "genre_dortmund" in highLevel: # get genre_dortmund + values             # CODE ASSUMES NUMBER OF FIELDS IN dort_values IS ALWAYS RIGHT
                        dort_values = get_genre_values(highLevel["genre_dortmund"]) 
                        row.append(highLevel["genre_dortmund"]["value"])   # genre label
                        row.extend(dort_values)  # adding values for: alt, blu, electonic, folk, funksoul, jazz, pop, rap, rock

                    if "genre_electronic" in highLevel: # get genre_electronic + values         # CODE ASSUMES NUMBER OF FIELDS IN elec_values IS ALWAYS RIGHT
                        elec_values = get_genre_values(highLevel["genre_electronic"])
                        row.append(highLevel["genre_electronic"]["value"]) # genre label
                        row.extend(elec_values) # adding values for: ambient, dnb, house, techno, trance

                    if "genre_rosamerica" in highLevel: # get genre_rosamerica + values         # CODE ASSUMES NUMBER OF FIELDS IN rosa_values IS ALWAYS RIGHT
                        rosa_values = get_genre_values(highLevel["genre_rosamerica"])
                        row.append(highLevel["genre_rosamerica"]["value"])  # genre label
                        row.extend(rosa_values) # adding values for: cla, dan, hip, jaz, pop, rhy, roc, spe

                    if "genre_tzanetakis" in highLevel: # get genre_tzanetakis + values         # CODE ASSUMES NUMBER OF FIELDS IN tzan_values IS ALWAYS RIGHT
                        tzan_values = get_genre_values(highLevel["genre_tzanetakis"])
                        row.append(highLevel["genre_tzanetakis"]["value"])  # genre label
                        row.extend(tzan_values) # adding values for: blu, cla, cou, dis, hip,  jaz, met, pop, reg, roc

                    ### MOOD ###
                    if all(key in highLevel for key in ["mood_acoustic", "mood_aggressive", "mood_electronic", 
                                    "mood_happy", "mood_party", "mood_relaxed", "mood_sad"]):
                        mood_values = get_mood_values(highLevel)
                        row.extend(mood_values)

                    ### SOUND ###
                    if "timbre" in highLevel and "tonal_atonal" in highLevel and "ismir04_rhythm" in highLevel:
                        sound_values = get_sound_values(highLevel)
                        row.extend(sound_values)

                    ### LYRICS ###
                    if "voice_instrumental" in highLevel:
                        row.append(highLevel["voice_instrumental"]["all"]["voice"])

                    writer.writerow(row)
                    print(f"Added to CSV: {title} -> {songId}")  # Debugging print

                else:
                    print(f"Skipping {json_file}: Missing 'title' or 'musicbrainz_recordingid'.")
            except json.JSONDecodeError:
                print(f"Error: Invalid JSON format in {json_file}")
            except Exception as e:
                print(f"Unexpected error with {json_file}: {e}")
            except (KeyError, IndexError, TypeError):
                print("key or index or type error")
                return None


def get_genre_values(dataset):
    values = []
    if "all" in dataset:
        allData = dataset["all"]
        values = list(allData.values())
    return values

def get_mood_values(dataset):
    arr = []
    arr.append(dataset["mood_acoustic"]["all"]["acoustic"])
    arr.append(dataset["mood_aggressive"]["all"]["aggressive"])
    arr.append(dataset["mood_electronic"]["all"]["electronic"])
    arr.append(dataset["mood_happy"]["all"]["happy"])
    arr.append(dataset["mood_party"]["all"]["party"])
    arr.append(dataset["mood_relaxed"]["all"]["relaxed"])
    arr.append(dataset["mood_sad"]["all"]["sad"])
    return arr
    ###### ADD MIREX STUFF?

def get_sound_values(dataset):
    arr = []
    arr.append(dataset["timbre"]["all"]["bright"])
    arr.append(dataset["tonal_atonal"]["all"]["tonal"])
    arr.append(dataset["ismir04_rhythm"]["all"]["ChaChaCha"])
    arr.append(dataset["ismir04_rhythm"]["all"]["Jive"])
    arr.append(dataset["ismir04_rhythm"]["all"]["Quickstep"])
    arr.append(dataset["ismir04_rhythm"]["all"]["Rumba-American"])
    arr.append(dataset["ismir04_rhythm"]["all"]["Rumba-International"])
    arr.append(dataset["ismir04_rhythm"]["all"]["Rumba-Misc"])
    arr.append(dataset["ismir04_rhythm"]["all"]["Samba"])
    arr.append(dataset["ismir04_rhythm"]["all"]["Tango"])
    arr.append(dataset["ismir04_rhythm"]["all"]["VienneseWaltz"])
    arr.append(dataset["ismir04_rhythm"]["all"]["Waltz"])
    return arr


def main():
    csv_filename = 'sample_data_1.csv'
    process_json_files(mainFolderName, csv_filename)
    print(f"CSV file '{csv_filename}' has been created successfully.")


main()
