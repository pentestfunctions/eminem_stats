# Eminem Song Lyrics Analysis

This project analyzes Eminem's song lyrics from all albums (excluding intros, outros, and splits) to extract unique words, analyze word usage patterns, and calculate song similarity. The dataset used for this project was sourced from [Kaggle](https://www.kaggle.com/datasets/thaddeussegura/eminem-lyrics-from-all-albums?resource=download), covering 223 albums of Eminem's discography.

## Dataset

- **Source**: [Eminem Lyrics from All Albums (Kaggle)](https://www.kaggle.com/datasets/thaddeussegura/eminem-lyrics-from-all-albums?resource=download)
- **Exclusion**: Intros, outros, and split tracks are not included in this analysis.

## Dictionary

- **Source**: [DWYL's English Words Dictionary](https://github.com/dwyl/english-words/blob/master/words_alpha.txt)
- This dictionary was used to identify common English words in Eminem's lyrics.
- Any words not found in the dictionary were flagged as potential slang, misspellings, or unique usages and saved to a custom lexicon.

## Key Findings

### Word Analysis
- **Total songs processed**: 220
- **Total unique words across all songs**: 13,664
- **Total words found in dictionary**: 10,868 (79.54%)
- **Total new words (not in dictionary)**: 2,796 (20.46%)
- **Percentage of dictionary words used**: 2.94%
- **Longest dictionary word**: `antidisestablishmentarianism` (28 characters)
- **Most repeated word**: `i` (repeated 6,339 times)

### Song Statistics
- **Song with most total words**: `eminem_rapgod.txt` (1,546 words)
- **Song with least total words**: `eminem_trapped.txt` (206 words)
- **Song with most unique words**: `eminem_shadyxv.txt` (610 unique words)
- **Song with least unique words**: `eminem_itsbeenreal.txt` (127 unique words)
- **Average total words per song**: 812.80
- **Average unique words per song**: 338.10

## Song Similarity Analysis

The similarity between songs was calculated using both Jaccard and Cosine similarity measures to understand word overlap and usage between songs.

### Jaccard Similarity
- **Most similar songs**: `eminem_hailiessong.txt` and `eminem_saygoodbyehollywood.txt` (similarity: 0.2665)
- **Least similar songs**: `eminem_shadyxv.txt` and `eminem_trapped.txt` (similarity: 0.0707)

### Cosine Similarity
- **Most similar songs**: `eminem_offended.txt` and `eminem_theringer.txt` (similarity: 0.9027)
- **Least similar songs**: `eminem_beautifulpain.txt` and `eminem_fack.txt` (similarity: 0.2171)

### Common Words Between Songs
- **Songs with most similar words**: `eminem_badguy.txt` and `eminem_rapgod.txt` (183 common words)
- **Songs with least similar words**: `eminem_fack.txt` and `eminem_trapped.txt` (29 common words)

## Lexicon and Custom Words

During the analysis, any words not found in the dictionary were saved to a custom lexicon. This lexicon includes slang, misspelled words, or unique words that Eminem frequently uses.

- **Custom lexicon saved to**: `eminem_lexicon_custom.txt`
- **Known words used by Eminem saved to**: `known_words_eminem_has_used.txt`

## Conclusion

This analysis provides an in-depth look into Eminem's lyrical content, showcasing the diversity in his vocabulary, the commonality of words across songs, and how certain songs share more in common with one another in terms of word usage. The project highlights his creative use of language, incorporating a mix of standard words and unique slang that set his lyrics apart.

---

**Image Placeholder for Visual Representation**

Feel free to dive into the lexicon or explore individual song analysis files for further insights!
