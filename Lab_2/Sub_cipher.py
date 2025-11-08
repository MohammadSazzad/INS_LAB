from collections import Counter
import re

# English letter frequencies (from the lab manual)
ENGLISH_FREQ = {
    'e': 12.22, 't': 9.67, 'a': 8.05, 'o': 7.63, 'i': 6.28, 
    'n': 6.95, 's': 6.02, 'h': 6.62, 'r': 5.29, 'd': 5.10,
    'l': 4.08, 'u': 2.92, 'c': 2.23, 'm': 2.33, 'w': 2.60,
    'f': 2.14, 'g': 2.30, 'y': 2.04, 'p': 1.66, 'b': 1.67,
    'v': 0.82, 'k': 0.95, 'j': 0.19, 'x': 0.11, 'q': 0.06, 'z': 0.06
}

def analyze_frequency(cipher):
    """Analyze letter frequency in cipher text"""
    # Extract only letters
    letters = re.findall(r'[a-z]', cipher.lower())
    total = len(letters)
    
    # Count frequencies
    freq_count = Counter(letters)
    
    # Calculate percentages
    freq_percent = {letter: (count/total)*100 for letter, count in freq_count.items()}
    
    # Sort by frequency
    sorted_freq = sorted(freq_percent.items(), key=lambda x: x[1], reverse=True)
    
    return sorted_freq, freq_count

def display_frequency_analysis(cipher, cipher_name):
    """Display frequency analysis for a cipher"""
    print(f"\n{'='*70}")
    print(f"FREQUENCY ANALYSIS: {cipher_name}")
    print(f"{'='*70}")
    
    sorted_freq, freq_count = analyze_frequency(cipher)
    
    print(f"\nTotal letters: {sum(freq_count.values())}")
    print(f"\nLetter frequencies (sorted by frequency):")
    print("-" * 70)
    
    # Get sorted English frequencies for comparison
    english_sorted = sorted(ENGLISH_FREQ.items(), key=lambda x: x[1], reverse=True)
    
    print(f"{'Cipher':<10} {'Freq':<8} {'%':<8} {'Likely':<10} {'English %'}")
    print("-" * 70)
    
    for i, (letter, percent) in enumerate(sorted_freq):
        if i < len(english_sorted):
            likely_letter = english_sorted[i][0]
            english_pct = english_sorted[i][1]
            print(f"{letter:<10} {freq_count[letter]:<8} {percent:<8.2f} "
                  f"{likely_letter:<10} {english_pct:.2f}")
        else:
            print(f"{letter:<10} {freq_count[letter]:<8} {percent:<8.2f}")
    
    return sorted_freq

def create_substitution_map(cipher_freq, common_words=None):
    """Create initial substitution map based on frequency"""
    # Sort English letters by frequency
    english_sorted = sorted(ENGLISH_FREQ.keys(), 
                           key=lambda x: ENGLISH_FREQ[x], 
                           reverse=True)
    
    # Create initial mapping
    sub_map = {}
    for i, (cipher_letter, _) in enumerate(cipher_freq):
        if i < len(english_sorted):
            sub_map[cipher_letter] = english_sorted[i]
    
    return sub_map

def apply_substitution(cipher, sub_map):
    """Apply substitution mapping to cipher"""
    result = ""
    for char in cipher:
        if char.lower() in sub_map:
            decrypted = sub_map[char.lower()]
            result += decrypted.upper() if char.isupper() else decrypted
        else:
            result += char
    return result

def break_substitution(cipher, cipher_name, manual_map=None):
    """Break substitution cipher using frequency analysis"""
    print(f"\n\n{'#'*70}")
    print(f"BREAKING {cipher_name}")
    print(f"{'#'*70}")
    
    # Analyze frequency
    cipher_freq = display_frequency_analysis(cipher, cipher_name)
    
    # Create initial substitution map
    sub_map = create_substitution_map(cipher_freq)
    
    print(f"\n\nINITIAL SUBSTITUTION MAP:")
    print("-" * 70)
    print("Cipher -> Plaintext")
    for cipher_letter, plain_letter in sorted(sub_map.items()):
        print(f"  {cipher_letter} -> {plain_letter}")
    
    # Apply substitution
    initial_decrypt = apply_substitution(cipher, sub_map)
    
    print(f"\n\nINITIAL DECRYPTION ATTEMPT:")
    print("-" * 70)
    print(initial_decrypt[:500] + "..." if len(initial_decrypt) > 500 else initial_decrypt)
    
    # If manual mapping provided, use it for better results
    if manual_map:
        print(f"\n\n{'*'*70}")
        print(f"REFINED SUBSTITUTION MAP (Manual Analysis):")
        print("*" * 70)
        print("Cipher -> Plaintext")
        for cipher_letter, plain_letter in sorted(manual_map.items()):
            print(f"  {cipher_letter} -> {plain_letter}")
        
        refined_decrypt = apply_substitution(cipher, manual_map)
        
        print(f"\n\nREFINED DECRYPTION:")
        print("*" * 70)
        print(refined_decrypt)
        
        return manual_map, refined_decrypt
    
    return sub_map, initial_decrypt

# Cipher texts
cipher1 = """af p xpkcaqvnpk pfg, af ipqe qpri, gauuikifc tpw, ceiri udvk tiki afgarxifrphni cd eao--wvmd popkwn, hiqpvri du ear jvaql vfgikrcpfgafm du cei xkafqaxnir du xrwqedearcdkw pfg du ear aopmafpcasi xkdhafmr afcd fit pkipr. ac tpr qdoudkcafm cd lfdt cepc au pfwceafm epxxifig cd ringdf eaorinu hiudki cei opceiopcaqr du cei uaing qdvng hi qdoxnicinw tdklig dvc--pfg edt rndtnw ac xkdqiigig, pfg edt odvfcpafdvr cei dhrcpqnir--ceiki tdvng pc niprc kiopaf dfi mddg oafg cepc tdvng qdfcafvi cei kiripkqe"""

