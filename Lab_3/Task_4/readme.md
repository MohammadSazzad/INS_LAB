# Task 4: Padding Analysis Report

## ✅ Task Completed Successfully!

---

## Objective
Study padding schemes by conducting experiments with different AES encryption modes (ECB, CBC, CFB, OFB) to determine which modes require padding and which do not.

---

## Experimental Setup

### Test File
- **Filename:** `plaintext.txt`
- **Size:** 194 bytes
- **Block size:** 16 bytes (AES)
- **Blocks:** 12 full blocks + 2 bytes remainder
- **Remainder:** 194 mod 16 = 2 bytes (NOT a multiple of 16)

### Encryption Parameters
- **Algorithm:** AES-128
- **Key:** `00112233445566778889aabbccddeeff` (128-bit)
- **IV (for CBC/CFB/OFB):** `0102030405060708`

---

## Commands Used

### 1. ECB Mode Encryption
```bash
openssl enc -aes-128-ecb -e -in plaintext.txt -out cipher_ecb.bin \
  -K 00112233445566778889aabbccddeeff
```

### 2. CBC Mode Encryption
```bash
openssl enc -aes-128-cbc -e -in plaintext.txt -out cipher_cbc.bin \
  -K 00112233445566778889aabbccddeeff -iv 0102030405060708
```

### 3. CFB Mode Encryption
```bash
openssl enc -aes-128-cfb -e -in plaintext.txt -out cipher_cfb.bin \
  -K 00112233445566778889aabbccddeeff -iv 0102030405060708
```

### 4. OFB Mode Encryption
```bash
openssl enc -aes-128-ofb -e -in plaintext.txt -out cipher_ofb.bin \
  -K 00112233445566778889aabbccddeeff -iv 0102030405060708
```

### 5. Examine Padding (with -nopad flag)
```bash
# ECB
openssl enc -aes-128-ecb -d -nopad -in cipher_ecb.bin \
  -out ecb_decrypted_nopad.bin -K 00112233445566778889aabbccddeeff

# CBC
openssl enc -aes-128-cbc -d -nopad -in cipher_cbc.bin \
  -out cbc_decrypted_nopad.bin -K 00112233445566778889aabbccddeeff \
  -iv 0102030405060708
```

---

## Results Summary

### File Size Comparison

| Mode | Plaintext Size | Ciphertext Size | Padding Added | Requires Padding? |
|------|----------------|-----------------|---------------|-------------------|
| **ECB** | 194 bytes | 208 bytes | +14 bytes | **YES ✓** |
| **CBC** | 194 bytes | 208 bytes | +14 bytes | **YES ✓** |
| **CFB** | 194 bytes | 194 bytes | 0 bytes | **NO ✗** |
| **OFB** | 194 bytes | 194 bytes | 0 bytes | **NO ✗** |

### Padding Analysis

**ECB and CBC Modes:**
- Padding bytes: `0e 0e 0e 0e 0e 0e 0e 0e 0e 0e 0e 0e 0e 0e` (14 bytes)
- Padding scheme: **PKCS#7**
- All padding bytes have value `0x0e` (14 in decimal)
- Original: 194 bytes → Padded: 208 bytes (13 complete blocks)

**CFB and OFB Modes:**
- No padding bytes added
- Ciphertext size matches plaintext size exactly (194 bytes)
- Stream cipher modes - no block completion required

---

## Detailed Analysis

### 🔴 ECB Mode - **REQUIRES PADDING ✓**

**Why:**
- ECB (Electronic Code Book) is a **block cipher mode**
- Operates on fixed-size blocks (16 bytes for AES-128)
- Each block encrypted independently: `Ci = E(K, Pi)`
- Incomplete last block must be padded to 16 bytes

**Padding Mechanism:**
- Used: PKCS#7 padding
- Needed: 2 bytes in last block, need 14 more bytes
- Added: 14 bytes, each with value `0x0e` (14)
- Result: 194 → 208 bytes (12 blocks + 2 bytes → 13 complete blocks)

**Hexdump of padding:**
```
Original last block:  ... 67 2e [END - needs 14 more bytes]
After padding:        ... 67 2e 0e 0e 0e 0e 0e 0e 0e 0e 0e 0e 0e 0e 0e 0e
```

---

### 🟡 CBC Mode - **REQUIRES PADDING ✓**

**Why:**
- CBC (Cipher Block Chaining) is a **block cipher mode**
- Each block XORed with previous ciphertext: `Ci = E(K, Pi ⊕ Ci-1)`
- Requires complete 16-byte blocks for XOR operation
- Encryption function E(K, ·) requires full blocks

