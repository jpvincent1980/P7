import csv
import time


def timer(function):
    def decoratedfunction(*args, **kwargs):
        start = time.time()
        result = function(*args, **kwargs)
        end = time.time()
        print("*" * 50)
        print("Temps d'exécution -> " + str(round(end-start, 2)) + "s")
        return result
    return decoratedfunction


@timer
def optimized(file, maximum):
    # Keeps track of the original maximum value
    original_maximum = maximum
    # Converts Euros to Cents to get only integers as they will be used as
    # indices in the upcoming array
    maximum = maximum * 100
    # Converts external data into a list of dictionaries
    with open(file, newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        shares_list = []
        for row in reader:
            # To consider only positive prices
            if float(row["price"]) >= 0:
                shares_dict = {"share_name": row["name"],
                               "share_price": int(float(row["price"]) * 100),
                               "share_profit": int(float(row["profit"]) * 100),
                               "share_gain": int(float(row["price"]) * 100) *
                                             int(float(row["profit"]) * 100) / 1000000}
                shares_list.append(shares_dict)
    total_nb_shares = len(shares_list)
    # Initialise une matrice avec le nombre d'éléments en ligne et la valeur maximale en colonne
    # Chaque cellule de la matrice est un dictionnaire composé de la valeur maximale et d'un booléen qui vérifie si la valeur maximale est bien générée par l'élément de cette ligne
    matrix = [[{"max_value":0,"optimal":False} for _ in range(maximum + 1)] for _ in range(total_nb_shares + 1)]
    for i in range(1, total_nb_shares + 1):
        for j in range(maximum + 1):
            if shares_list[i-1]["share_price"] > j:
                matrix[i][j]["max_value"] = matrix[i-1][j]["max_value"]
            else:
                if shares_list[i-1]["share_gain"] + matrix[i-1][j - shares_list[i-1]["share_price"]]["max_value"] > matrix[i-1][j]["max_value"]:
                    matrix[i][j]["max_value"] = shares_list[i-1]["share_gain"] + matrix[i-1][j-shares_list[i-1]["share_price"]]["max_value"]
                    matrix[i][j]["optimal"] = True
                else:
                    matrix[i][j]["max_value"] = matrix[i-1][j]["max_value"]
    selected_shares = []
    max_value = 0
    sum_price = 0
    for ligne in range(total_nb_shares, 0, -1):
        if matrix[ligne][maximum]["optimal"]:
            selected_shares.append(shares_list[ligne-1]["share_name"] +
                                   " -> " +
                                   str(shares_list[ligne-1]["share_price"] / 100) +
                                   "€")
            max_value = max(max_value, matrix[ligne][maximum]["max_value"])
            sum_price += shares_list[ligne - 1]["share_price"]
            maximum -= shares_list[ligne-1]["share_price"]
    print(f"To maximize your {original_maximum}€, you should buy:\n")
    for share in selected_shares:
        print(share)
    print()
    print(f"Total cost = {round(sum_price / 100, 2)}€")
    print(f"Total return = {round(max_value, 2)}€")
    return

if __name__ == "__main__":
    optimized("dataset2_Python+P7.csv", 500)


