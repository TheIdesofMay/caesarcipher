import sys
import collections
import re
import ast

# Alphabet stored in a string instead of dictionary due to easier element referencing
alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]


# Print usage instructions and exit script
def printinstructions():

    print("\n--------------------------------------------------------\n"
          "Usage instructions: enter the following two parameters into the CLI: '--encrypt' or '--decrypt' followed by "
          "some positive integer as your rotation. You may also enter two additional parameters, '--file' and '[filename]' "
          "if you would like to encrypt/decrypt a text file."
          "\n--------------------------------------------------------\n")
    sys.exit()


# Retrieves manual message entry
def getmessage():
    message = input("Enter your message: \n\n").upper()
    return message


# Gets rotation, checks for correct data type (int), checks if int is +ve, prints instructions and exits if otherwise
def getrotationandcheck():

    rotation = sys.argv[2]

    # Error handling for correct data type
    try:
        int(rotation)
    except ValueError:
        print("ERROR! - your rotation value isn't an integer!\n")
        printinstructions()

    # Check for legal rotation (+ve int)
    if int(rotation) < 1:
        print("ERROR! - your rotation isn't positive!\n")
        printinstructions()

    return rotation

# Increases the index of each letter in message by rotation
def encryptmessage(alphabet, rotation, message):

    # Create temp list for new letter to be added
    output_list = []

    # Splits each character in message into list
    character_list = list(message)

    # Alphabetical characters have index added
    # Non-alphabetical characters added to list with no change
    for character in character_list:
        if character.isalpha():
            # Modulo operator used to loop around the 26 letters
            letter_index = (alphabet.index(character) + int(rotation)) % 26
            # Rotation added to index and then referenced to alphabet list
            output_list.append(alphabet[letter_index])
        else:
            output_list.append(character)

    # Joins list and prints it
    output_message = "".join(output_list)
    print("You encrypted message is: {}\n".format(output_message))


# Same function as encryptmessage() but with rotation subtracted from index
def decryptmessage(alphabet, rotation, message):

    output_list = []
    character_list = list(message)
    for character in character_list:
        if character.isalpha():
            letter_index = (alphabet.index(character) - int(rotation)) % 26
            output_list.append(alphabet[letter_index])
        else:
            output_list.append(character)

    output_message = "".join(output_list)
    print("You decrypted message is: {}\n".format(output_message))


# Determines all message statistics
def getmessagestats(message):

    print("\n--------------------------------------------------------\n"
          "Word Statistics:"
          "\n--------------------------------------------------------\n")

    # Lists for message processing
    word_lengths = []
    message_list = message.split()

    # Regex used to remove all non-alphabetical characters from message
    message_alpha_only = re.sub("[^A-Z]+", "", message)

    # Fills list with the length of each word in message (for min/max/avg)
    for word in message_list:
        word_lengths.append(len(word))

    # Utilises the 'most_common' method from collections for letter and word frequency
    most_common_letter = collections.Counter(message_alpha_only).most_common(1)

    # Calculations carried out in .format() to avoid unnecessary variable assignments
    print("There are {} total words in your message\n".format(len(message_list)))
    # By converting the data type to set, only unique elements are included
    print("There are {} unique words in your message\n".format(len(set(message_list))))
    print("The minimum word length is {}\n".format(min(word_lengths)))
    print("The maximum word length is {}\n".format(max(word_lengths)))
    print("The average word length is {}\n".format(sum(word_lengths)/len(word_lengths)))
    # most_common presents the value and frequency in tuple pairs, hence double indexing
    # to extract the first (value) and last (freq) elements of the tuple
    print("The most common letter is '{}' with {} appearances\n".format(most_common_letter[0][0], most_common_letter[0][1]))

# Opens and returns dictionary for automatic decryption
def processdictionary():

    # Open dictionary text fie and store add each word to to a list
    words_list = []
    dict = open("dictionary.txt", "r")
    for word in dict:
        words_list.append(word)
    # Strips the '\n' which is added to the end of each word
    stripped_words = [words.rstrip() for words in words_list]
    return stripped_words

