import os
import string
import codecs
from collections import Counter
import math
from itertools import combinations

# Folder containing the song .txt files
SONGS_FOLDER = 'Songs'
# Path to the dictionary file (assumed to be in the same directory)
DICTIONARY_PATH = 'Dictionary/words_alpha.txt'
# Path to the custom lexicon output file
CUSTOM_LEXICON_PATH = 'eminem_lexicon_custom.txt'
# Path to the known words output file
KNOWN_WORDS_PATH = 'known_words_eminem_has_used.txt'

# Function to load the dictionary from words_alpha.txt
def load_dictionary(dictionary_path):
    with open(dictionary_path, 'r', encoding='utf-8') as f:
        valid_words = set(word.strip().lower() for word in f.readlines())
    return valid_words

# Function to normalize the text by removing punctuation and converting to lowercase
def normalize_text(text):
    # Remove punctuation and make lowercase
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator).lower().split()

# Function to calculate Jaccard similarity between two sets
def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0

# Function to calculate cosine similarity between two word frequency dictionaries
def cosine_similarity(dict1, dict2):
    common_words = set(dict1.keys()) & set(dict2.keys())
    numerator = sum(dict1[word] * dict2[word] for word in common_words)
    sum1 = sum(dict1[word]**2 for word in dict1)
    sum2 = sum(dict2[word]**2 for word in dict2)
    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    return numerator / denominator if denominator != 0 else 0

# Function to count similar words between two sets
def count_similar_words(set1, set2):
    return len(set1.intersection(set2))

