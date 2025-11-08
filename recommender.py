# from evaluation import evaluate
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from sklearn.neighbors import NearestNeighbors


class Recommender:

    clustering_columns = [
        "danceability",
        "energy",
        "speechiness",
        "acousticness",
        "instrumentalness",
    ]

    def __init__(self) -> None:
        self.df = pd.read_csv("dataset.csv")
        self.df["artists"] = self.df["artists"].str.split(";")
        self.df = self.df.dropna(subset=["artists", "track_name"])
        self.df = self.df.drop_duplicates(subset=["track_id"], keep="first")
        self.df = self.df.reset_index(drop=True)

        for column in self.clustering_columns:
            self.df[column] = MinMaxScaler().fit_transform(self.df[[column]])

    def get_recommendations(
        self,
        input_track_ids: list[str],
        n_recommendations: int,
        target_artist: set[str],
    ) -> list[str]:
        """
        Get recommendations based on multiple input songs

        Args:
            input_track_ids: List of track IDs to base recommendations on
            n_recommendations: Integer specifying how many songs to recommend
            target_artist: A set of artist names. This is a hint of which artists were removed from the playlist. You may use this set to recommend songs.

        Returns:
            List of recommended track IDs of length n_recommendations
            The list should be ordered by relevance (most relevant first)
        """

        playlist_clustering_df = pd.DataFrame(columns=["mean", "weight"])
        track_df = self.df[self.df["track_id"].isin(input_track_ids)]

        for col in self.clustering_columns:
            mean, weight = self.cluster_weight(track_df[col])
            playlist_clustering_df.loc[col] = {"mean": mean, "weight": weight}

        mask = self.df["artists"].apply(
            lambda artists: bool(set(artists) & target_artist)
        )
        possibility_df = self.df[mask]

        model = self.weighted_knn_fit(
            possibility_df[self.clustering_columns],
            playlist_clustering_df["weight"],
            n_recommendations,
        )

        distances, indices = self.query_weighted_knn(
            model,
            playlist_clustering_df["weight"],
            self.df[self.clustering_columns].iloc[10],
        )

        print(indices)

        return possibility_df.iloc[indices]

        # return recommended_track_ids

    def cluster_weight(self, values, k=5):
        values = np.array(values)
        mean = np.mean(values)
        std = np.std(values)
        weight = np.exp(-k * std)
        return mean, weight

    def weighted_knn_fit(self, X, feature_weights, n_neighbors=5):
        # Scale features by sqrt(weight)
        # X_weighted = X * np.sqrt(feature_weights)
        # model = NearestNeighbors(n_neighbors=n_neighbors, metric="euclidean")
        # model.fit(X_weighted)
        # return model

        X_weighted = X.values * np.sqrt(feature_weights.values)

        # print(x_weighted)

        model = NearestNeighbors(n_neighbors=n_neighbors, metric="euclidean")
        model.fit(X_weighted)

        return model

    def query_weighted_knn(
        self, model: NearestNeighbors, feature_weights, query
    ):
        q_weighted = query * np.sqrt(feature_weights.values)

        distances, indices = model.kneighbors([q_weighted])

        return distances[0], indices[0]


# recommender = Recommender()

# results = evaluate(recommender)
# print(results)
