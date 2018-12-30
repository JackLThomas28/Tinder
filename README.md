# Machine Learning with Tinder - Information Retrieval (CS4320)
This project collects information from Tinder profiles, analyzes the biography section text, and applies clustering to determine popular topics expressed.

## Results
### Top 5 Topics Expressed
![](topics.png)  

### Collection Statistics
* 2790 total profiles collected
* 2060 profiles with usable biography text
<img src="no_bio_percentage.png" alt="No Bio Percentage" width=50% height=auto/>

## Procedure
### Data Collection
1. Obtain a Facebook token to authenticate with the Tinder API.
2. Request the recommended profiles.
3. Save the biography text to a JSON file.
4. "Like" each recommended profile.
5. Repeat steps 2 - 3 until no more likes available.
6. Repeat steps 2 - 5 when more likes are available (every 12 hours).
### Data Analysis
1. Preprocess the text (Remove: Stop Words, Punctuation, Emojis, and Numbers).
2. Feature extraction from the documents (Each Tinder profile is a document): TF-IDF.
3. Perform clustering: Truncated SVD (Latent Semantic Analysis)