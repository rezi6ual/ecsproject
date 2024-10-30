import pandas as pd

# Load the character-to-binary mapping from the Excel file
xl = pd.read_excel("P2M012_G4.xlsx", dtype=str)


def encode(fn, output_filename="BinOutput.txt"):
    """
    Reads a text file, converts the characters to their binary equivalents,
    and writes the encoded binary string to an output file.
    
    :param fn: The text file to be encoded.
    :param output_filename: The name of the output binary file.
    """
    # Creating lists for characters and their corresponding binary representations
    chars = list(xl['Char'])
    bins = list(xl['Bin'])
    encode_map = dict(zip(chars, bins))
    
    # Handle space and newline characters
    if "<space>" in chars:
        encode_map[" "] = encode_map.pop("<space>")
    if "\\n" in chars:
        encode_map["\n"] = encode_map.pop("\\n")

    try:
        with open(fn, 'r') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"Error: The file '{fn}' was not found.")
        return

    total_bits = 0
    binary_string = ""
    content_length = len(content)

    # Step through the content
    i = 0
    while i < content_length:
        found = False
        for length in range(3, 0, -1):  # Check for substrings of length 3, 2, 1
            substring = content[i:i + length]
            if substring in encode_map:
                binary_code = encode_map[substring]
                binary_string += binary_code
                total_bits += len(binary_code)
                i += length  # Move the index forward
                found = True
                break

        if not found:
            print(f"Warning: Character '{content[i]}' not found in the mapping.")
            i += 1

    with open(output_filename, 'w') as outfile:
        outfile.write(f"{total_bits}.{binary_string}")

def decode(fn, output_filename="TextOutput.txt"):
    """
    Reads a binary encoded file, decodes it back to text using the character mapping,
    and writes the output to a text file.
    
    :param fn: The binary encoded file to be decoded.
    :param output_filename: The name of the output text file.
    """
    chars = list(xl['Char'])
    bins = list(xl['Bin'])
    decode_map = dict(zip(bins, chars))

    # Handle space and newline characters
    if "<space>" in chars:
        decode_map["00000"] = " "
    if "\\n" in chars:
        decode_map["1110101"] = "\n"

    try:
        with open(fn, 'r') as f:
            contents = f.read()
    except FileNotFoundError:
        print(f"Error: The file '{fn}' was not found.")
        return

    index = contents.find(".")
    if index == -1:
        print("Error: Invalid encoded file format.")
        return

    contents = contents[index + 1:]

    output = ""

    while contents:
        # Attempt to decode using 5 bits for space or 7 bits otherwise
        if contents.startswith('00000'):
            output += decode_map['00000']
            contents = contents[5:]  # Remove the used code
        elif contents.startswith('1110101'):
            output += decode_map['1110101']
            contents = contents[7:]  # Remove the used code
        else:
            try:
                code_length = 7 if contents[0] == '1' else 5
                binary_code = contents[:code_length]
                output += decode_map[binary_code]
                contents = contents[code_length:]  # Remove the decoded binary
            except KeyError:
                print(f"Warning: Binary code '{contents[:code_length]}' not found.")
                break

    with open(output_filename, 'w') as file:
        file.write(output)


encode()
decode()

def same(fn1, fn2="TextOutput.txt"):
    """
    Compares two text files line by line and character by character.
    If the files are identical, it prints "Identical Files".
    Otherwise, it prints "Different Files" and creates an 'Errors.txt' file
    that details the differences.

    :param fn1: The first text file to be compared.
    :param fn2: The second text file to be compared, defaults to "TextOutput.txt".
    """
    try:
        with open(fn1, 'r') as file1, open(fn2, 'r') as file2:
            content1 = file1.read()
            content2 = file2.read()
            
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return

    # Check if files are identical
    if content1 == content2:
        print("Identical Files")
        return
    else:
        print("Different Files")
        
        # Create an Errors.txt file with detailed differences
        with open("Errors.txt", 'w') as error_file:
            # Write file lengths
            len1, len2 = len(content1), len(content2)
            error_file.write(f"file 1: {len1} and file 2: {len2}\n")
            
            # Compare files character by character
            for i, (c1, c2) in enumerate(zip(content1, content2)):
                if c1 != c2:
                    error_file.write(f"{i}: {c1}: {c2}\n")

            # Handle case where one file is longer than the other
            longer_content = content1 if len1 > len2 else content2
            longer_file = "file 1" if len1 > len2 else "file 2"
            if len1 != len2:
                for i in range(min(len1, len2), max(len1, len2)):
                    extra_char = longer_content[i]
                    error_file.write(f"{i}: {extra_char} ({longer_file} extra)\n")
same()