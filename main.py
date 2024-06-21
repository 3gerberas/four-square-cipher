import sys
import subprocess
from termcolor import colored
from art import logo
import random
import time


# Define the alphabet
alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
            'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
# Colors for the logo
colors = ['red', 'green', 'blue', 'yellow', 'cyan', 'magenta', 'white']


def clear_screen():
    # Clear the unwanted part
    operating_system = sys.platform
    if operating_system == 'win32' or operating_system == 'cygwin' or operating_system == 'msys':
        subprocess.run("cls")
    if operating_system == 'linux' or operating_system == 'linux2' or operating_system == 'darwin':
        subprocess.run("clear")


def print_logo():
    # Display the logo for the program
    clear_screen()
    print(colored(logo, random.choice(colors), attrs=['bold']))


def get_data(prompt, allow_spaces=False):
    # Prompt for user input
    while True:
        # Convert user input to uppercase
        data_input = input(prompt).upper()

        # Check if input contains spaces
        if allow_spaces:
            # Include spaces in filtered data if allowed
            filtered_data = ''.join([char for char in data_input if char in alphabet or char == ' '])
        else:
            filtered_data = ''.join([char for char in data_input if char in alphabet])

        # Validate input based on whether spaces are allowed or not
        if not allow_spaces and len(filtered_data) != len(data_input):
            # Make sure that the input contains only alphabetic characters
            print("Invalid input. Please use only alphabetic characters from A-Z (no spaces).")
        elif allow_spaces and not all(char in alphabet or char == ' ' for char in data_input):
            # Make sure that the input doesn't contain any invalid characters like (#, @, etc.)
            print("Invalid input. Please use only alphabetic characters from A-Z and spaces.")
        else:
            return filtered_data


def make_key_matrix(key):
    # Create a 5x5 matrix from the given key
    # Remove duplicates and fill it with the remaining letters
    seen = set()
    matrix = [char for char in key if char in alphabet and not (char in seen or seen.add(char))]
    matrix += [char for char in alphabet if char not in seen]
    return ''.join(matrix)


def make_reference_matrix():
    # Create a 5x5 matrix from the alphabet
    return ''.join(alphabet)


def initiate_matrices(key1, key2):
    # Create matrices based on keys and reference matrix
    matrix1 = make_key_matrix(remove_duplicates(key1))
    matrix2 = make_key_matrix(remove_duplicates(key2))
    ref_matrix = make_reference_matrix()

    return matrix1, matrix2, ref_matrix


def print_matrices(key1, key2):
    # Display the matrices
    matrix1, matrix2, ref_matrix = initiate_matrices(key1, key2)
    print("\nMatrices:\n")
    for i in range(0, len(matrix1), 5):
        print(f"{' '.join(ref_matrix[i:i + 5].lower()):<15}{' '.join(matrix1[i:i + 5]):<20}")

    print("\n")

    for i in range(0, len(matrix1), 5):
        print(f"{' '.join(matrix2[i:i + 5]):<15}{' '.join(ref_matrix[i:i + 5].lower()):<20}")


def remove_duplicates(key):
    # Remove duplicate characters from a string
    seen = set()
    return ''.join([char for char in key if not (char in seen or seen.add(char))])


