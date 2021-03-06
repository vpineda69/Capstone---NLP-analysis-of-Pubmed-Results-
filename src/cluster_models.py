from __future__ import division
from Bio import Medline
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from time import time
import matplotlib.pyplot as plt
import seaborn as sns

"""Code from medline_reader streamlined for clustering purposes"""
def abstract_dataframe(filename):
    """
    Input - file of Medline text output from Pubmed
    Output - DataFrame with PMID, Abstract, and Tokenized Abstract
    """
    pmid_ab_dict = medline_parser(filename)
    df = pd.DataFrame.from_dict(pmid_ab_dict, orient='index').reset_index()
    df.columns = ['PMID', 'Abstract']
    df = topic_extraction(df, 'Abstract') # after topic extraction
    # df.to_csv('../data/metab_LDA_NMF_labels', index=False, index_label=None)
    # tsne_algorithm(tfidf)
    # # """
    # Parallelized tokenizer and gene pairs functions gene-network analysis.
    # Original code used are commented out
    # """
    # df = parallel_tokenizer(df)
    # df = parallel_genepairs(df)
    # """create dictionary for networx_work"""
    # gene_dict = {entry[0]:entry[1:] for entry in df['gene_pairs'] if entry != None}
    # network_graph(gene_dict)


def medline_parser(filename):
    """extracts info from medline text file from pubmed"""
    pmid_abstract_dict = {}
    with open(filename) as handle:
        for record in Medline.parse(handle):
            if 'AB' in record.keys():
                pmid, abstract = record['PMID'], record['AB']
                pmid_abstract_dict[pmid] = abstract
        return pmid_abstract_dict

def topic_extraction(df, col_name):
    """
    Two algorithms for topic extraction -
    NMF and LatentDirichletAllocation(LDA).
    Need to tie in with K-means clustering
    """

    tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2,
                                       max_features=200,
                                       stop_words='english')
    tfidf = tfidf_vectorizer.fit_transform(df[col_name])

    # tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2,
    #                                 max_features=200,
    #                                 stop_words='english')
    # tf = tf_vectorizer.fit_transform(df[col_name])
    nmf = NMF(n_components=20, random_state=1,
            alpha=.1, l1_ratio=.5)
    tfidf_feature_names = tfidf_vectorizer.get_feature_names()
    nmf_w = nmf.fit_transform(tfidf)
    nmf_h = nmf.components_
    df['labels'] = nmf_w.argmax(axis=1) # this was the right code to get labels/clusters
    labels = df['labels'].values
    clustering_algorithm(tfidf, labels)
    # tsne_algorithm(tfidf) # feed the tsne algorithm
    # sns.distplot(df['labels'], kde=True)
    # plt.show()
    # print("\nTopics in NMF model:")
    # print_top_words(nmf, tfidf_feature_names)


    # lda = LatentDirichletAllocation(n_topics=40, max_iter=5,
    #                             learning_method='online',
    #                             learning_offset=50.,
    #                             random_state=0,
    #                             n_jobs=-1)
    # mod = lda.fit(tf)
    # comp = mod.components_
    # df['lda_topics'] = comp[:,0]
    # print("\nTopics in LDA model:")
    # tf_feature_names = tf_vectorizer.get_feature_names()
    # print_top_words(lda, tf_feature_names)
    # df = clustering_algorithm(df, tfidf, labels)
    return df

def print_top_words(model, feature_names, n_top_words=20):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print('End')

def clustering_algorithm(tfidf, labels):
    num_clusters = 20
    num_seeds = 20
    max_iterations = 300
    tsne_num_components = 20
    # km = KMeans(n_clusters=num_clusters, algorithm='full', n_jobs=-1, verbose=1)
    # mod = km.fit_transform(tfidf)
    # x, y = mod[0], mod[1]
    # print x
    # print y
    # centroids = mod.cluster_center_
    # mod_labels = mod.labels_
    # plt.scatter(x, y)
    # plt.show()
    X = tfidf.todense()
    tsne_mod = TSNE(n_components=20, verbose=1, init='pca')
    coords = tsne_mod.fit_transform(X)
    x, y = coords[:,0], coords[:, 1]
    plt.scatter(x, y, cmap=plt.cm.Spectral)
    plt.show()

if __name__ == "__main__":
    """first file is PLOS Genetics abstract through June 2017"""
    # abstract_dataframe("../capstone_files/pubmed_result_medline.txt")
    # abstract_dataframe("../capstone_files/pubmed_result_plos_med.txt")
    # abstract_dataframe("../capstone_files/pubmed_result_plos_one.txt")
    # abstract_dataframe("../capstone_files/nature_genetics_all.txt")
    abstract_dataframe("../capstone_files/metabolism_5year_reviews.txt")
