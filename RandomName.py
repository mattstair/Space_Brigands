import random

first_parts = ["B", "Bh", "Bl", "Br", "C", "Ch", "Chr", "Cl", "Cr", "D", "Dr", "F", "Fl", "Fr", "G",
               "Gh", "Gl", "Gn", "Gr", "H", "J", "K", "Kl", "Kn", "Kr", "L", "M", "Mb", "N", "P",
               "Ph", "Phr", "Pl", "Pr", "Qu", "R", "S", "Sc", "Sch", "Scr", "Sh", "Shr", "Shl", "Sk",
               "Sl", "Sm", "Sn", "Sp", "Spl", "Spr", "Squ", "St", "Str", "Sw", "T", "Th", "Thr", "Tr",
               "Ts", "Tw", "V", "W", "Wh", "Wr", "X", "Y", "Z"]
vowels = ["a", "e", "i", "o", "u"]
last_parts = ["b", "bb", "ch", "ck", "ct", "d", "dd", "f", "ff", "ft", "g", "gg", "gh", "ld", "lf",
              "lk", "ll", "lm", "lp", "lt", "m", "mb", "mm", "mp", "mph", "n", "nch", "nd", "ng",
              "nk", "nn", "nt", "nth", "p", "ph", "pp", "r", "rb", "rch", "rd", "rf", "rg", "rk",
              "rl", "rm", "rn", "rp", "rst", "rt", "rth", "sh", "sk", "sm", "sp", "ss", "st", "t",
              "tch", "th", "tt", "w", "wn", "x", "zz"]
suffixes = ["", "berry", "dale", "ford", "ington", "kin", "ly", "man", "sky", "smith", "son",
            "stein", "ston", "sworth", "word", "ham", "wold", "lord", "berg", "storm", "strom"]


def get_random_name():

    done = False
    while not done:
        first_part = random.choice(first_parts)
        last_part = random.choice(last_parts)

        # check if last letter of first part is same as first of last part. hard to pronounce, not natural
        # same letter is OK if first is uppercase
        if first_part[-1] != last_part[0]:
            done = True

    first_name = first_part + random.choice(vowels) + last_part

    done = False
    while not done:
        first_part = random.choice(first_parts)
        last_part = random.choice(last_parts)

        # check if last letter of first part is same as first of last part. hard to pronounce, not natural
        # same letter is OK if first is uppercase
        if first_part[-1] != last_part[0]:
            done = True

    last_name = first_part + random.choice(vowels) + last_part + random.choice(suffixes)

    full_name = (first_name + " " + last_name)

    return full_name
