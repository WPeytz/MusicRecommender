"""
Weighted K-Nearest Neighbors implementation
Allows different features to have different importance weights
"""

import pandas as pd
import numpy as np


def weighted_knn(
    candidates_df: pd.DataFrame,
    feature_columns: list[str],
    weight_columns: list[str],
    n_recommendations: int,
    target_features: np.ndarray = None
) -> list[int]:
    """
    Weighted K-Nearest Neighbors for music recommendations

    Args:
        candidates_df: DataFrame with candidate songs (typically ~1000 songs)
        feature_columns: List of feature column names (e.g., ['danceability', 'energy', ...])
        weight_columns: List of weight column names (e.g., ['danceability_weight', 'energy_weight', ...])
        n_recommendations: Number of songs to return
        target_features: Optional target feature vector. If None, uses mean of candidates

    Returns:
        List of indices (from candidates_df) of top N recommendations

    Example:
        feature_cols = ['danceability', 'energy', 'valence']
        weight_cols = ['danceability_weight', 'energy_weight', 'valence_weight']

        candidates_df:
            track_id  danceability  energy  valence  danceability_weight  energy_weight  valence_weight
            abc       0.8           0.7     0.6      1.5                  1.0            1.2
            def       0.7           0.8     0.5      1.5                  1.0            1.2
            ...
    """

    # Extract feature matrix (N_candidates x N_features)
    feature_matrix = candidates_df[feature_columns].values

    # Extract weight matrix (N_candidates x N_features)
    weight_matrix = candidates_df[weight_columns].values

    # If no target provided, use mean of candidates
    if target_features is None:
        target_features = np.mean(feature_matrix, axis=0)

    # Ensure target is 1D array
    target_features = np.array(target_features).flatten()

    # Calculate weighted distances
    distances = weighted_euclidean_distance(
        feature_matrix,
        target_features,
        weight_matrix
    )

    # Get indices of top N closest songs (smallest distances)
    top_indices = np.argsort(distances)[:n_recommendations]

    return top_indices.tolist()


def weighted_euclidean_distance(
    feature_matrix: np.ndarray,
    target_features: np.ndarray,
    weight_matrix: np.ndarray
) -> np.ndarray:
    """
    Calculate weighted Euclidean distance between target and all candidates

    Args:
        feature_matrix: (N_candidates, N_features) array of candidate features
        target_features: (N_features,) array of target features
        weight_matrix: (N_candidates, N_features) array of feature weights

    Returns:
        (N_candidates,) array of weighted distances

    Formula:
        d_i = sqrt(Σ_j w_ij * (f_ij - t_j)^2)

        where:
        - d_i = distance for candidate i
        - w_ij = weight for feature j of candidate i
        - f_ij = feature j value of candidate i
        - t_j = target feature j value
    """

    # Compute differences: (N_candidates, N_features)
    differences = feature_matrix - target_features

    # Square differences: (N_candidates, N_features)
    squared_differences = differences ** 2

    # Apply weights: (N_candidates, N_features)
    weighted_squared_differences = weight_matrix * squared_differences

    # Sum across features: (N_candidates,)
    sum_weighted_squared = np.sum(weighted_squared_differences, axis=1)

    # Take square root: (N_candidates,)
    distances = np.sqrt(sum_weighted_squared)

    return distances


def weighted_cosine_similarity(
    feature_matrix: np.ndarray,
    target_features: np.ndarray,
    weight_matrix: np.ndarray
) -> np.ndarray:
    """
    Calculate weighted cosine similarity between target and all candidates

    Args:
        feature_matrix: (N_candidates, N_features) array of candidate features
        target_features: (N_features,) array of target features
        weight_matrix: (N_candidates, N_features) array of feature weights

    Returns:
        (N_candidates,) array of weighted cosine similarities (higher = more similar)

    Formula:
        sim_i = (Σ_j w_ij * f_ij * t_j) / (||w*f|| * ||w*t||)
    """

    # Apply weights to features
    weighted_features = weight_matrix * feature_matrix  # (N_candidates, N_features)
    weighted_target = weight_matrix * target_features   # (N_candidates, N_features)

    # Compute dot products: (N_candidates,)
    dot_products = np.sum(weighted_features * weighted_target, axis=1)

    # Compute norms
    feature_norms = np.linalg.norm(weighted_features, axis=1)  # (N_candidates,)
    target_norms = np.linalg.norm(weighted_target, axis=1)     # (N_candidates,)

    # Avoid division by zero
    norms_product = feature_norms * target_norms
    norms_product = np.where(norms_product == 0, 1e-10, norms_product)

    # Compute similarities
    similarities = dot_products / norms_product

    return similarities


def weighted_knn_cosine(
    candidates_df: pd.DataFrame,
    feature_columns: list[str],
    weight_columns: list[str],
    n_recommendations: int,
    target_features: np.ndarray = None
) -> list[int]:
    """
    Weighted K-Nearest Neighbors using cosine similarity
    (Higher similarity = better match)

    Args:
        candidates_df: DataFrame with candidate songs
        feature_columns: List of feature column names
        weight_columns: List of weight column names
        n_recommendations: Number of songs to return
        target_features: Optional target feature vector

    Returns:
        List of indices of top N recommendations
    """

    # Extract matrices
    feature_matrix = candidates_df[feature_columns].values
    weight_matrix = candidates_df[weight_columns].values

    # If no target provided, use mean
    if target_features is None:
        target_features = np.mean(feature_matrix, axis=0)

    target_features = np.array(target_features).flatten()

    # Calculate weighted cosine similarities
    similarities = weighted_cosine_similarity(
        feature_matrix,
        target_features,
        weight_matrix
    )

    # Get indices of top N most similar songs (highest similarities)
    top_indices = np.argsort(similarities)[::-1][:n_recommendations]

    return top_indices.tolist()


