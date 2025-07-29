#!/usr/bin/env python3
import sys
import re
import random
import string

def generate_random_characters(pattern):
    def replace_brackets(match):
        content = match.group(1)
        result = []
        
        # Process each character in the pattern individually
        for char in content:
            if char == 'x':
                # Generate random digit
                result.append(str(random.randint(0, 9)))
            elif char == 'a':
                # Generate random lowercase letter
                result.append(random.choice(string.ascii_lowercase))
            elif char == 'A':
                # Generate random uppercase letter
                result.append(random.choice(string.ascii_uppercase))
            else:
                # Keep any other character as is
                result.append(char)
        
        return ''.join(result)
    
    result = re.sub(r'\[([xaA]+)\]', replace_brackets, pattern)
    return result

def main():
    if len(sys.argv) < 2:
        print("Usage: rando [FORMAT]")
        print("Example: rando [xx]-[xxx]-andalso[x]")
        print("Where:")
        print("  [x] gets replaced with random digits")
        print("  [a] gets replaced with random lowercase letters")
        print("  [A] gets replaced with random uppercase letters")
        print("  [aA] creates alternating lowercase and uppercase letters")
        sys.exit(1)
        
    pattern = sys.argv[1]
    result = generate_random_characters(pattern)
    print(result)

if __name__ == "__main__":
    main()