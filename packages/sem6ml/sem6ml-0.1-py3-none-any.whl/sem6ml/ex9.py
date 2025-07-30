# exercise1.py
import inspect
import sys

print("=== Code of sem6ml.exercise9 ===")
print(inspect.getsource(sys.modules[__name__]))

def run():
    print("Running K-Means Clustering Algorithm...")
    
    # Original K-Means implementation code
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from sklearn.cluster import KMeans

    # Sample dataset
    data = np.array([[2, 4], [4, 6], [4, 4], [6, 2], [8, 4]])
    
    # Apply K-Means with 2 clusters
    kmeans = KMeans(n_clusters=2, random_state=42)
    kmeans.fit(data)
    
    # Get cluster labels and centroids
    labels = kmeans.labels_
    centroids = kmeans.cluster_centers_
    
    # Print cluster information
    print("\nCluster Assignments:")
    for i, point in enumerate(data):
        print(f"Point {point} belongs to Cluster {labels[i]}")
    
    print("\nCluster Centroids:")
    for i, centroid in enumerate(centroids):
        print(f"Cluster {i} centroid at {centroid}")
    
    # Visualizing clusters
    plt.figure(figsize=(8, 6))
    plt.scatter(data[:, 0], data[:, 1], c=labels, cmap='viridis', 
               marker='o', s=100, edgecolors='k', label='Data Points')
    plt.scatter(centroids[:, 0], centroids[:, 1], c='red', 
               marker='X', s=200, label='Centroids')
    
    # Annotate each point with its coordinates
    for i, txt in enumerate(data):
        plt.annotate(f"{txt}", (data[i, 0]+0.1, data[i, 1]+0.1))
    
    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.title('K-Means Clustering (2 Clusters)')
    plt.legend()
    plt.grid(True)
    plt.show()