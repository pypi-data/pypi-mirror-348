import itertools, string, time

def run(givenPassword=None):
    # Define all characters to use in the password
    chars = string.printable

    # Define the password to search for cracked
    if givenPassword is None:
        password = input("Input your own password:")
        if password == "":
            print("Password can't be empty. Quitting process...")
            return 0.0
    else:
        password = givenPassword

    # Define max_length, min_value length and passwordfound
    max_length = 2
    min_value = 1
    passwordfound = False

    # Track the start time of the password cracking process
    start_time = time.perf_counter()

    # Try all possible combinations of characters up to max_length

    while not passwordfound:
        for length in range(min_value, max_length + 1):
            for combination in itertools.product(chars, repeat=length):
                # Join the characters in the combination to form a password candidate
                candidate = "".join(combination)

                #print("Trying password:", candidate) increase speed by disabling this

                # Check if the candidate matches the password
                if candidate == password:
                    # Track the end time of the password cracking process
                    end_time = time.perf_counter()
                    print("Password found:", candidate)
                    # Calculate the time taken to crack the password
                    time_taken = end_time - start_time
                    print("Time taken:", time_taken, "seconds")
                    # Terminate the password cracking process
                    return (time_taken)#even better as it will stop and allow normal running after subroutine runs

        #increase min and max password lengths to lengths that haven't been iterated thru. Done when for loop stops, because password was not found
        min_value = max_length + 1
        max_length += 5  #make bigger so it checks more in a go before jumping to the next length (^num,^effic)