**Padding Mechanism:**
- Same as ECB: PKCS#7 padding
- Same padding: 14 bytes of `0x0e`
- Result: 194 → 208 bytes

**Hexdump of padding:**
```
Original last block:  ... 67 2e [END - needs 14 more bytes]
After padding:        ... 67 2e 0e 0e 0e 0e 0e 0e 0e 0e 0e 0e 0e 0e 0e 0e
```

**Note:** Even if plaintext were exactly 192 bytes (12 blocks), CBC would add a full 16-byte padding block to avoid ambiguity!

---

### 🟢 CFB Mode - **NO PADDING REQUIRED ✗**

**Why:**
- CFB (Cipher Feedback) is a **stream cipher mode**
- Generates keystream by encrypting previous ciphertext
- XORs keystream with plaintext: `Ci = Pi ⊕ E(K, Ci-1)`
- Can process any number of bytes - no block completion needed

**How it works:**
1. Encrypt previous ciphertext block (or IV for first block)
2. XOR result with plaintext byte(s)
3. Output ciphertext has same length as input plaintext
4. No padding needed - can stop at any byte

**Result:**
- Input: 194 bytes → Output: 194 bytes
- Exact 1:1 size mapping
- Self-synchronizing after one block (useful for error recovery)

---

### 🔵 OFB Mode - **NO PADDING REQUIRED ✗**

**Why:**
- OFB (Output Feedback) is a **stream cipher mode**
- Generates keystream independently of plaintext/ciphertext
- XORs keystream with plaintext: `Ci = Pi ⊕ Si` where `Si = E(K, Si-1)`
- Keystream can be pre-computed - any length plaintext accepted

**How it works:**
1. Generate keystream by repeatedly encrypting previous output
2. Start with IV: `S0 = IV, S1 = E(K, S0), S2 = E(K, S1), ...`
3. XOR keystream with plaintext byte-by-byte
4. Can stop at any point - no block requirement

**Result:**
- Input: 194 bytes → Output: 194 bytes
- Exact 1:1 size mapping
- No error propagation (each bit independent)

---

## Explanation: Why This Difference?

### Block Cipher Modes vs Stream Cipher Modes

#### 🔲 Block Cipher Modes (ECB, CBC)

**Characteristics:**
- Process data in fixed-size blocks
- Encryption function: `E: {0,1}^block_size → {0,1}^block_size`
- **Must have complete blocks** - padding required

**Why padding needed:**
1. AES encryption function requires exactly 128 bits (16 bytes)
2. Cannot encrypt partial blocks (e.g., 2 bytes)
3. Must pad to next block boundary
4. Decryption removes padding to recover original size

