import os
import regex as re
import numpy as np
import pandas as pd
import seaborn as sns
import unicodedata as uc
import matplotlib.pyplot as plt

# Oskar Šefců 
# Comments are in english, cause they are weird in czech. 
# Supporting library for auto encoding/decoding

# Global variables
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ_"

# Function for normalizing text into the alphabet only char set
def textNormalize(text: str):
    
    # Removing interpunction
    text = uc.normalize('NFD', text)
    
    # Standardizing to UpperCase and replacing spaces
    text = text.replace(" ","_").upper()
    
    # Removing any other characters
    mod = re.compile('[^_A-Z]')
    text = mod.sub("",text)
 
    return text

# Function for creating bigrams 
def createBigram(text: str):

    # Checks if only allowed chars are used in the text
    if not set(text).issubset(set(alphabet)):
        raise SyntaxError("ERROR: invalid char, use textNormalize")

    bigram = []
    n = len(text); i = 0     

    while i < n-1:
        bigram.append(str(text[i]+text[i+1]))
        i += 1
    
    return bigram

# Unigram creation
def createUnigram(text: str=None):
    if text is None:
        print("No text provided for unigram, using default text.")
        # Get the directory where the current script is located.
        current_dir = os.path.dirname(os.path.abspath(__file__))
    
        # Construct the full file path for a file in the same directory.
        file_path = os.path.join(current_dir, 'data', 'mladik_z_povolani.txt')
        with open(file_path, 'r', encoding='utf-8') as file:
            text = textNormalize(file.read())
    
    # Checks if only allowed chars are used in the text
    if not set(text).issubset(set(alphabet)):
        raise SyntaxError("ERROR: invalid char, use textNormalize")

    
    freq = {letter: 0 for letter in alphabet}
    for ch in text:
            freq[ch] += 1

    total = sum(freq.values())

    for letter in freq:
        freq[letter] /= total if total > 0 else 1
    
    return pd.Series(freq)

# Text encryption from plaintext and key
def textEncrypt(text: str, key: str):
    # Checks if only allowed chars are used in the text
    if not set(text).issubset(set(alphabet)) or not set(key).issubset(set(alphabet)):
        raise SyntaxError("ERROR: invalid char, use textNormalize")

    # Create mapping based on ecnryption
    mapping = {k: v for k, v in zip(alphabet, key)}

    # Iterate over text produce encryption using the key
    result = ''.join(mapping[char] if char in mapping else char for char in text)
    
    return result

# Text Decryption based on plaintext and provided key
def textDecrypt(text: str, key: str):
    # Checks if only allowed chars are used in the text
    if not set(text).issubset(set(alphabet)) or not set(key).issubset(set(alphabet)):
        raise SyntaxError("ERROR: invalid char, use textNormalize")
    
    # Create mapping based on decryption
    mapping = {k: v for k, v in zip(key, alphabet)}

    # Iterate over text produce decryption using the key
    result = ''.join(mapping[char] if char in mapping else char for char in text)
    
    return result

# Creating a bigram matrix, optional provide bigram, set relative/absolute matrix and add verbosity
def createBigramMatrix(bigram: list = None, v: int = 0):

    # If no bigram is provided, calculate from provided text
    if bigram is None:
        print("No bigram provided for matrix, using default text.")
        # Get the directory where the current script is located.
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the full file path for a file in the same directory.
        file_path = os.path.join(current_dir, 'data', 'mladik_z_povolani.txt')
        with open(file_path, 'r', encoding='utf-8') as file:
            bigram = createBigram(textNormalize(file.read()))

    # Creating an empty matrix
    matrix = pd.DataFrame(0, index=list(alphabet), columns=list(alphabet))

    # Calculating absolute bigram matrix
    for i, item in enumerate(bigram, start=0): 
        matrix.at[item[0],item[1]] += 1

        # Verbose proggres bar
        if v>0:
            percent = int((i / len(bigram)) * 100)
            last_percent = -1
            if percent > last_percent:
                print(f"\rProgress: {percent}% ({i}/{len(bigram)})", end='')
                last_percent = percent
    
    # Transform to relative matrix
    matrix = matrix/matrix.values.sum() 

    return matrix

# Calculate decryption plausability - provided decrypted text and reference matrix (how it should be in czech)
def decryptionPlausability(text: str, refMatrix, refUnigram, alpha:int= 0.5):
    # Check for valid dataframe matrix
    if not isinstance(refMatrix, pd.DataFrame):
        raise TypeError("refMatrix must be a pandas DataFrame")
    
    # Checks if only allowed chars are used in the text
    if not set(text).issubset(set(alphabet)):
        raise SyntaxError("ERROR: invalid char, use textNormalize")
    
    # Compute candidate bigram matrix from the text
    candidateBigram = createBigramMatrix(createBigram(text))
    bigram_distance = np.sqrt(0.5 * np.sum((np.sqrt(refMatrix.values) - np.sqrt(candidateBigram.values)) ** 2))

    # Compute candidate unigram frequencies from the text
    candidateUnigram = createUnigram(text)
    unigram_distance = np.sqrt(0.5 * np.sum((np.sqrt(refUnigram.values) - np.sqrt(candidateUnigram.values)) ** 2))

    return alpha * bigram_distance + (1 - alpha) * unigram_distance

