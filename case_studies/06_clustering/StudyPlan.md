# Case Study 06 — Clustering: k-Means vs Spectral Graph Theory

## Objective

Compare k-means clustering with spectral clustering (graph Laplacian approach)
on synthetic and real datasets. Demonstrate when Euclidean-distance-based methods
fail and how spectral methods recover structure by reasoning about connectivity
rather than proximity.

## Why This Comparison Works

k-means and spectral clustering solve the same problem — partition data into
groups — but with fundamentally different assumptions:

| Method | Assumption | Strength | Weakness |
|--------|-----------|----------|----------|
| k-means | Clusters are convex, roughly spherical | Fast, simple, scalable | Fails on non-convex structure |
| Spectral clustering | Clusters are connected components in a similarity graph | Handles arbitrary cluster shapes | Slower (eigendecomposition), requires choosing similarity kernel |

Spectral clustering actually *contains* k-means as a sub-step: it builds a
similarity graph, computes eigenvectors of the graph Laplacian to embed points
into a new space, then runs k-means in that eigenspace. So spectral is a
generalization, not a replacement.

## Key Concepts

1. **k-means** — minimize within-cluster variance (sum of squared distances to centroids)
2. **Similarity graph** — encode pairwise relationships (ε-neighborhood, k-NN, or Gaussian kernel)
3. **Graph Laplacian** — L = D - W (degree matrix minus adjacency/weight matrix)
4. **Fiedler vector** — second-smallest eigenvector of L; encodes the best binary partition
5. **Spectral embedding** — use the first k eigenvectors of L as new coordinates
6. **Normalized cuts** — the optimization problem that spectral clustering approximately solves

## Datasets for Demonstration

**Synthetic (where the comparison is most vivid):**
- Concentric rings (2D) — k-means assigns by angle, spectral by ring
- Interleaved half-moons — k-means splits vertically, spectral follows curvature
- Spirals — extreme non-convexity
- Well-separated Gaussian blobs — both methods agree (baseline)

**Real (optional, for grounding):**
- Image segmentation (small patch → pixel affinity graph)
- Social network community detection
- Glacier flow regime segmentation (connecting to case study 03)

## Steps

1. Generate synthetic datasets (scikit-learn `make_moons`, `make_circles`, custom spirals)
2. Run k-means, visualize assignments — show failure cases
3. Build similarity graph (Gaussian kernel, tune σ)
4. Compute graph Laplacian and its eigenvalues/eigenvectors
5. Visualize the eigenvalue spectrum (the "gap" indicates cluster count)
6. Embed in eigenspace, run k-means there — show success
7. Side-by-side comparison plots
8. Explore sensitivity to hyperparameters (σ, number of neighbors, k)
9. (Optional) Apply to a real dataset

## The Mathematics

### Graph Laplacian

Given n data points and a weight matrix W (where W_ij = similarity between i and j):

```
D = diag(d_1, ..., d_n)    where d_i = Σ_j W_ij  (degree of node i)
L = D - W                   (unnormalized Laplacian)
L_sym = D^{-1/2} L D^{-1/2} (symmetric normalized Laplacian)
```

Properties of L:
- Positive semi-definite
- Smallest eigenvalue is 0 (eigenvector = constant)
- Number of zero eigenvalues = number of connected components
- The Fiedler vector (2nd eigenvector) gives the optimal 2-partition

### Why It Works

k-means minimizes Σ ||x_i - μ_k||² — this is a Euclidean criterion. Points in
the same cluster must be *close* in the original space.

Spectral clustering minimizes a graph cut criterion: separate clusters by cutting
the fewest (or weakest) edges. Points in the same cluster must be *connected*,
not necessarily close. The eigenvectors of L provide the relaxed solution to this
combinatorial optimization problem.

## What We'll Use

| Component | Choice |
|-----------|--------|
| Algorithms | scikit-learn (KMeans, SpectralClustering) |
| Graph/matrix ops | numpy, scipy.sparse |
| Visualization | matplotlib |
| Framework | No neural network needed — this is classical ML / linear algebra |

## Connection to the Broader Sequence

This case study is *not* a neural network. It's here because:
- It grounds the concept of "what clustering actually is" before seeing how
  neural approaches (autoencoders, contrastive learning) address the same problem
- The graph Laplacian appears again in Graph Neural Networks (GNNs)
- Spectral methods connect to the eigenvalue/eigenvector intuition used in PCA,
  which underlies many dimensionality-reduction steps in ML pipelines
- It provides a crisp example of "when simple methods fail, what mathematical
  structure rescues you" — a recurring theme

## Presentation Context

CloudBank Cloud Clinic — demonstrating that not everything in ML is deep learning.
Classical methods with clean mathematical foundations still solve problems that
neural networks struggle with (small data, interpretability, guarantees).

## Status

🔲 Not started