**Padding scheme (PKCS#7):**
- If need N bytes of padding, add N bytes each with value N
- Example: Need 14 bytes → add `0e 0e 0e 0e 0e 0e 0e 0e 0e 0e 0e 0e 0e 0e`
- Always unambiguous (can determine padding length from last byte)
- If already multiple of block size, add full block (16 bytes of `0x10`)

---

#### 📡 Stream Cipher Modes (CFB, OFB)

**Characteristics:**
- Convert block cipher into stream cipher
- Generate continuous keystream
- XOR keystream with plaintext bit-by-bit
- **No block completion requirement**

**Why no padding:**
1. Keystream can be any length
2. XOR operation works on individual bits/bytes
3. Can stop encryption at any point
4. Output size = Input size (always)

**Advantages:**
- No padding overhead
- No padding oracle attacks possible
- Exact size preservation
- Simpler to use (no padding management)

**Disadvantages:**
- Must maintain synchronization (lost byte = corrupted stream)
- No built-in error detection
- CFB: Some error propagation (1-2 blocks)
- OFB: No error propagation (good and bad!)

---

## Padding Schemes Explained

### PKCS#7 Padding (used by OpenSSL)

**Rule:** If need N bytes of padding, add N bytes each with value N

**Examples:**
```
Need 1 byte:   ... 01
Need 2 bytes:  ... 02 02
Need 3 bytes:  ... 03 03 03
...
Need 14 bytes: ... 0e 0e 0e 0e 0e 0e 0e 0e 0e 0e 0e 0e 0e 0e
Need 16 bytes: ... 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10
```

**Special case:** If plaintext is already multiple of block size, add full block!
- 192 bytes → add 16 bytes of `0x10` → 208 bytes
- Avoids ambiguity (can always determine if padding present)

**Removal:**
1. Read last byte value (N)
2. Verify last N bytes all equal N
3. Remove last N bytes
4. If invalid → padding error

---

### Other Padding Schemes

**PKCS#5:**
- Same as PKCS#7 but only for 8-byte blocks
- Not used with AES (16-byte blocks)

**Zero Padding:**
- Pad with zeros: `... 00 00 00`
- **Problem:** Ambiguous if plaintext ends with zeros!
- Not recommended

**ANSI X.923:**
- Zeros with last byte = length: `... 00 00 00 00 0e`
- Less common than PKCS#7

**ISO 10126:**
- Random bytes with last byte = length: `... a3 5f 2c 91 0e`
- More secure but less common

---

## Security Implications

### 1. Padding Oracle Attacks

**Vulnerability:**
- If server reveals padding validation errors
- Attacker can decrypt ciphertext byte-by-byte
- Affects block modes with padding (ECB, CBC)

**Example:**
- Send modified ciphertext
- Server says "Invalid padding" → information leak!
- Attacker uses this to decode message

**Mitigation:**
- Use authenticated encryption (GCM, CCM)
- Never reveal padding errors specifically
- Same error message for all decryption failures

---

### 2. Mode Selection

**For Block Modes (ECB, CBC):**
- ✓ Padding required but manageable
- ✓ Good error detection (garbled output)
- ✗ Padding oracle vulnerability
- ✗ Size overhead (up to 1 block)

**For Stream Modes (CFB, OFB):**
- ✓ No padding needed
- ✓ No padding oracle attacks
- ✓ Exact size preservation
- ✗ Need separate authentication
- ✗ Synchronization critical

---

### 3. Modern Recommendations

**Best Practice: Use Authenticated Encryption**

**AES-GCM (Galois/Counter Mode):**
- Stream mode (no padding needed)
- Built-in authentication (GMAC)
- Detects tampering automatically
- Industry standard
- **Recommended for new applications**

**AES-CCM (Counter with CBC-MAC):**
- Alternative to GCM
- Used in IoT, TLS
- Also provides authentication

**ChaCha20-Poly1305:**
- Modern stream cipher
- Very fast on mobile devices
- Growing adoption

---

## Practical Implications

### When Padding Matters:

1. **Storage Systems:**
   - Block modes common for disk encryption
   - Padding increases file size slightly
   - Must store exact original size separately

2. **Network Protocols:**
   - Stream modes preferred (no size overhead)
   - CFB/OFB or modern GCM mode
   - Padding can reveal message lengths

3. **Database Encryption:**
   - Column size fixed → padding fits naturally
   - Or use stream modes for variable length

4. **Embedded Systems:**
   - Limited memory → stream modes advantageous
   - No padding buffer needed

---

## Conclusion

### Summary of Findings:

| Aspect | ECB | CBC | CFB | OFB |
|--------|-----|-----|-----|-----|
| **Padding Required** | ✓ Yes | ✓ Yes | ✗ No | ✗ No |
| **Type** | Block | Block | Stream | Stream |
| **Size Overhead** | Up to 16B | Up to 16B | None | None |
| **Padding Scheme** | PKCS#7 | PKCS#7 | N/A | N/A |
| **Security** | Poor | Moderate | Good | Good |
| **Recommendation** | Never use | Use with auth | OK | OK |

### Key Takeaways:

1. **Block cipher modes (ECB, CBC) REQUIRE padding**
   - Need complete blocks for encryption
   - PKCS#7 is standard padding scheme
   - Adds 1-16 bytes depending on input size

2. **Stream cipher modes (CFB, OFB) DON'T need padding**
   - Generate continuous keystream
   - XOR byte-by-byte
   - Output size = Input size (exact)

3. **Security considerations:**
   - Padding can introduce vulnerabilities (padding oracle)
   - Stream modes avoid this but need authentication
   - **Always use authenticated encryption in production**

4. **Modern best practice:**
   - Use **AES-GCM** (no padding + authentication)
   - Avoid ECB completely
   - CBC only with proper authentication (HMAC)
   - Stream modes good for size-sensitive applications

---

## Files Attached for Submission

1. **plaintext.txt** - Original file (194 bytes)
2. **cipher_ecb.bin** - ECB encrypted (208 bytes) - has padding
3. **cipher_cbc.bin** - CBC encrypted (208 bytes) - has padding
4. **cipher_cfb.bin** - CFB encrypted (194 bytes) - no padding
5. **cipher_ofb.bin** - OFB encrypted (194 bytes) - no padding
6. **ecb_decrypted_nopad.bin** - Decrypted with padding visible
7. **cbc_decrypted_nopad.bin** - Decrypted with padding visible
8. **analyze_padding.py** - Analysis script
9. **examine_padding.py** - Hexdump examination script

**Task 4 completed successfully! ✓**