# Processing file I/O
def processtextfile():

    # Temp list for reading file text to list
    message_list = []

    if sys.argv[3] != "--file":
        printinstructions()

    # Error handling if filename not found
    try:
        file_message = open(str(sys.argv[4]), "r")
    except FileNotFoundError:
        print("The file you specified could not be found! Please ensure it is entered correctly and placed in the same "
              "directory as the python script\n")
        sys.exit()

    # Opens file, reads to list, returns the joined message in uppercase
    file_message = open(str(sys.argv[4]), "r")
    for line in file_message:
        message_list.append(line)
    message = "".join(message_list).upper()

    return message

# *!* Part 3 and optional Part 4: this function will automatically decrypt the message by attempting
# each rotation from 1-26, comparing it against the dictionary and asking the user if the decryption is correct *!*

def autodecrypt(alphabet, message, dictionary):

    # variable definitions for later use
    character_list = list(message)
    accepted_answer = False
    output_list = []
    identical_words = 0
    n = 0
    rot_dict = {}

    # iteratively goes through rotations 1-26 and applies them to the message decryption
    for rot in range(1, 26):
        for character in character_list:
            # Largely re-used code from decryptmessage()
            if character.isalpha():
                letter_index = (alphabet.index(character) - rot)
                output_list.append(alphabet[letter_index])
            else:
                output_list.append(character)

        # values are joined to form a list of strings in the message
        word_list = "".join(output_list).split()

        # Tallies the total number of similarities between the message words and the dictionary
        for word in word_list:
            if word.lower() in dictionary:
                identical_words += 1

        # Create a dictionary data type where the key is the message with rotation applies and value is the
        # number of matches between the message and dictionary.txt
        rot_dict[str(word_list)] = identical_words

        # Resets the message and matching count to prevent each iteration appending to the previous list
        identical_words = 0
        output_list = []

        # Sorts the dictionary key in descending order so that the message with the most matches are
        # at the beginning of the list
    ranked_rotations = sorted(rot_dict.items(), key=lambda a: a[1], reverse=True)

    # While loop which will execute until the user accepts the message
    while accepted_answer != True:

        # Due to the dictionary ranking producing a str which follows the form of a list instead of an actual
        # list, the syntax is corrected using the literal evaluation tool in abs
        syntax_corrected_string = ast.literal_eval(ranked_rotations[n][0])

        # Presents the sentence and queries the user if it's correct
        answer = input("Is this decryption correct: {}?\nEnter 'yes'/'no':\n".format(" ".join(syntax_corrected_string)))

        # If rejected, the script will then present the next element in the dictionary (the next-highest matched rot)
        if answer == "yes":
            accepted_answer = True
        elif answer == "no":
            n += 1
        # Exits if user doesn't enter 'yes' or 'no'
        else:
            print("Please enter either 'yes' or 'no'\n")
            sys.exit()

        # Error handling if user says no 25 times (no more unique messages due to alphabet being exhausted)
        try:
            rotation_exhausted = ranked_rotations[n][0]
        except IndexError:
            print("There are no more rotations to try, sorry!\n")
            sys.exit()


# Control flow of program
print("\n")

# encryption_choice is always required hence it's not a function
encryption_choice = sys.argv[1]

# No arguments provided; illegal
if len(sys.argv) == 1:
    printinstructions()

# encryption with file provided
elif encryption_choice == "--encrypt" and len(sys.argv) == 5:
    message = processtextfile()
    rotation = getrotationandcheck()

    encryptmessage(alphabet, rotation, message)

# decryption with file provided
elif encryption_choice == "--decrypt" and len(sys.argv) == 5:
    message = processtextfile()
    rotation = getrotationandcheck()

    decryptmessage(alphabet, rotation, message)

# encryption with manual message entry
elif encryption_choice == "--encrypt" and len(sys.argv) == 3:
    message = getmessage()
    rotation = getrotationandcheck()

    encryptmessage(alphabet, rotation, message)

# decryption with manual message entry
elif encryption_choice == "--decrypt" and len(sys.argv) == 3:
    message = getmessage()
    rotation = getrotationandcheck()

    decryptmessage(alphabet, rotation, message)

# decryption with automatic rotation
elif encryption_choice == "--decrypt" and len(sys.argv) == 2:
    message = getmessage()
    dictionary = processdictionary()

    autodecrypt(alphabet, message, dictionary)

else:
    printinstructions()

# Message stats always provided for legal messages
getmessagestats(message)

sys.exit()