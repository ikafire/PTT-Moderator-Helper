from NBC import NaiveBayesClassifier

nbc = NaiveBayesClassifier()
nbc.train()
print(nbc.classify(''))
