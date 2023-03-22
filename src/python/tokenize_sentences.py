import nltk

# prep
nltk.download("punkt")
nltk.sent_tokenize(a)

# paragraph
a = 'This is a test... a testy test. Dr. tester thinks of things as tests. E. K. Tester is an exemplary kind tester.'

# tokenize by sentence
nltk.sent_tokenize(a)

# tokenize by word
nltk.TweetTokenizer().tokenize(a)
