import csv


def optimized(file, maximum):
    # Keeps track of the original maximum value to print it at the end
    original_maximum = maximum
    # Converts Euros to Cents to get only integers as they will be used as
    # indexes in the upcoming matrix
    maximum = maximum * 100
    # Imports external data and converts them into a list of dictionaries
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
    # Initialize a matrix where each line represents a share and each column
    # represents an investment cost. Each cell consists of a dictionary made of
    # the maximum profit possible and a boolean that double checks if the
    # maximum profit possible comes from that cell or the one above.
    matrix = [[{"max_value":0,"optimal":False} for _ in range(maximum + 1)] for _ in range(total_nb_shares + 1)]
    # The first line of the matrix does not represent any share. The share
    # on line i of the matrix will represent the share at index i-1 from
    # the shares list. The loop will then start at line 1 which will represent
    # the share at index 0 of the shares list.
    for i in range(1, total_nb_shares + 1):
        for j in range(maximum + 1):
            # if the share's cost is greater than the investment amount of the
            # given column, cell gets the "max_value" of the cell above and
            # stays at "optimal" = False
            if shares_list[i-1]["share_price"] > j:
                matrix[i][j]["max_value"] = matrix[i-1][j]["max_value"]
            else:
                # if the sum of the line's share profit and the ones from the
                # previous shares is greater than the maximum value from the
                # previous line for the same investment amount
                # (i.e. same column), the max_value gets that sum as its value
                # and the "optimal" key is set to True.
                if shares_list[i-1]["share_gain"] + matrix[i-1][j - shares_list[i-1]["share_price"]]["max_value"] > matrix[i-1][j]["max_value"]:
                    matrix[i][j]["max_value"] = shares_list[i-1]["share_gain"] + matrix[i-1][j-shares_list[i-1]["share_price"]]["max_value"]
                    matrix[i][j]["optimal"] = True
                else:
                    # otherwise cell gets the "max_value" of the cell above and
                    # stays at "optimal" = False.
                    matrix[i][j]["max_value"] = matrix[i-1][j]["max_value"]
    selected_shares = []
    max_value = 0
    sum_price = 0
    # We finally inspect the matrix starting by the last cell at
    # the bottom right.
    for ligne in range(total_nb_shares, 0, -1):
        # If that cell is optimal, we add its share's profit to the selected
        # shares list and subtract its share's cost from the total investment
        # amount
        if matrix[ligne][maximum]["optimal"]:
            selected_shares.append(shares_list[ligne-1]["share_name"] +
                                   " -> " +
                                   str("{:.2f}".format(shares_list[ligne-1]["share_price"] / 100)) +
                                   "€")
            max_value = max(max_value, matrix[ligne][maximum]["max_value"])
            sum_price += shares_list[ligne - 1]["share_price"]
            maximum -= shares_list[ligne-1]["share_price"]
    print(f"To maximize your {original_maximum}€, you should buy:\n")
    for share in selected_shares:
        print(share)
    print()
    print(f"Total cost = {round(sum_price / 100, 2):.2f}€")
    print(f"Total return = {round(max_value, 2):.2f}€")
    return


if __name__ == "__main__":
    optimized("share_list.csv", 500)


