# ===============================
# IMPORT LIBRARIES
# ===============================

import pandas as pd
import numpy as np

# Machine learning model
from sklearn.neighbors import NearestNeighbors

# Sparse matrix (memory optimization)
from scipy.sparse import csr_matrix

# ===============================
# LOAD DATASETS
# ===============================

products = pd.read_csv('/products.csv')
orders = pd.read_csv('/orders.csv')
order_products = pd.read_csv('/order_products__train.csv')

# Show dataset samples
print(order_products.head())

# Merge dataset
data = pd.merge(order_products, products, on='product_id')

# Take a sample of orders to reduce memory usage
sample_orders = data['order_id'].drop_duplicates().sample(10000)

# Filter dataset
data_sample = data[data['order_id'].isin(sample_orders)]

print("Sample dataset size:", data_sample.shape)

# ===============================
# CREATE TRANSACTION MATRIX
# ===============================

basket = data_sample.pivot_table(
    index='order_id',
    columns='product_name',
    values='product_id',
    aggfunc='count'
)

basket = basket.fillna(0)

basket = (basket > 0).astype(int)

print(basket.head())

# ===============================
# SPARSE MATRIX
# ===============================

basket_sparse = csr_matrix(basket)

# ===============================
# TRAIN KNN MODEL
# ===============================

model = NearestNeighbors(
    metric='cosine',
    algorithm='brute'
)

model.fit(basket_sparse)

print("KNN Model Training Completed")

# ===============================
# PRODUCT RECOMMENDATION FUNCTION
# ===============================

def recommend_products(order_number, n_recommendations=5):

    distances, indices = model.kneighbors(
        basket_sparse[order_number],
        n_neighbors=n_recommendations+1
    )

    print("\nRecommended Similar Orders:\n")

    for i in range(1, len(indices.flatten())):

        print("Recommendation", i)

        order = basket.iloc[indices.flatten()[i]]

        products = order[order == 1].index.tolist()

        print(products)
        print("------------")

        # Example recommendation

recommend_products(10)

import matplotlib.pyplot as plt

# Top purchased products

top_products = data['product_name'].value_counts().head(10)

top_products.plot(kind='bar')

plt.title("Top 10 Purchased Products")
plt.xlabel("Products")
plt.ylabel("Frequency")

plt.show()