# Evaluation Criteria & Optimization Strategy

## Understanding the Judging Criteria

### 1. NDCG@5 (Normalized Discounted Cumulative Gain)

**What it measures:**
- How well your model predicts the last 5 songs that were removed from human-curated playlists
- **Order matters** - Getting the right songs in the right order scores better
- Scale: 0.0 (worst) to 1.0 (perfect)

**How NDCG@5 works:**
```
NDCG@5 = DCG@5 / IDCG@5

Where:
- DCG@5 = Σ(relevance_i / log2(position_i + 1)) for top 5 recommendations
- IDCG@5 = Best possible DCG (if you got all 5 songs in perfect order)
- Relevance = 1 if song was in the removed 5, 0 otherwise
```

**Example:**
```
Removed songs: [A, B, C, D, E]
Your recommendations: [A, X, B, C, Y]

Position 1: A (relevant) → 1/log2(2) = 1.0
Position 2: X (not relevant) → 0/log2(3) = 0.0
Position 3: B (relevant) → 1/log2(4) = 0.5
Position 4: C (relevant) → 1/log2(5) = 0.43
Position 5: Y (not relevant) → 0/log2(6) = 0.0

DCG = 1.0 + 0.0 + 0.5 + 0.43 + 0.0 = 1.93
IDCG = 1.0 + 0.63 + 0.5 + 0.43 + 0.39 = 2.95
NDCG@5 = 1.93 / 2.95 = 0.65
```

**Key insights:**
- Earlier positions are weighted more heavily
- Getting the #1 song right is most important
- Order of recommendations matters

### 2. Performance (Speed)

**What it measures:**
- Time to return recommendations
- Comparison against a baseline model

**Current performance:**
- Initialization: ~2-3 seconds (one-time cost)
- Per-query: ~0.1-0.2 seconds
- Bottleneck: KNN search across 89,740 tracks

**Optimization strategies:**
- ✅ Already using efficient KNN with brute-force cosine (fast for this size)
- ✅ Pre-computed and normalized feature matrix
- ✅ Vectorized numpy operations
- Potential: Reduce candidate pool if needed

### 3. Explainability

**What it requires:**
- Explain to non-technical stakeholders
- How the model works
- How it reaches recommendations

**Key concepts to explain:**
- Audio features (in simple terms)
- Similarity matching
- Why certain songs are recommended

---

## Our Current Strategy

### ✅ Strengths for NDCG@5

1. **target_artist boost (1.5x)** - Playlists often have repeated artists
2. **Genre matching (1.1x)** - Playlists tend to be genre-coherent
3. **Playlist aggregation** - Combines all input songs to find the "vibe"
4. **Multi-feature similarity** - Uses 9 audio features for nuanced matching
5. **Popularity boost** - Slightly favors popular tracks

### 🎯 Potential Improvements for NDCG@5

1. **Tune boost parameters**
   - Current: artist=1.5x, genre=1.1x, popularity=1.1x
   - Could experiment with: artist=2.0x, genre=1.2x

2. **Consider sequential patterns**
   - Analyze if playlists have patterns (e.g., similar energy progression)
   - Weight recent songs more heavily

3. **Diversity penalty for top 5**
   - Ensure top 5 aren't all too similar
   - Use MMR (Maximal Marginal Relevance)

4. **Artist repetition analysis**
   - If playlist has same artist multiple times, strongly boost that artist

5. **Temporal features**
   - Consider release dates (playlists might favor recent songs)

### ⚡ Performance Optimization

Current optimizations:
- ✅ Efficient KNN with cosine metric
- ✅ Normalized feature vectors (avoid redundant computation)
- ✅ Vectorized operations
- ✅ Pre-built index

Potential optimizations:
- Reduce candidate pool from 1000 to 500 (faster, might reduce quality slightly)
- Cache common queries
- Use approximate KNN (FAISS) for larger datasets

### 📊 Explainability Framework

**Simple explanation structure:**

1. **What**: Content-based music recommender
2. **How**: Analyzes song characteristics (like DNA matching for music)
3. **Why**: Finds songs that "feel" similar to your playlist

**Audio features in plain language:**
- Danceability → How easy is it to dance to?
- Energy → How intense/loud is the song?
- Valence → How happy/positive does it sound?
- Acousticness → Electric instruments vs. acoustic?
- Tempo → How fast is the beat?

---

## Action Items

### Before Evaluation

- [ ] Test with different boost parameters
- [ ] Benchmark exact performance times
- [ ] Create presentation slides for explainability
- [ ] Test with sample playlists
- [ ] Verify no crashes with edge cases

### During Evaluation

- [ ] Monitor NDCG@5 scores
- [ ] Track performance times
- [ ] Be ready to explain decisions

### Presentation Talking Points

1. **Simple analogy**: "Like Spotify's song DNA matching"
2. **Audio features**: Visual graphs showing how songs match
3. **Example**: Show a real playlist and explain why each recommendation makes sense
4. **Trust**: Explain the math is working behind the scenes, but focus on intuition

---

## Competitive Advantages

1. **Multi-signal approach**: Uses audio features + artist + genre + popularity
2. **Fast**: Sub-second recommendations
3. **Explainable**: Clear reason for each recommendation
4. **Robust**: Handles various playlist sizes and styles

## Risk Mitigation

**Risk**: NDCG@5 might be low if removed songs are very diverse
**Mitigation**: Target_artist boost helps capture artist patterns

**Risk**: Performance might lag on slow hardware
**Mitigation**: Already optimized, can reduce candidate pool if needed

**Risk**: Stakeholders don't understand the model
**Mitigation**: Prepare clear analogies and visual examples

---

## Expected Performance

**NDCG@5 estimate**: 0.3-0.5
- Content-based methods typically score 0.2-0.4
- Our artist/genre boosts should push us higher

**Performance**: < 0.2 seconds per query
- Well within acceptable range
- Baseline is likely 1-2 seconds

**Explainability**: Strong
- Clear audio features
- Visual examples
- Simple analogies
