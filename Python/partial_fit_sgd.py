""" 
Partial fit of SKlearn

If you have data that does not fit in memory, instead of using
SVC from sklearn, you can use the SGD with partial fit as follows

For further information, check out
http://scikit-learn.org/stable/modules/scaling_strategies.html
"""

from sklearn.linear_model import SGDClassifier
from sklearn.datasets import make_blobs

# make some fake data
X, y = make_blobs(n_samples=1000010,
                  random_state=0)

# train on a subset of the data at a time
clf = SGDClassifier()
for i in range(10):
    subset = slice(100000 * i, 100000 * (i + 1))
    clf.partial_fit(X[subset], y[subset], classes=np.unique(y))

# predict on unseen data
y_pred = clf.predict(X[-10:])

print(y_pred)
# [2 0 1 2 2 2 1 0 1 1]

print(y[-10:])
# [2 0 1 2 2 2 1 0 1 1]
