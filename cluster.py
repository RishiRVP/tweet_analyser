import pandas as pd
import nltk
from nltk.corpus import stopwords 
import gensim
from gensim import corpora
from gensim.models import CoherenceModel
stopwords = set(stopwords.words('english'))
import warnings
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt
%matplotlib inline

tweetsInfo = pd.read_csv('AllTweetInfo.csv')

#Get Text for Topics
def MorePreprocessing(text):
    text_new = [t for t in text.split() if t not in stopwords]
    text_new = [t for t in text_new if not str.isnumeric(t)]
    
    return text_new
    
tweetsInfo['topic_text'] =tweetsInfo['text_features_new'].apply(MorePreprocessing)


t_list = tweetsInfo['topic_text'].tolist()
corpdict = corpora.Dictionary(t_list)

doc_term_matrix = [corpdict.doc2bow(doc) for doc in t_list]
corpora.MmCorpus.serialize('corpus.mm', doc_term_matrix)

Lda = gensim.models.ldamodel.LdaModel
ldamodel = Lda(doc_term_matrix, num_topics=20, id2word = corpdict)

# Visualize Models
import pyLDAvis
import pyLDAvis.gensim
pyLDAvis.enable_notebook()
corpora =  gensim.corpora.MmCorpus('corpus.mm')
vis =pyLDAvis.gensim.prepare(ldamodel, corpora, corpdict)
pyLDAvis.display(vis)