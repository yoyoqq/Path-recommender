from first_and_second_task import *

"""
Go to the main function to run the code (line 62)
"""

graph = Graph()

# function to get the most common substring
def most_similar_word(text1, text2):
    """
    Levenshtain Distance algorithm
    """
    n, m = len(text1), len(text2)
    # Create 2D grid
    dp = [[0]*(m+1) for _ in range(n+1)]

    for r in range(1, n + 1):
        for c in range(1, m + 1):
            # If the values are equal, total + 1
            if text1[r-1] == text2[c-1]:
                dp[r][c] = 1 + dp[r-1][c-1]
            # if not, take the value of the top or left
            else:
                dp[r][c] = max(dp[r-1][c], dp[r][c-1])
    # return the last value of the dp
    return dp[-1][-1]


def process(cin):  
    if len(cin) == 0:
        return print(cin)
    # Optimization, check if the names exists in the nodes.
    cin = cin.capitalize().strip()
    words = tuple(i for i in graph.nodes)
    if cin in words:
        return print(cin)
    
    # Look for the mosts similar words using the Levenshtein distance
    correct_word = []
    for i in words:
        new_word = most_similar_word(cin, i)
        correct_word.append([i, new_word])
    correct_word.sort(key= lambda x:x[1])

    # Process from raw input to the most common words. 
    final_words = []
    level = correct_word[-1][1]
    for i in range(len(correct_word)-2, -1, -1):
        if correct_word[i][1] >= level - 1:
            final_words.append(correct_word[i])
    
    # Process data for the output.
    str_other = ""
    for i in final_words:
        str_other = str_other +", "+ i[0]
    str_other = str_other.replace(",", "", 1)
    # print("Did you mean {} or{}.".format(correct_word[-1][0], str_other))
    print("Did you mean {}?".format(correct_word[-1][0]))


if __name__ == "__main__":
    """
    User input
    """
    # cin = "bankk"   # user inpout
    cin = "Bankk"

    """
    System 
    """
    a = process(cin)