cipher2 = """aceah toz puvg vcdl omj puvg yudqecov, omj loj auum klu thmjuv hs klu zlcvu shv zcbkg guovz, upuv zcmdu lcz vuwovroaeu jczoyyuovomdu omj qmubyudkuj vukqvm. klu vcdluz lu loj avhqnlk aodr svhw lcz kvopuez loj mht audhwu o ehdoe eunumj, omj ck toz yhyqeoveg auecupuj, tlokupuv klu hej sher wcnlk zog, klok klu lcee ok aon umj toz sqee hs kqmmuez zkqssuj tckl kvuozqvu. omj cs klok toz mhk umhqnl shv sowu, kluvu toz oezh lcz yvhehmnuj pcnhqv kh wovpue ok. kcwu thvu hm, aqk ck zuuwuj kh lopu eckkeu ussudk hm wv. aonncmz. ok mcmukg lu toz wqdl klu zowu oz ok scskg. ok mcmukg-mcmu klug aunom kh doee lcw tuee-yvuzuvpuj; aqk qmdlomnuj thqej lopu auum muovuv klu wovr. kluvu tuvu zhwu klok zlhhr klucv luojz omj klhqnlk klcz toz khh wqdl hs o nhhj klcmn; ck zuuwuj qmsocv klok omghmu zlhqej yhzzuzz (oyyovumkeg) yuvyukqoe ghqkl oz tuee oz (vuyqkujeg) cmubloqzkcaeu tuoekl. ck tcee lopu kh au yocj shv, klug zocj. ck czm'k mokqvoe, omj kvhqaeu tcee dhwu hs ck! aqk zh sov kvhqaeu loj mhk dhwu; omj oz wv. aonncmz toz numuvhqz tckl lcz whmug, whzk yuhyeu tuvu tceecmn kh shvncpu lcw lcz hjjckcuz omj lcz nhhj shvkqmu. lu vuwocmuj hm pczckcmn kuvwz tckl lcz vueokcpuz (ubduyk, hs dhqvzu, klu zodrpceeu-aonncmzuz), omj lu loj womg juphkuj ojwcvuvz owhmn klu lhaackz hs yhhv omj qmcwyhvkomk sowcecuz. aqk lu loj mh dehzu svcumjz, qmkce zhwu hs lcz ghqmnuv dhqzcmz aunom kh nvht qy. klu uejuzk hs kluzu, omj aceah'z sophqvcku, toz ghqmn svhjh aonncmz. tlum aceah toz mcmukg-mcmu lu ojhykuj svhjh oz lcz lucv, omj avhqnlk lcw kh ecpu ok aon umj; omj klu lhyuz hs klu zodrpceeu- aonncmzuz tuvu scmoeeg jozluj. aceah omj svhjh loyyumuj kh lopu klu zowu acvkljog, zuykuwauv 22mj. ghq loj aukkuv dhwu omj ecpu luvu, svhjh wg eoj, zocj aceah hmu jog; omj klum tu dom dueuavoku hqv acvkljog-yovkcuz dhwshvkoaeg khnukluv. ok klok kcwu svhjh toz zkcee cm lcz ktuumz, oz klu lhaackz doeeuj klu cvvuzyhmzcaeu ktumkcuz auktuum dlcejlhhj omj dhwcmn hs onu ok klcvkg-klvuu"""

# Break both ciphers
print("SUBSTITUTION CIPHER BREAKER")
print("="*70)

# Manual refined mappings based on pattern analysis and common words
# These were derived by looking for common words like "the", "and", "of", etc.

# For cipher 1: Looking for patterns and common words
manual_map1 = {
    'i': 'e', 'd': 'o', 'c': 't', 'p': 'a', 'a': 'i',
    'f': 'n', 'e': 'h', 'g': 'd', 'u': 'f', 'k': 'r',
    'v': 'u', 'n': 'l', 'q': 'c', 'o': 'm', 't': 'w',
    'w': 'y', 'r': 's', 'x': 'p', 'h': 'b', 'j': 'q',
    'l': 'k', 'm': 'g', 's': 'v', 'b': 'x', 'y': 'z', 'z': 'j'
}

# For cipher 2: Common patterns suggest this is from Tolkien
manual_map2 = {
    'u': 'e', 'k': 't', 'l': 'h', 'o': 'a', 'h': 'o',
    'z': 's', 'm': 'n', 'c': 'i', 'v': 'r', 'j': 'd',
    'a': 'b', 'e': 'l', 's': 'f', 'w': 'm', 'q': 'u',
    'g': 'y', 'y': 'p', 'n': 'g', 't': 'w', 'p': 'v',
    'd': 'k', 'x': 'x', 'i': 'q', 'r': 'j', 'b': 'z', 'f': 'c'
}

sub_map1, decrypt1 = break_substitution(cipher1, "CIPHER-1", manual_map1)
sub_map2, decrypt2 = break_substitution(cipher2, "CIPHER-2", manual_map2)

print("\n\n" + "="*70)
print("ANALYSIS COMPLETE")
print("="*70)
print("\nFrequency analysis provides initial mapping.")
print("Manual refinement using common words gives better results.")
print("\nThe JSX file provides an interactive web interface for")
print("manual decryption - useful for experimenting with mappings!")