# Function to process each song file and deduplicate words
def process_songs(folder_path, dictionary_words):
    song_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
    total_songs = len(song_files)
    
    # To track unique words across all songs
    unique_words_overall = set()
    new_words_overall = set()
    known_words_overall = set()
    all_words = []  # To keep track of all words for frequency counting

    longest_dict_word = ''
    
    # New variables for tracking song word counts and content
    song_word_counts = {}
    song_unique_word_counts = {}
    song_unique_words = {}
    song_word_frequencies = {}
    
    for song_file in song_files:
        file_path = os.path.join(folder_path, song_file)
        
        # Try different encodings
        encodings = ['utf-8', 'cp1252', 'iso-8859-1']
        lyrics = None
        
        for encoding in encodings:
            try:
                with codecs.open(file_path, 'r', encoding=encoding) as f:
                    lyrics = f.read()
                break  # If successful, break the loop
            except UnicodeDecodeError:
                continue  # If unsuccessful, try the next encoding
        
        if lyrics is None:
            print(f"Error: Unable to read file {song_file} with any of the attempted encodings.")
            continue  # Skip to the next file
        
        # Normalize and process the words in the lyrics
        words = normalize_text(lyrics)
        unique_words = set(words)
        unique_words_overall.update(unique_words)   # Update the global set of unique words
        all_words.extend(words)  # Add all words to the list for frequency counting
        
        # Update longest dictionary word
        dict_words_in_song = [word for word in unique_words if word in dictionary_words]
        known_words_overall.update(dict_words_in_song)  # Update the global set of known words
        if dict_words_in_song:
            longest_word_in_song = max(dict_words_in_song, key=len)
            if len(longest_word_in_song) > len(longest_dict_word):
                longest_dict_word = longest_word_in_song
        
        # Calculate total words and unique words for each song
        total_words = len(words)
        unique_word_count = len(unique_words)
        song_word_counts[song_file] = total_words  # Store total word count for each song
        song_unique_word_counts[song_file] = unique_word_count  # Store unique word count for each song
        song_unique_words[song_file] = unique_words  # Store set of unique words for each song
        song_word_frequencies[song_file] = Counter(words)  # Store word frequencies for each song
        
        # Compare words with the dictionary
        found_words = [word for word in unique_words if word in dictionary_words]
        new_words = [word for word in unique_words if word not in dictionary_words]
        new_words_overall.update(new_words)  # Update the global set of new words
        
        found_percent = (len(found_words) / unique_word_count) * 100 if unique_word_count > 0 else 0
        new_percent = (len(new_words) / unique_word_count) * 100 if unique_word_count > 0 else 0

        # Output the results for each song
        print(f'Song: {song_file}')
        print(f'Total words: {total_words}')
        print(f'Unique words: {unique_word_count}')
        print(f'Words found in dictionary: {len(found_words)} ({found_percent:.2f}%)')
        print(f'New words (not in dictionary): {len(new_words)} ({new_percent:.2f}%)')
        print('---')

    # Find the most repeated word
    word_counts = Counter(all_words)
    most_common_word, most_common_count = word_counts.most_common(1)[0]

    # Final summary across all lyrics (deduplicated)
    total_unique_words = len(unique_words_overall)
    found_words_overall = [word for word in unique_words_overall if word in dictionary_words]
    
    found_percent_overall = (len(found_words_overall) / total_unique_words) * 100 if total_unique_words > 0 else 0
    new_percent_overall = (len(new_words_overall) / total_unique_words) * 100 if total_unique_words > 0 else 0
    
    # Calculate total percentage relative to dictionary size
    total_dict_words = len(dictionary_words)
    found_percent_of_dict = (len(found_words_overall) / total_dict_words) * 100 if total_dict_words > 0 else 0

    # Find songs with most and least words (total and unique)
    song_most_words = max(song_word_counts, key=song_word_counts.get)
    song_least_words = min(song_word_counts, key=song_word_counts.get)
    song_most_unique_words = max(song_unique_word_counts, key=song_unique_word_counts.get)
    song_least_unique_words = min(song_unique_word_counts, key=song_unique_word_counts.get)
    average_words = sum(song_word_counts.values()) / len(song_word_counts) if song_word_counts else 0
    average_unique_words = sum(song_unique_word_counts.values()) / len(song_unique_word_counts) if song_unique_word_counts else 0

    # Calculate similarity between songs
    song_pairs = list(combinations(song_files, 2))
    jaccard_similarities = {pair: jaccard_similarity(song_unique_words[pair[0]], song_unique_words[pair[1]]) for pair in song_pairs}
    cosine_similarities = {pair: cosine_similarity(song_word_frequencies[pair[0]], song_word_frequencies[pair[1]]) for pair in song_pairs}
    similar_word_counts = {pair: count_similar_words(song_unique_words[pair[0]], song_unique_words[pair[1]]) for pair in song_pairs}

    most_similar_jaccard = max(jaccard_similarities, key=jaccard_similarities.get)
    least_similar_jaccard = min(jaccard_similarities, key=jaccard_similarities.get)
    most_similar_cosine = max(cosine_similarities, key=cosine_similarities.get)
    least_similar_cosine = min(cosine_similarities, key=cosine_similarities.get)
    most_similar_words = max(similar_word_counts, key=similar_word_counts.get)
    least_similar_words = min(similar_word_counts, key=similar_word_counts.get)

    # Output the final summary
    print('--- Final Summary ---')
    print(f'Total songs processed: {total_songs}')
    print(f'Total unique words across all songs: {total_unique_words}')
    print(f'Total words found in dictionary: {len(found_words_overall)} ({found_percent_overall:.2f}%)')
    print(f'Total new words (not in dictionary): {len(new_words_overall)} ({new_percent_overall:.2f}%)')
    print(f'Percentage of dictionary words used: {found_percent_of_dict:.2f}%')
    print(f'Longest dictionary word: "{longest_dict_word}" ({len(longest_dict_word)} characters)')
    print(f'Most repeated word: "{most_common_word}" (repeated {most_common_count} times)')
    print(f'Song with most total words: "{song_most_words}" ({song_word_counts[song_most_words]} words)')
    print(f'Song with least total words: "{song_least_words}" ({song_word_counts[song_least_words]} words)')
    print(f'Song with most unique words: "{song_most_unique_words}" ({song_unique_word_counts[song_most_unique_words]} words)')
    print(f'Song with least unique words: "{song_least_unique_words}" ({song_unique_word_counts[song_least_unique_words]} words)')
    print(f'Average total words per song: {average_words:.2f}')
    print(f'Average unique words per song: {average_unique_words:.2f}')
    print('\nSong Similarity Analysis:')
    print(f'Most similar songs (Jaccard): "{most_similar_jaccard[0]}" and "{most_similar_jaccard[1]}" (similarity: {jaccard_similarities[most_similar_jaccard]:.4f})')
    print(f'Least similar songs (Jaccard): "{least_similar_jaccard[0]}" and "{least_similar_jaccard[1]}" (similarity: {jaccard_similarities[least_similar_jaccard]:.4f})')
    print(f'Most similar songs (Cosine): "{most_similar_cosine[0]}" and "{most_similar_cosine[1]}" (similarity: {cosine_similarities[most_similar_cosine]:.4f})')
    print(f'Least similar songs (Cosine): "{least_similar_cosine[0]}" and "{least_similar_cosine[1]}" (similarity: {cosine_similarities[least_similar_cosine]:.4f})')
    print(f'Songs with most similar words: "{most_similar_words[0]}" and "{most_similar_words[1]}" ({similar_word_counts[most_similar_words]} common words)')
    print(f'Songs with least similar words: "{least_similar_words[0]}" and "{least_similar_words[1]}" ({similar_word_counts[least_similar_words]} common words)')
    print('---')

    # Write new words to custom lexicon file
    with open(CUSTOM_LEXICON_PATH, 'w', encoding='utf-8') as f:
        for word in sorted(new_words_overall):
            f.write(f"{word}\n")
    
    print(f"Custom lexicon saved to {CUSTOM_LEXICON_PATH}")

    # Write known words to file
    with open(KNOWN_WORDS_PATH, 'w', encoding='utf-8') as f:
        for word in sorted(known_words_overall):
            f.write(f"{word}\n")
    
    print(f"Known words saved to {KNOWN_WORDS_PATH}")

# Main script execution
if __name__ == '__main__':
    # Load the dictionary
    dictionary_words = load_dictionary(DICTIONARY_PATH)
    
    # Process the song lyrics in the Songs folder
    process_songs(SONGS_FOLDER, dictionary_words)