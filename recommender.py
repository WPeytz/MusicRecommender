from evaluation import evaluate
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

    trend_follower_columns = ["loudness", "valence", "tempo"]

    custom_columns = ["popularity"]

    def __init__(self) -> None:
        self.df = pd.read_csv("dataset.csv")
        self.df["artists"] = self.df["artists"].str.split(";")
        self.df = self.df.dropna(subset=["artists", "track_name"])
        self.df = self.df.drop_duplicates(subset=["track_id"], keep="first")
        self.df = self.df.reset_index(drop=True)

        self.df["popularity"] = self.df["popularity"] / 100.0

        for column in self.clustering_columns + self.trend_follower_columns:
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

        playlist_clustering_df = pd.DataFrame(columns=["value", "weight"])
        track_df = self.df[self.df["track_id"].isin(input_track_ids)]

        for col in self.clustering_columns:
            mean, weight = self.cluster_weight(track_df[col])
            playlist_clustering_df.loc[col] = {"value": mean, "weight": weight}

        for col in self.trend_follower_columns:
            value = self.rolling_next_value(track_df[col].values)
            playlist_clustering_df.loc[col] = {"value": value, "weight": 0.3}

        for col in self.custom_columns:
            playlist_clustering_df.loc[col] = {"value": 1, "weight": 0.4}

        mask = self.df["artists"].apply(
            lambda artists: bool(set(artists) & target_artist)
        )
        possibility_df = self.df[mask]

        mask = possibility_df["track_id"].apply(
            lambda track_id: bool(track_id not in input_track_ids)
        )
        possibility_df = possibility_df[mask]

        model = self.weighted_knn_fit(
            possibility_df[
                self.clustering_columns
                + self.trend_follower_columns
                + self.custom_columns
            ],
            playlist_clustering_df["weight"],
            n_recommendations,
        )

        distances, indices = self.query_weighted_knn(
            model,
            playlist_clustering_df["weight"],
            playlist_clustering_df["value"],
        )

        return possibility_df.iloc[indices]["track_id"].to_list()

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

    def query_weighted_knn(self, model: NearestNeighbors, feature_weights, query):
        q_weighted = query * np.sqrt(feature_weights.values)

        distances, indices = model.kneighbors([q_weighted])

        return distances[0], indices[0]

    def rolling_next_value(self, series):
        window = min(len(series), 3)

        next_value = pd.Series(series).rolling(window).mean().iloc[-1]

        return next_value


recommender = Recommender()

results = evaluate(recommender)
print(results)
