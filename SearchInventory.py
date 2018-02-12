import re
import DatabaseQueries

def searchItem(itemNameInput):
    df_inventory = DatabaseQueries.getInventory()
    df_inventory.index = df_inventory.index + 1

    words = itemNameInput.split()

    wordsClean = ""
    for word in words:
        for i, letter in enumerate(word):
             if i == 0:
                 wordsClean += letter.upper()
             else:
                 wordsClean += letter
        wordsClean += wordsClean.join(" ")


    df_result = df_inventory[df_inventory.itemName.str.contains(wordsClean) == True]

    return df_result


if __name__ == "__main__":

    df_result = searchItem("star")
    print(len(df_result))


