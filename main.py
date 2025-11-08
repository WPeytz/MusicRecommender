import pandas
from recommender import Recommender

def main():
    print("Hello from musicrecommender!")

    r = Recommender()

    df = r.get_recommendations([], 5, set(['ZAYN', 'Sam Smith']))

    print(df)



if __name__ == "__main__":
    main()
