#from evaluation import evaluate
import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np


class Recommender:

    def __init__(self) -> None:
        self.df = pd.read_csv("dataset.csv")
        self.df['artists']=self.df['artists'].str.split(';')
        self.df = self.df.dropna(subset=['artists', 'track_name'])
        self.df = self.df.drop_duplicates(subset=['track_id'], keep='first')
        self.df = self.df.reset_index(drop=True)


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

        mask = self.df['artists'].apply(lambda artists: bool(set(artists) & target_artist))
        df = self.df[mask]



        return df

        #return recommended_track_ids


#recommender = Recommender()

#results = evaluate(recommender)
#print(results)