def determine(ref1, ref2):
    # Evaluate the new position of the characters in the matrix 
    # base on the transformation of the rows and columns

    return (ref1 // 5) * 5 + ref2 % 5


def search(matrix, letter):
    # Return the index of the letter in the matrix
    return matrix.index(letter) if letter in matrix else -1


def four_square(word, key1, key2, direction):
    # Encrypt or decrypt the word using the two matrix keys
    matrix1, matrix2, ref_matrix = initiate_matrices(key1, key2)
    result = []
    # Iterate through the word through character pairs 
    for i in range(0, len(word), 2):
        if i + 1 < len(word):
            # Find the positions of the characters in the reference matrix
            if direction == 'encrypt' or direction == 'e':
                a, b = search(ref_matrix, word[i]), search(ref_matrix, word[i + 1])
                # Encrypt characters using key matrices
                result.append(matrix1[determine(a, b)])
                result.append(matrix2[determine(b, a)])
            elif direction == 'decrypt' or direction == 'd':
                a, b = search(matrix1, word[i]), search(matrix2, word[i + 1])
                # Decrypt characters using key matrices
                result.append(ref_matrix[determine(a, b)])
                result.append(ref_matrix[determine(b, a)])
        else:
            # Management of the case when we have an odd number of characters
            if direction == 'encrypt' or direction == 'e':
                a = search(ref_matrix, word[i])
                result.append(matrix1[a])
            elif direction == 'decrypt' or direction == 'd':
                a = search(matrix1, word[i])
                result.append(ref_matrix[a])
    return ''.join(result)


def cipher(message, key1, key2, direction, allow_spaces=True):
    # Apply the Four-Square cipher to multiple words
    print_matrices(key1, key2)
    if allow_spaces:
        result = []
        list_word = message.split()
        for word in list_word:
            filter_word = ''.join([char for char in word if char in alphabet])
            cipher_word = four_square(filter_word, key1, key2, direction)
            result.append(cipher_word)
        return ' '.join(result)
    else:
        result = four_square(message, key1, key2, direction)
        return result


def main():
    keyword_list = ["Pizza", "Monarchy", "Zebras", "Cocoon", "Cryptology",
                    "Computer", "Science", "Programming", "Apple",
                    "Kiwi", "Cyberpunk", "Monochrome", "Capricorn",
                    "Python", "GitHub", "Copilot", "Artificial", "Intelligence",
                    "Machine", "Learning", "Data", "Analysis", "Algorithm",
                    "Database", "Web", "Development", "Mobile", "App",
                    "Network", "Security", "Cloud", "Computing", "Internet",
                    "Blockchain", "Virtual", "Reality", "Automation", "Robotics",
                    "Big", "Data", "Internet", "Offline", "Things",
                    "Software", "Engineering", "User", "Interface", "Testing"]
    # Make Color
    global alphabet
    print_logo()
    again = 'yes'
    while again in ['yes', 'y']:
        # Get the keys and message from the user
        direction = input("Type 'encrypt' ('e') or 'decrypt' ('d') for cipher direction: ").lower()
        count = 0
        while direction not in ['encrypt', 'e', 'decrypt', 'd']:
            if count == 3:
                print("Too many invalid choices. Exiting the program.")
                exit()
            direction = input("Invalid input. Please type 'encrypt' ('e') or 'decrypt' ('d'): ")
            count += 1
        omit = input("Enter the letter you want to omit (one letter from A to Z): ").upper()
        while omit not in alphabet and len(omit) != 1:
            omit = input("Invalid input. Please enter the letter you want to omit (one letter from A to Z): ").upper()
        alphabet.remove(omit)
        # Remove keys that contain the omit letter
        keyword_list = [keyword for keyword in keyword_list if omit.upper() not in keyword]
        keyword_list = [keyword for keyword in keyword_list if omit.lower() not in keyword]
        choice = input("Enter '1' to choose the keywords from a default list or '2' to enter two keywords manually: ")
        if choice == '1':
            print("Available keywords:")
            for i, keyword in enumerate(keyword_list):
                print(f"{i+1}. {keyword}")
            while True:
                try:
                    key1_index = int(input("Enter the index of Key 1: ")) - 1
                    key2_index = int(input("Enter the index of Key 2: ")) - 1
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid index.")
            key1 = keyword_list[key1_index].upper()
            key2 = keyword_list[key2_index].upper()
        elif choice == '2':
            key1 = get_data(f"Enter Key 1 (only A-Z, excluding {omit}): ", allow_spaces=False)
            key2 = get_data(f"Enter Key 2 (only A-Z, excluding {omit}): ", allow_spaces=False)
        else:
            print("Invalid choice. Exiting the program.")
            exit()
        temp = 0
        while True:
            choice = input("Enter '1' to use a file as input or '2' to manually enter the message: ").lower()
            if choice == '1':
                file_path = input("Enter the file path: ")
                try:
                    with open(file_path, 'r') as file:
                        message = file.read().upper()
                        break
                except FileNotFoundError:
                    print("File not found. Please enter a valid file path.")
            elif choice == '2':
                message = input(f"Enter the message (only A-Z, excluding Q): ").upper()
                break
            else:
                temp += 1
                if temp >= 3:
                    print("Invalid choice. Exiting the program.")
                    exit()
            print("Invalid choice. Please enter '1' or '2'.")
        # Encrypt or decrypt the message and display the result
        print_logo()
        start_time = time.time()
        result = cipher(message, key1, key2, direction, allow_spaces=True)
        end_time = time.time()

        execution_time = end_time - start_time
        with open("result.txt", "w") as file:
            file.write(result)
        # Display the result in a decorated table
        print(f"\nResult: {format(result)}")
        print(f"\nExecution time: {execution_time} seconds")
        print("\nThe result has been saved to 'result.txt'.")
        # Ask the user if they want to encrypt another message
        again = input("\nWould you like to encrypt another message? (yes/no): ").lower()
        # Make color
        print_logo()
        alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                    'U', 'V', 'W', 'X', 'Y', 'Z']
        if again not in ['yes', 'y']:
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
