
# from sklearn import tree

# # Step 1: Collect Data
# # Features: [weight (grams), color (0 = red, 1 = orange)]
# features = [
#     [150, 0],  # Apple
#     [170, 0],  # Apple
#     [130, 1],  # Orange
#     [120, 1],  # Orange
# ]
# labels = ["apple", "apple", "orange", "orange"]

# # Step 2: Train a model
# clf = tree.DecisionTreeClassifier()
# clf = clf.fit(features, labels)

# # Step 3: Predict!
# print(clf.predict([[160, 0]]))  # Heavy and red-ish? Probably an apple!
# print(clf.predict([[115, 1]]))  # Light and orange? Probably an orange!

# from sklearn import tree
# import matplotlib.pyplot as plt
# plt.figure(figsize=(10, 6))
# tree.plot_tree(clf, feature_names=["weight", "color"], class_names=["apple", "orange"], filled=True)


from sklearn import tree
from sklearn.ensemble import RandomForestClassifier

# Step 1: Collect Data
# Features: [weight (grams), color (0 = red, 1 = orange)]
features = [
    [150, 0],  # Apple
    [170, 0],  # Apple
    [130, 1],  # Orange
    [120, 1],  # Orange
]
labels = ["apple", "appleddd", "orange", "orangeggg"]

# Step 2: Train a model
clf = RandomForestClassifier() # Using Random Forest instead of Decision Tree
clf = clf.fit(features, labels)

# Step 3: Predict!
print(clf.predict([[160, 0]]))  # Heavy and red-ish? Probably an apple!
print(clf.predict([[125, 1]]))  # Light and orange? Probably an orange!