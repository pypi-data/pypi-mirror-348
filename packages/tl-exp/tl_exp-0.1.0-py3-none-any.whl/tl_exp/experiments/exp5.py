import gensim
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize
import nltk
import multiprocessing

print("⏳ Downloading NLTK data...")
nltk.download('punkt')
nltk.download('punkt_tab')
print("✅ NLTK data downloaded successfully!")

corpus = [
    "Word embeddings are a type of word representation.",
    "Word2Vec is a popular word embedding model.",
    "GloVe is another word embedding model.",
    "Both Word2Vec and GloVe capture semantic relationships."
]

print("📜 Corpus defined successfully!")
print("Sample sentences:", corpus[:2])

try:
    tokenized_corpus = [word_tokenize(sentence.lower()) for sentence in corpus]
    print("🔡 Tokenization successful!")
    print("Sample tokenized sentence:", tokenized_corpus[0])
except LookupError:
    from nltk.tokenize import RegexpTokenizer
    tokenizer = RegexpTokenizer(r'\w+')
    tokenized_corpus = [tokenizer.tokenize(sentence.lower()) for sentence in corpus]
    print("⚠️ Used fallback tokenizer (NLTK punkt failed).")
    print("Sample tokenized sentence:", tokenized_corpus[0])


vector_size = 100  # Dimension of word vectors
window_size = 5    # Context window size
min_count = 1      # Minimum word frequency
workers = multiprocessing.cpu_count()  # Use all CPU cores
epochs = 100       # Training iterations

print("⚙️ Word2Vec parameters set:")
print(f"- Vector size: {vector_size}")
print(f"- Window size: {window_size}")
print(f"- Min word count: {min_count}")
print(f"- Workers: {workers}")
print(f"- Epochs: {epochs}")

# Step 7: Check vocabulary and sample outputs
vocab = list(word2vec_model.wv.key_to_index.keys())
print(f" Vocabulary size: {len(vocab)} words")
print("Sample words in vocab:", vocab[:5])  # First 5 words

# Check if 'word' is in vocab
if 'word' in word2vec_model.wv:
    print("\n Most similar words to 'word':")
    print(word2vec_model.wv.most_similar("word", topn=3))  # Top 3 similar words
else:
    print("'word' not in vocabulary.")

# Get vector for 'embedding'
if 'embedding' in word2vec_model.wv:
    print("\n Vector for 'embedding' (first 5 dims):")
    print(word2vec_model.wv["embedding"][:5])  # Show first 5 dimensions
else:
    print("'embedding' not in vocabulary.")

## **GLOVE MODEL**

!wget http://nlp.stanford.edu/data/glove.6B.zip
!unzip glove.6B.zip

import numpy as np

def load_glove_embeddings(path):
    embeddings = {}
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            values = line.split()
            word = values[0]
            vector = np.asarray(values[1:], dtype='float32')
            embeddings[word] = vector
    return embeddings

glove_path = 'glove.6B.100d.txt'
glove_embeddings = load_glove_embeddings(glove_path)

print(f"Loaded {len(glove_embeddings)} word vectors")
print("Vector for 'king':", glove_embeddings['king'][:5])  # Show first 5 dimensions
print("Most similar to 'paris':", sorted(
    [(word, np.dot(glove_embeddings['paris'], glove_embeddings[word]))
     for word in ['france', 'london', 'berlin']],
    key=lambda x: -x[1]
))

