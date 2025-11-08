import pandas
from recommender import Recommender

def main():
    print("Hello from musicrecommender!")

    r = Recommender()

    df = r.get_recommendations(['5SuOikwiRyPMVoIQDJUgSV','4nmjL1mUKOAfAbo9QG9tSE','12qmPGMrOCogibc7qyxT9s','3dPpQeLTWjCjEbSevDMQfW','2pcuXnZhTirLXsfXGVFTv2','4qPNDBW1i3p13qLCt0Ki3A','1pG5nd6gmfbMwUfT5shDQe','7bhHLZxkRekrNPPkEdDTbn','14BMBNRzv24eG6OKoIgPfP','0Pi3Ua6fJV1Yx5MGXhfybT'], 5, set(['Jason Mraz']))

    print(df)



if __name__ == "__main__":
    main()
