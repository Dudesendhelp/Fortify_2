from pathlib import Path
import pickle
import math


def score(password):
    base_dir = Path(__file__).parent.parent.parent
    pickle_path = base_dir / "Password_checker" / "common_passwords" / "password_hash_table.pkl"

    with open(pickle_path, "rb") as f:
        common_passwords = pickle.load(f)

    score = 1
    common=False
    if password in common_passwords:
        score = 0
        common=True
    length=False
    if len(password) > 10:
        length=True
        score += 1

    has_upper = False
    has_lower = False
    has_digit = False
    has_special = False
    if(len(password)==0):
        return [0,common,length,has_upper,has_lower,has_digit,has_special,0]
    for ch in password:
        if ch.isupper():
            has_upper = True
        elif ch.islower():
            has_lower = True
        elif ch.isdigit():
            has_digit = True
        else:
            has_special = True

    score += has_upper + has_lower + has_digit + has_special
    combination=0
    if has_digit:
      combination+=10
    if has_lower:
      combination+=26
    if has_upper:
      combination+=26
    if has_special:
      combination+=32
    entropy=len(password)*math.log(combination,2)

    return [score,common,length,has_upper,has_lower,has_digit,has_special,entropy]



if __name__ == "__main__":
    pwd = input("Enter password: ")
    print("Score:", score(pwd)[-1])