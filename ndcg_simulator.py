"""
NDCG@5 Simulator - Understand how NDCG@5 scoring works
This helps you understand what the evaluation metric measures
"""

import numpy as np

def calculate_dcg(relevances, k=5):
    """Calculate Discounted Cumulative Gain"""
    dcg = 0.0
    for i, rel in enumerate(relevances[:k], start=1):
        dcg += rel / np.log2(i + 1)
    return dcg

def calculate_ndcg(recommended_ids, actual_removed_ids, k=5):
    """
    Calculate NDCG@5

    Args:
        recommended_ids: List of recommended track IDs (your model's output)
        actual_removed_ids: List of actual removed track IDs (ground truth)
        k: Number of recommendations to consider (5 for this evaluation)

    Returns:
        NDCG score between 0 and 1
    """
    # Create relevance scores (1 if in removed set, 0 otherwise)
    relevances = [1 if rec_id in actual_removed_ids else 0
                  for rec_id in recommended_ids[:k]]

    # Calculate DCG (your score)
    dcg = calculate_dcg(relevances, k)

    # Calculate IDCG (perfect score - all relevant items first)
    # Best case: all k recommendations are relevant
    num_relevant = min(len(actual_removed_ids), k)
    ideal_relevances = [1] * num_relevant + [0] * (k - num_relevant)
    idcg = calculate_dcg(ideal_relevances, k)

    # NDCG = DCG / IDCG
    if idcg == 0:
        return 0.0

    return dcg / idcg

def print_scenario(title, recommended, removed):
    """Print a scenario with NDCG calculation"""
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}")

    print(f"\nRemoved songs (ground truth): {removed}")
    print(f"Your recommendations: {recommended}")

    ndcg = calculate_ndcg(recommended, removed, k=5)

    print(f"\nBreakdown:")
    for i, rec in enumerate(recommended[:5], start=1):
        relevant = "✓ RELEVANT" if rec in removed else "✗ not relevant"
        position_weight = 1 / np.log2(i + 1)
        contribution = position_weight if rec in removed else 0
        print(f"  Position {i}: '{rec}' {relevant:20s} "
              f"(weight={position_weight:.3f}, contrib={contribution:.3f})")

    print(f"\n  NDCG@5 = {ndcg:.4f}")

    if ndcg == 1.0:
        print("  ⭐ PERFECT SCORE!")
    elif ndcg >= 0.8:
        print("  🎉 EXCELLENT!")
    elif ndcg >= 0.6:
        print("  ✅ GOOD")
    elif ndcg >= 0.4:
        print("  👍 DECENT")
    elif ndcg >= 0.2:
        print("  ⚠️  NEEDS IMPROVEMENT")
    else:
        print("  ❌ POOR")

    return ndcg

# Example scenarios
print("="*80)
print("  NDCG@5 SIMULATOR - Understanding the Evaluation Metric")
print("="*80)
print("\nThis script shows how NDCG@5 scores different recommendation scenarios.")
print("Higher scores are better. Order matters - earlier positions count more!")

# Scenario 1: Perfect recommendations
print_scenario(
    "SCENARIO 1: Perfect Recommendations",
    recommended=['A', 'B', 'C', 'D', 'E'],
    removed=['A', 'B', 'C', 'D', 'E']
)

# Scenario 2: All correct but wrong order
print_scenario(
    "SCENARIO 2: All Correct but Reversed Order",
    recommended=['E', 'D', 'C', 'B', 'A'],
    removed=['A', 'B', 'C', 'D', 'E']
)

# Scenario 3: Only first recommendation correct
print_scenario(
    "SCENARIO 3: Only First Song Correct",
    recommended=['A', 'X', 'Y', 'Z', 'W'],
    removed=['A', 'B', 'C', 'D', 'E']
)

# Scenario 4: Mixed results
print_scenario(
    "SCENARIO 4: Mixed Results (3 out of 5 correct)",
    recommended=['A', 'X', 'B', 'Y', 'C'],
    removed=['A', 'B', 'C', 'D', 'E']
)

# Scenario 5: Good but not perfect
print_scenario(
    "SCENARIO 5: 4 out of 5 correct, good order",
    recommended=['A', 'B', 'C', 'D', 'X'],
    removed=['A', 'B', 'C', 'D', 'E']
)

# Scenario 6: Last position correct
print_scenario(
    "SCENARIO 6: Only Last Song Correct",
    recommended=['X', 'Y', 'Z', 'W', 'A'],
    removed=['A', 'B', 'C', 'D', 'E']
)

# Scenario 7: Realistic scenario
print_scenario(
    "SCENARIO 7: Realistic Scenario (2 correct in top positions)",
    recommended=['A', 'C', 'X', 'Y', 'Z'],
    removed=['A', 'B', 'C', 'D', 'E']
)

# Summary
print("\n" + "="*80)
print("  KEY INSIGHTS FOR OPTIMIZATION")
print("="*80)

print("""
1. POSITION MATTERS
   - Getting the #1 recommendation right contributes: 1.000
   - Getting the #2 recommendation right contributes: 0.631
   - Getting the #3 recommendation right contributes: 0.500
   - Getting the #4 recommendation right contributes: 0.431
   - Getting the #5 recommendation right contributes: 0.387

   → Focus on getting the TOP recommendations right!

2. PERFECT SCORE IS RARE
   - NDCG@5 = 1.0 requires all 5 recommendations correct and in perfect order
   - NDCG@5 = 0.8+ is excellent
   - NDCG@5 = 0.6+ is very good
   - NDCG@5 = 0.4+ is decent

3. OPTIMIZATION STRATEGIES

   Strategy 1: ARTIST REPETITION
   - If playlist has Taylor Swift 3 times → strongly boost Taylor Swift
   - Our current boost: 1.5x → consider increasing to 2.0x

   Strategy 2: RECENT SONGS
   - Weight recent songs in playlist more heavily
   - They might indicate current preference

   Strategy 3: GENRE CONSISTENCY
   - If 90% of playlist is pop → strongly favor pop
   - Our current boost: 1.1x → consider genre-adaptive boosting

   Strategy 4: DIVERSITY PENALTY
   - Don't recommend 5 songs that are too similar to each other
   - Use MMR (Maximal Marginal Relevance)

   Strategy 5: POPULARITY + RECENCY
   - Removed songs might be recent popular hits
   - Balance similarity with trending songs

4. EXPECTED PERFORMANCE

   Content-based methods typically achieve:
   - Random baseline: ~0.05-0.10
   - Simple popularity: ~0.15-0.20
   - Content-based (ours): ~0.30-0.50
   - Collaborative filtering: ~0.40-0.60
   - Hybrid methods: ~0.50-0.70

   Our target: 0.35-0.50 (solid performance for content-based)
""")

print("="*80)
print("  TIP: When evaluation.py arrives, analyze which songs were removed")
print("       and look for patterns (repeated artists, genres, etc.)")
print("="*80)
