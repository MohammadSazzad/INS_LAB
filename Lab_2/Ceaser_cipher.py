def decrypt_caesar(cipher, shift):
    """Decrypt Caesar cipher with given shift"""
    result = ""
    for char in cipher:
        if char.isalpha():
            # Determine if uppercase or lowercase
            base = ord('A') if char.isupper() else ord('a')
            # Shift the character
            shifted = (ord(char) - base - shift) % 26
            result += chr(base + shifted)
        else:
            result += char
    return result

def break_caesar(cipher):
    """Try all possible shifts and display results"""
    print("Caesar Cipher Breaker")
    print("=" * 60)
    print(f"\nOriginal cipher: {cipher}\n")
    print("Trying all possible shifts:")
    print("-" * 60)
    
    for shift in range(26):
        decrypted = decrypt_caesar(cipher, shift)
        print(f"Shift {shift:2d}: {decrypted}")
    
    return None

# Given cipher
cipher = "odroboewscdrolocdcwkbdmyxdbkmdzvkdpybwyeddrobo"

# Break the cipher
break_caesar(cipher)

print("\n" + "=" * 60)
print("ANALYSIS:")
print("Looking for readable English text...")
print("=" * 60)

# The most readable decryption
correct_shift = 10
plaintext = decrypt_caesar(cipher, correct_shift)
print(f"\nThe correct shift is: {correct_shift}")
print(f"Plaintext: {plaintext}")