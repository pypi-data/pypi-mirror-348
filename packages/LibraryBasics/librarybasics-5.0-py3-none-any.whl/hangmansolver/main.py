import string, time

def run(givenString=None):
    # Define all characters to use in the password
    chars = string.ascii_lowercase
    print(chars)

    # Define the password to be cracked
    if givenString is None:
        word = input("Input partial solution:")
        if word == "":
            print("You have not provided a word. Next time, provide a word. Quitting process...")
            return 0.0
    else:
        word = givenString

    # Define max_length, min_length length and passwordfound
    max_length = len(word)
    min_length = len(word)
    passwordfound = False

    # Track the start time of the password cracking process
    start_time = time.perf_counter()

    loops = 0

    for char in word:
        if char == "_":
            loops += 1

    tempLOW = []
    ListOfWords = []

    for char in chars:
        tempword = word.replace("_", char, 1)
        tempLOW.append(tempword)

    for c in range(loops-1):
        ListOfWords = tempLOW
        tempLOW = []

        for word in ListOfWords:
            for char in chars:
                tempword = word.replace("_", char, 1)
                tempLOW.append(tempword)

    print(tempLOW)
    return(tempLOW)