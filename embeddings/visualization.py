import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from search import load_embeddings

def visualize_embeddings(embeddings):
    # Extract embedding vectors and prompts
    vectors = [entry["embedding"] for entry in embeddings]
    prompts = [entry["prompt"] for entry in embeddings]

    # Reduce dimensionality
    print("Reducing dimensionality...")
    pca = PCA(n_components=21).fit_transform(vectors)  # Step 1: PCA for initial reduction
    tsne = TSNE(n_components=2, perplexity=20, random_state=42).fit_transform(pca)  # Step 2: t-SNE for 2D projection

    # Plot the results
    print("Plotting the embeddings...")
    plt.figure(figsize=(12, 8))
    plt.scatter(tsne[:, 0], tsne[:, 1], c='blue', alpha=0.7)

    for i, prompt in enumerate(prompts):
        plt.annotate(prompt[:30] + "...", (tsne[i, 0], tsne[i, 1]), fontsize=8, alpha=0.6)

    plt.title("Embeddings Visualization")
    plt.xlabel("Dimension 1")
    plt.ylabel("Dimension 2")
    plt.show()

# Example Usage
def visualize_example():
    print("Loading embeddings for visualization...")
    embeddings_file = "data\embeddings.json"
    embeddings = load_embeddings(embeddings_file)
    visualize_embeddings(embeddings)

if __name__ == "__main__":
    visualize_example()
