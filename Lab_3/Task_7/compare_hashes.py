#!/usr/bin/env python3
"""
Compare two hash values and count bit differences
Demonstrates the avalanche effect in cryptographic hash functions
"""
import sys

def hex_to_binary(hex_string):
    """Convert hex string to binary string"""
    # Remove any spaces or special characters
    hex_string = hex_string.replace(" ", "").replace(":", "")
    # Convert to binary
    binary = bin(int(hex_string, 16))[2:]  # [2:] removes '0b' prefix
    # Pad to correct length (4 bits per hex digit)
    binary = binary.zfill(len(hex_string) * 4)
    return binary

def count_bit_differences(hash1, hash2):
    """
    Count the number of different bits between two hash values
    
    Args:
        hash1: First hash value (hex string)
        hash2: Second hash value (hex string)
    
    Returns:
        dict with statistics
    """
    # Clean inputs
    hash1 = hash1.strip().lower().replace(" ", "")
    hash2 = hash2.strip().lower().replace(" ", "")
    
    # Check lengths match
    if len(hash1) != len(hash2):
        raise ValueError(f"Hash lengths don't match: {len(hash1)} vs {len(hash2)}")
    
    # Convert to binary
    bin1 = hex_to_binary(hash1)
    bin2 = hex_to_binary(hash2)
    
    # Count different bits
    different_bits = sum(b1 != b2 for b1, b2 in zip(bin1, bin2))
    total_bits = len(bin1)
    same_bits = total_bits - different_bits
    
    return {
        'hash1': hash1,
        'hash2': hash2,
        'total_bits': total_bits,
        'different_bits': different_bits,
        'same_bits': same_bits,
        'difference_percentage': (different_bits / total_bits) * 100,
        'binary1': bin1,
        'binary2': bin2
    }

def display_comparison(stats, show_binary=False):
    """Display hash comparison statistics"""
    print(f"\n{'='*70}")
    print(f"  HASH COMPARISON ANALYSIS")
    print(f"{'='*70}")
    
    print(f"\nHash 1: {stats['hash1']}")
    print(f"Hash 2: {stats['hash2']}")
    
    if show_binary:
        print(f"\nBinary 1: {stats['binary1'][:64]}...")
        print(f"Binary 2: {stats['binary2'][:64]}...")
    
    print(f"\n{'='*70}")
    print(f"  BIT DIFFERENCE STATISTICS")
    print(f"{'='*70}")
    
    print(f"\nTotal bits:       {stats['total_bits']}")
    print(f"Different bits:   {stats['different_bits']}")
    print(f"Same bits:        {stats['same_bits']}")
    print(f"Difference:       {stats['difference_percentage']:.2f}%")
    print(f"Similarity:       {100 - stats['difference_percentage']:.2f}%")
    
    # Avalanche effect analysis
    print(f"\n{'='*70}")
    print(f"  AVALANCHE EFFECT ANALYSIS")
    print(f"{'='*70}")
    
    if stats['difference_percentage'] > 45:
        print(f"\n✓ EXCELLENT avalanche effect!")
        print(f"  {stats['difference_percentage']:.2f}% of bits changed")
        print(f"  Ideal hash function changes ~50% of bits for 1-bit input change")
    elif stats['difference_percentage'] > 30:
        print(f"\n✓ GOOD avalanche effect")
        print(f"  {stats['difference_percentage']:.2f}% of bits changed")
    else:
        print(f"\n⚠ WEAK avalanche effect")
        print(f"  Only {stats['difference_percentage']:.2f}% of bits changed")
        print(f"  Good hash functions should change ~50% of bits")

def main():
    print("="*70)
    print("  CRYPTOGRAPHIC HASH COMPARISON TOOL")
    print("="*70)
    
    if len(sys.argv) >= 3:
        # Command line arguments provided
        hash1 = sys.argv[1]
        hash2 = sys.argv[2]
    else:
        # Interactive mode
        print("\nEnter two hash values to compare (in hexadecimal)")
        hash1 = input("Hash 1: ").strip()
        hash2 = input("Hash 2: ").strip()
    
    try:
        stats = count_bit_differences(hash1, hash2)
        display_comparison(stats, show_binary=False)
        
        print(f"\n{'='*70}")
        print("Analysis complete! ✓")
        print("="*70 + "\n")
        
    except ValueError as e:
        print(f"\nError: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
