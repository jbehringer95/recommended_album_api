import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


def get_recommendations(df, column, value, value_list, limit=100):
    values = ', '.join([str(elem) for elem in value_list])
    df = df.append({'Album':value,
                    'Artist':value,
                    'Album_Genres_Descriptors':values},
                    ignore_index=True)

    tf = TfidfVectorizer(analyzer='word',
                         ngram_range=(1, 3),
                         min_df=0, 
                         stop_words='english')

    tfidf_matrix = tf.fit_transform(df['Album_Genres_Descriptors'])

    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

    indices = pd.Series(df.index, index=df[column]).drop_duplicates()

    target_index = indices[value]

    cosine_similarity_scores = list(enumerate(cosine_similarities[target_index]))

    cosine_similarity_scores = sorted(cosine_similarity_scores,
                                      key=lambda x: x[1],
                                      reverse=True)

    cosine_similarity_scores = cosine_similarity_scores[0:limit]

    index = (x[0] for x in cosine_similarity_scores)
    scores = (x[1] for x in cosine_similarity_scores)

    recommendation_indices = [i[0] for i in cosine_similarity_scores]

    recommendations = df[column].iloc[recommendation_indices]

    df = pd.DataFrame(list(zip(index, recommendations, scores)),
                      columns=['index','Album', 'Scores'])

    return df
