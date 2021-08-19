import itertools
import csv


def bruteforce(file, max_cost=500):
    # We import external data and convert them into a list of dictionaries
    with open(file, newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        shares_list = []
        for row in reader:
            shares_dict = {"share_name": row["name"],
                           "share_price": float(row["price"]),
                           "share_profit": float(row["profit"]),
                           "share_gain": float(row["price"]) * float(
                               row["profit"]) / 100}
            shares_list.append(shares_dict)
    selected_list = []
    # We generate all possible combinations
    for i in range(len(shares_list) +1):
        for element in itertools.combinations(shares_list, i):
            sum_cost = 0
            sum_gain = 0
            for sub_element in element:
                sum_cost += sub_element["share_price"]
                sum_gain += sub_element["share_gain"]
            # We only keep the combinations with a total cost lower or equal to
            # the maximum investment cost
            if sum_cost <= max_cost:
                selected_list.append((round(sum_gain, 2), element))
    # We rank the list by total profit in descending order
    selected_list = sorted(selected_list, key=lambda x: -x[0])
    # We return the first element of the list which is the best combination
    return selected_list[0]


if __name__ == "__main__":
    best_combination = bruteforce("share_list.csv")
    print(f"Le meilleur bénéfice est de {best_combination[0]}€ avec la "
          f"combinaison d'actions suivante:")
    for share in best_combination[1]:
        print(f"{share['share_name']} -> gain = "
              f"{round(share['share_gain'], 2)}")
