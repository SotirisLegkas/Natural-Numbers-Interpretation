'''
# Ask user for an input phone number (string)
# User gives number in sequences seperated with a space character
# Each sequence 1-3 digits
# Return the phone number without spaces (string)
# Phone numbers strictly 10 or 14 digits
# If 10 digits: must start with 2 or 69
# If 14 digits: must start with 00302 or 003069
# Ambiguities in GREEK
# Ambiguity 1: 20 5 -> 205 or 25
# Ambiguity 2: 75 -> 75 or 705
# Ambiguity 3: 725 -> 725 or 700 20 5 or 700 25 or 720 5
# Ambiguity 4: 720 -> 720 or 700 20 or 72 (if next number is 1-9) or 700 2 (if next number is 1-9)
# Ambiguity 5: 702 -> 702 or 700 2
# Ambiguity 6: 700 -> 700 or 70 (if next number is 1-9) or 7 (if next number is 10-99)
# handle 3 digits that start with 0 (probably not such case as the voice recognition will handle zero as a single digit each time)

# 2 10 6 9 30 6 6 4 in GREEK should have 10 6 -> 16 or 106
'''


from dataclasses import dataclass
from itertools import product
import pandas as pd

@dataclass
class Ambiguity:            # For debugging purposes
    kind: str               # "Ambiguity 1-6" or "None"
    index: int              # The index of the digit group
    potential_num: list     # A list with all the potential combination of digits for a group of numbers

def check_number_sequences(numbers: str):
    seqs = numbers.split()
    if not seqs:
        raise ValueError("Please provide a phone number.")
    else:
        for seq in seqs:
            if len(seq)>3 or not (seq.isdigit()):
                raise ValueError(f"Problem with sequence '{seq}'.\nEach sequence should have up to 3 digits and all of them should be numbers.")
    return seqs      # Always return a list


def check_ambiguities(sequences: list[str]):
    ambiguity_list=[]

    def add_ambiguity(kind, i, nums):
        ambiguity_list.append(
            Ambiguity(kind=kind, index=i, potential_num=nums)
        )

    def has_next_single_digit_nonzero(i):     # There is a next single nonzero digit
        return (
            i + 1 < len(sequences)
            and len(sequences[i + 1]) == 1
            and sequences[i + 1] != "0"
        )
    
    def has_next_double_digits_nonzero(i):    # There are next two nonzero digits
        return (
            i + 1 < len(sequences)
            and len(sequences[i + 1]) == 2
            and sequences[i + 1][0]!= "0"
        )

    for i, seq in enumerate(sequences):
        n= len(seq)                                                  # Number of digits
        kind = "None"
        nums = [seq]                                                 # Default sequence

        if n==2 and seq[0]!="0":                                     # Cases for groups with two digits
            if seq[1]=="0" and has_next_single_digit_nonzero(i):     # Ambiguity 1: 20 5 -> 205 or 25
                if not (seq == "10" and sequences[i + 1] in "12"):   # 11 and 12 cannot be split in Greek language
                    kind = "Ambiguity 1"
                    nums = [seq,                                     # 20
                            seq[0]]                                  # 2
            elif seq[1] != "0" and seq not in ["11", "12"]:          # Ambiguity 2: 75 -> 75 or 705
                kind = "Ambiguity 2"
                nums = [seq,                                         # 75
                        seq[0] + "0" + seq[1]]                       # 705

        elif n==3:                                                  # Cases for groups with three digits
            if "0" not in seq:                                      # Ambiguity 3: 725 -> 725 or 700 20 5 or 700 25 or 720 5
                kind = "Ambiguity 3"                            
                if seq[1:] in ["11","12"]:                          # 11 and 12 cannot be split in Greek language
                    nums = [seq,                                    # 711
                            seq[0]+"00"+seq[1:]]                    # 70011
                else:
                    nums = [seq,                                    # 725
                            seq[0]+"00"+seq[1]+"0"+seq[2],          # 700205
                            seq[0]+"00"+seq[1:],                    # 70025
                            seq[:2]+"0"+seq[2]]                     # 7205
            
            elif "0" not in seq[:2] and seq[2]=="0":                # Ambiguity 4: 720 -> 720 or 700 20 or 72 (if next number is 1-9) or 700 2 (if next number is 1-9)
                kind = "Ambiguity 4"
                nums = [seq,                                        # 720
                        seq[0]+"00"+seq[1]+"0"]                     # 70020
                if has_next_single_digit_nonzero(i) and not (seq[1] == "1" and sequences[i + 1] in "12"):   # Except the cases that combines into 11 or 12
                    nums.extend([seq[:2],                           # 72
                                 seq[0]+"00"+seq[1]])               # 7002
            
            elif seq[0]!="0" and seq[1]=="0" and seq[2]!="0":       # Ambiguity 5: 702 -> 702 or 700 2
                kind = "Ambiguity 5"
                nums = [seq,                                        # 702
                        seq[:2]+"0"+seq[2]]                         # 7002
            
            elif seq[0]!="0" and seq[1:]=="00":                    # Ambiguity 6: 700 -> 700 or 70 (if next number is 1-9) or 7 (if next number is 10-99)
                if has_next_single_digit_nonzero(i):
                    kind="Ambiguity 6"
                    nums = [seq,                                  # 700
                            seq[:2]]                              # 70
                elif has_next_double_digits_nonzero(i):
                    kind="Ambiguity 6"
                    nums = [seq,                                  # 700
                            seq[0]]                               # 7

        add_ambiguity(kind=kind, i=i, nums=nums)

    return ambiguity_list


def potential_numbers(numbers: str):
    sequences = check_number_sequences(numbers=numbers)
    ambiguities = check_ambiguities(sequences=sequences)
    combinations = ["".join(phone_number) for phone_number in list(product(*[ambiguity.potential_num for ambiguity in ambiguities]))]
    unique_combinations = list(set(combinations))
    return unique_combinations

def check_validation(phone_number: str):
    if (len(phone_number)==10 and phone_number.startswith(("2","69"))) or (len(phone_number)==14 and phone_number.startswith(("00302","003069"))):
        return True
    return False

def main():
    print("Phone Numbers Interpretation\n")
    print("Enter number groups separated by spaces (each group: 1-3 digits).")
    print("Type 'q' or press Ctrl+C to quit.\n")

    while True:
        try:
            input_number = input("Type your phone number: ").strip()
            print()
        except (KeyboardInterrupt, EOFError):
            print("\n\nExit application!")
            break
        if input_number.strip().lower() == "q":
            print("\n\nExit application!")
            break

        try:
            numbers = potential_numbers(numbers=input_number)
        except ValueError as error:
            print("Error: ",error)
            print()
            continue

        df = pd.DataFrame({
            "Interpretation": range(1, len(numbers) + 1),
            "Output": numbers,
            "Phone number": [ "VALID" if check_validation(number) else "INVALID" for number in numbers]
            })

        print("\nIdentified numbers:\n")
        print(df.to_string(index=False))
        print()

if __name__ == "__main__":
    main()