# Example usage and testing
if __name__ == "__main__":
    # Create sample data
    np.random.seed(42)
    n_candidates = 1000

    sample_data = {
        'track_id': [f'track_{i}' for i in range(n_candidates)],
        'danceability': np.random.rand(n_candidates),
        'energy': np.random.rand(n_candidates),
        'valence': np.random.rand(n_candidates),
        'acousticness': np.random.rand(n_candidates),
        'tempo_normalized': np.random.rand(n_candidates),
        # Weights - different importance for each feature
        'danceability_weight': np.full(n_candidates, 1.5),  # High importance
        'energy_weight': np.full(n_candidates, 1.5),        # High importance
        'valence_weight': np.full(n_candidates, 1.2),       # Medium-high importance
        'acousticness_weight': np.full(n_candidates, 1.0),  # Normal importance
        'tempo_weight': np.full(n_candidates, 0.8),         # Lower importance
    }

    candidates_df = pd.DataFrame(sample_data)

    # Define feature and weight columns
    feature_cols = ['danceability', 'energy', 'valence', 'acousticness', 'tempo_normalized']
    weight_cols = ['danceability_weight', 'energy_weight', 'valence_weight',
                   'acousticness_weight', 'tempo_weight']

    # Target profile (e.g., from input playlist)
    target = np.array([0.8, 0.7, 0.6, 0.3, 0.5])

    print("="*80)
    print("  WEIGHTED KNN EXAMPLE")
    print("="*80)

    # Method 1: Euclidean distance
    print("\n1. Using Weighted Euclidean Distance:")
    top_indices_euclidean = weighted_knn(
        candidates_df,
        feature_cols,
        weight_cols,
        n_recommendations=5,
        target_features=target
    )

    print(f"\nTop 5 recommendations (indices): {top_indices_euclidean}")
    print("\nRecommended songs:")
    for i, idx in enumerate(top_indices_euclidean, 1):
        row = candidates_df.iloc[idx]
        print(f"{i}. {row['track_id']}")
        print(f"   Features: dance={row['danceability']:.2f}, energy={row['energy']:.2f}, "
              f"valence={row['valence']:.2f}")

        # Calculate actual distance
        features = candidates_df.iloc[idx][feature_cols].values
        weights = candidates_df.iloc[idx][weight_cols].values
        diff = features - target
        weighted_dist = np.sqrt(np.sum(weights * (diff ** 2)))
        print(f"   Weighted distance: {weighted_dist:.4f}")

    # Method 2: Cosine similarity
    print("\n2. Using Weighted Cosine Similarity:")
    top_indices_cosine = weighted_knn_cosine(
        candidates_df,
        feature_cols,
        weight_cols,
        n_recommendations=5,
        target_features=target
    )

    print(f"\nTop 5 recommendations (indices): {top_indices_cosine}")
    print("\nRecommended songs:")
    for i, idx in enumerate(top_indices_cosine, 1):
        row = candidates_df.iloc[idx]
        print(f"{i}. {row['track_id']}")
        print(f"   Features: dance={row['danceability']:.2f}, energy={row['energy']:.2f}, "
              f"valence={row['valence']:.2f}")

        # Calculate actual similarity
        features = candidates_df.iloc[idx][feature_cols].values
        weights = candidates_df.iloc[idx][weight_cols].values
        weighted_feats = weights * features
        weighted_target = weights * target
        similarity = np.dot(weighted_feats, weighted_target) / (
            np.linalg.norm(weighted_feats) * np.linalg.norm(weighted_target)
        )
        print(f"   Weighted similarity: {similarity:.4f}")

    print("\n" + "="*80)
    print("  WEIGHT IMPACT DEMONSTRATION")
    print("="*80)

    # Show how changing weights affects results
    print("\nOriginal weights:")
    print(f"  Danceability: 1.5 (high importance)")
    print(f"  Energy: 1.5 (high importance)")
    print(f"  Valence: 1.2 (medium importance)")
    print(f"  Acousticness: 1.0 (normal importance)")
    print(f"  Tempo: 0.8 (low importance)")

    # Modify weights - make acousticness very important
    modified_data = candidates_df.copy()
    modified_data['acousticness_weight'] = 3.0  # Very high importance
    modified_data['danceability_weight'] = 0.5  # Low importance

    print("\nModified weights (acousticness now most important):")
    print(f"  Acousticness: 3.0 (VERY high importance)")
    print(f"  Danceability: 0.5 (low importance)")

    top_indices_modified = weighted_knn_cosine(
        modified_data,
        feature_cols,
        weight_cols,
        n_recommendations=5,
        target_features=target
    )

    print(f"\nTop 5 with modified weights (indices): {top_indices_modified}")
    print("(Notice how recommendations change based on weight adjustments)")

    print("\n" + "="*80)
    print("✅ Weighted KNN implementation complete!")
    print("="*80)