# THE CODE BREEEKAAHHHH
def codeBreaker(text: str, refMatrix=None,refUnigram=None, iter: int=10000, startKey: str = None, v:int = 0):
    if refMatrix is None:
        print("Creating reference matrix as none was provided")
        refMatrix = createBigramMatrix()

    if refUnigram is None:
        print("Creating reference matrix as none was provided")
        refUnigram = createUnigram()

    if not set(text).issubset(set(alphabet)):
        raise SyntaxError("ERROR: invalid char, use textNormalize")

    # Creating a starting key
    if startKey is None:
        currentKey = ''.join(np.random.permutation(list(alphabet)))
    else:
        currentKey = startKey

    # Creating starting decryption and its plausiblity
    currentDecript = textDecrypt(text, currentKey)
    currentPlaus = decryptionPlausability(currentDecript, refMatrix, refUnigram)

    progress = []
    progressBest = []
    k = 0
    coolingRate = 0.999
    T = 1.0

    while k < iter:
        
        # Swap two randoms letters in the key
        candidateKey = list(currentKey)
        i, j = np.random.choice(len(candidateKey), 2, replace=False)
        candidateKey[i], candidateKey[j] = candidateKey[j], candidateKey[i]
        candidateKey = ''.join(candidateKey)

        # Calculate the new key plausability
        candidateDecript = textDecrypt(text, candidateKey)
        candidatePlaus = decryptionPlausability(candidateDecript, refMatrix, refUnigram)

        # Updating candidate list 
        if v>1:
            progress.append(candidatePlaus)

        delta = candidatePlaus - currentPlaus

        # Accept if improvement, or with a probability exp(-delta/T) otherwise.
        if delta < 0 or np.random.rand() < np.exp(-delta / T):
            currentKey = candidateKey
            currentPlaus = candidatePlaus

        # Update temperature.
        T *= coolingRate

        # Verbose logging
        if k % 500 == 0 and v>0:
            print(f"Iteration {k}: Best Plausability={currentPlaus:.4f}")

        # Updating current best
        if v>1:
            progressBest.append(currentPlaus)

        k += 1

    if v > 1:
        sns.set_theme(style="whitegrid")

        window_size = 50  
        rolling_all = np.convolve(progress, 
                                np.ones(window_size)/window_size, 
                                mode='valid')

        plt.figure(figsize=(12, 6))
        plt.plot(rolling_all, label='All Candidates (Rolling Avg)', color='blue', alpha=0.7)
        plt.plot(progressBest, label='Best Candidates', color='orange', alpha=0.9)
        plt.xlabel('Iteration')
        plt.ylabel('Plausibility Score')
        plt.title('Progress Summary from CodeBreaker')
        plt.legend()
        plt.tight_layout()
        plt.show()

    finalDecrypt = textDecrypt(text, currentKey)

    return finalDecrypt, currentKey, currentPlaus

# Create a key with the least plausibility
def keyMaker(text: str, refMatrix, iter: int=1000, v:int=0):
    
    if not set(text).issubset(set(alphabet)):
        raise SyntaxError("ERROR: invalid char, use textNormalize")

    if refMatrix is None:
        print("Creating reference matrix as none was provided")
        refMatrix = createBigramMatrix(v=True)


    currentKey = ''.join(np.random.permutation(list(alphabet)))
    
    # Creating starting decryption and its plausiblity
    currentDecript = textDecrypt(text, currentKey)
    currentPlaus = decryptionPlausability(currentDecript, refMatrix)

    k = 0
    while k < iter:
        # Swap two randoms letters in the key
        candidateKey = list(currentKey)
        i, j = np.random.choice(len(candidateKey), 2, replace=False)
        candidateKey[i], candidateKey[j] = candidateKey[j], candidateKey[i]
        candidateKey = ''.join(candidateKey)

        # Calculate the new key plausability
        candidatePlaus = decryptionPlausability(textEncrypt(text, candidateKey), refMatrix)

        q = candidatePlaus/currentPlaus

        # If improvement is reached
        if q > 1:
            
            # Switch for new candidate
            currentKey = candidateKey

            # Switch new best plausability
            currentPlaus = candidatePlaus

        if k % 500 == 0 and v==1:
            print(f"Iter {k}: plaus={currentPlaus:.4f}")

        k += 1
    
    return currentKey

# Matcher if you know the expected output
def matchPercent(input: str, compare:str):

    # Use the length of the longer string for normalization
    total = max(len(input), len(compare))

    # Count exact matches only (swapped letters count as a difference)
    match_count = sum(1 for i in range(min(len(input), len(compare))) if input[i] == compare[i])
    
    # Characters in the longer string without a corresponding position count as mismatches.
    return (match_count / total) * 100
    