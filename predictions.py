import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


def get_recommendations(df, column, value, value_list, limit=10):

    # Turning value_list from a list to a string
    values = ', '.join([str(elem) for elem in value_list])
    
    # Adding a new row to the end of the Dataframe
    df = df.append({'Album':value, 'Artist':value, 'Album_Genres_Descriptors':values}, ignore_index = True)

    # Vectorizing the Album_Genres_Descriptors column
    tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 3),min_df=0, stop_words='english')
    tfidf_matrix = tf.fit_transform(df['Album_Genres_Descriptors'])
    
    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

    indices = pd.Series(df.index, index=df[column]).drop_duplicates()

    # Get the index for the target value
    target_index = indices[value]

    # Get the cosine similarity scores for the target value
    cosine_similarity_scores = list(enumerate(cosine_similarities[target_index]))

    # Sort the cosine similarities in order of closest similarity
    cosine_similarity_scores = sorted(cosine_similarity_scores, key=lambda x: x[1], reverse=True)

    # Return tuple of the requested closest scores excluding the target item and index
    cosine_similarity_scores = cosine_similarity_scores[0:limit]

    # Extract the tuple values
    index = (x[0] for x in cosine_similarity_scores)
    scores = (x[1] for x in cosine_similarity_scores)

    # Get the indices for the closest items
    recommendation_indices = [i[0] for i in cosine_similarity_scores]

    # Get the actutal recommendations
    recommendations = df[column].iloc[recommendation_indices]

    # Return a dataframe
    df = pd.DataFrame(list(zip(index, recommendations, scores)), 
                      columns=['index','Album', 'Scores'])

    return df
