#!/usr/bin/env python3
"""
Flip a single bit in a file to demonstrate the avalanche effect in hash functions
"""
import sys

def flip_bit(input_file, output_file, byte_position, bit_position):
    """
    Flip a specific bit in a file
    
    Args:
        input_file: Input file path
        output_file: Output file path
        byte_position: Position of byte to modify (0-indexed)
        bit_position: Which bit to flip (0-7)
    """
    # Read the file
    with open(input_file, 'rb') as f:
        data = bytearray(f.read())
    
    if byte_position >= len(data):
        print(f"Error: File only has {len(data)} bytes, cannot modify byte {byte_position}")
        sys.exit(1)
    
    # Store original value
    original_byte = data[byte_position]
    original_char = chr(original_byte) if 32 <= original_byte < 127 else f"\\x{original_byte:02x}"
    
    # Flip the specified bit
    bit_mask = 1 << bit_position
    data[byte_position] ^= bit_mask
    
    # Store modified value
    modified_byte = data[byte_position]
    modified_char = chr(modified_byte) if 32 <= modified_byte < 127 else f"\\x{modified_byte:02x}"
    
    # Write modified data
    with open(output_file, 'wb') as f:
        f.write(data)
    
    print(f"Bit flip completed successfully!")
    print(f"  Input: {input_file}")
    print(f"  Output: {output_file}")
    print(f"  Byte position: {byte_position}")
    print(f"  Bit position: {bit_position}")
    print(f"  Original byte: 0x{original_byte:02x} (binary: {original_byte:08b}) = '{original_char}'")
    print(f"  Modified byte: 0x{modified_byte:02x} (binary: {modified_byte:08b}) = '{modified_char}'")
    print(f"  Changed bit {bit_position}: {(original_byte >> bit_position) & 1} → {(modified_byte >> bit_position) & 1}")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python flip_bit.py <input_file> <output_file> [byte_pos] [bit_pos]")
        print("\nExample:")
        print("  python flip_bit.py plaintext.txt modified.txt 50 3")
        print("  (Flips bit 3 of byte 50)")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    byte_pos = int(sys.argv[3]) if len(sys.argv) > 3 else 50
    bit_pos = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    
    flip_bit(input_file, output_file, byte_pos, bit_pos)
