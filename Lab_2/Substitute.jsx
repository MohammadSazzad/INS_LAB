import React, { useState, useEffect } from 'react';
import { RefreshCw, Check } from 'lucide-react';

const SubstitutionBreaker = () => {
  const cipher1 = "af p xpkcaqvnpk pfg, af ipqe qpri, gauuikifc tpw, ceiri udvk tiki afgarxifrphni cd eao--wvmd popkwn, hiqpvri du ear jvaql vfgikrcpfgafm du cei xkafqaxnir du xrwqedearcdkw pfg du ear aopmafpcasi xkdhafmr afcd fit pkipr. ac tpr qdoudkcafm cd lfdt cepc au pfwceafm epxxifig cd ringdf eaorinu hiudki cei opceiopcaqr du cei uaing qdvng hi qdoxnicinw tdklig dvc--pfg edt rndtnw ac xkdqiigig, pfg edt odvfcpafdvr cei dhrcpqnir--ceiki tdvng pc niprc kiopaf dfi mddg oafg cepc tdvng qdfcafvi cei kiripkqe";
  
  const cipher2 = "aceah toz puvg vcdl omj puvg yudqecov, omj loj auum klu thmjuv hs klu zlcvu shv zcbkg guovz, upuv zcmdu lcz vuwovroaeu jczoyyuovomdu omj qmubyudkuj vukqvm. klu vcdluz lu loj avhqnlk aodr svhw lcz kvopuez loj mht audhwu o ehdoe eunumj, omj ck toz yhyqeoveg auecupuj, tlokupuv klu hej sher wcnlk zog, klok klu lcee ok aon umj toz sqee hs kqmmuez zkqssuj tckl kvuozqvu. omj cs klok toz mhk umhqnl shv sowu, kluvu toz oezh lcz yvhehmnuj pcnhqv kh wovpue ok. kcwu thvu hm, aqk ck zuuwuj kh lopu eckkeu ussudk hm wv. aonncmz. ok mcmukg lu toz wqdl klu zowu oz ok scskg. ok mcmukg-mcmu klug aunom kh doee lcw tuee-yvuzuvpuj; aqk qmdlomnuj thqej lopu auum muovuv klu wovr. kluvu tuvu zhwu klok zlhhr klucv luojz omj klhqnlk klcz toz khh wqdl hs o nhhj klcmn; ck zuuwuj qmsocv klok";

  const [selectedCipher, setSelectedCipher] = useState(2);
  const [mapping, setMapping] = useState({});
  const [decrypted, setDecrypted] = useState('');
  const [frequencies, setFrequencies] = useState([]);

  const cipherText = selectedCipher === 1 ? cipher1 : cipher2;

  // Initial mappings based on frequency analysis
  const initialMapping1 = {
    'i': 'e', 'p': 't', 'c': 'a', 'd': 'o', 'a': 'i',
    'f': 'n', 'k': 's', 'e': 'h', 'g': 'r', 'u': 'd',
    'n': 'l', 'v': 'u', 'q': 'c', 'o': 'm', 't': 'w',
    'w': 'f', 'm': 'g', 'x': 'y', 'h': 'p', 'r': 'b',
    's': 'v', 'l': 'k', 'j': 'j', 'b': 'x', 'y': 'q', 'z': 'z'
  };

  const initialMapping2 = {
    'u': 'e', 'k': 't', 'h': 'a', 'o': 'o', 'z': 'i',
    's': 'n', 'l': 's', 'c': 'h', 'v': 'r', 'j': 'd',
    'e': 'l', 'q': 'u', 'm': 'c', 'w': 'm', 't': 'w',
    'n': 'f', 'y': 'g', 'g': 'y', 'x': 'p', 'a': 'b',
    'p': 'v', 'd': 'k', 'r': 'j', 'b': 'x', 'i': 'q', 'f': 'z'
  };

  useEffect(() => {
    // Calculate frequencies
    const letters = cipherText.toLowerCase().match(/[a-z]/g) || [];
    const freq = {};
    letters.forEach(l => freq[l] = (freq[l] || 0) + 1);
    const total = letters.length;
    const freqArray = Object.entries(freq)
      .map(([letter, count]) => ({ letter, count, percent: (count/total*100).toFixed(2) }))
      .sort((a, b) => b.count - a.count);
    setFrequencies(freqArray);

    // Set initial mapping
    setMapping(selectedCipher === 1 ? initialMapping1 : initialMapping2);
  }, [selectedCipher]);

  useEffect(() => {
    // Apply decryption
    let result = '';
    for (let char of cipherText) {
      if (char.match(/[a-z]/i)) {
        const lower = char.toLowerCase();
        const decryptedChar = mapping[lower] || '_';
        result += char === char.toUpperCase() ? decryptedChar.toUpperCase() : decryptedChar;
      } else {
        result += char;
      }
    }
    setDecrypted(result);
  }, [mapping, cipherText]);

  const updateMapping = (cipherChar, plainChar) => {
    setMapping(prev => ({ ...prev, [cipherChar]: plainChar.toLowerCase() }));
  };

  const resetMapping = () => {
    setMapping(selectedCipher === 1 ? initialMapping1 : initialMapping2);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 text-white p-6">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold mb-2 text-center bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
          Substitution Cipher Breaker
        </h1>
        <p className="text-center text-slate-400 mb-6">Interactive Frequency Analysis Tool</p>

        {/* Cipher Selection */}
        <div className="bg-slate-800 rounded-lg p-4 mb-6 shadow-xl">
          <label className="block text-sm font-semibold mb-2 text-slate-300">Select Cipher:</label>
          <div className="flex gap-4">
            <button
              onClick={() => setSelectedCipher(1)}
              className={`flex-1 py-3 px-4 rounded-lg font-semibold transition-all ${
                selectedCipher === 1
                  ? 'bg-blue-600 text-white shadow-lg'
                  : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
              }`}
            >
              Cipher 1 (Shorter)
            </button>
            <button
              onClick={() => setSelectedCipher(2)}
              className={`flex-1 py-3 px-4 rounded-lg font-semibold transition-all ${
                selectedCipher === 2
                  ? 'bg-purple-600 text-white shadow-lg'
                  : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
              }`}
            >
              Cipher 2 (Longer)
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Frequency Analysis */}
          <div className="bg-slate-800 rounded-lg p-4 shadow-xl">
            <h2 className="text-lg font-bold mb-3 flex items-center gap-2">
              <span className="text-yellow-400">📊</span> Frequency Analysis
            </h2>
            <div className="space-y-1 max-h-96 overflow-y-auto">
              {frequencies.map(({ letter, count, percent }) => (
                <div key={letter} className="flex items-center gap-2 text-sm">
                  <span className="font-mono font-bold text-blue-400 w-6">{letter}</span>
                  <div className="flex-1 bg-slate-700 rounded-full h-4 overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-blue-500 to-purple-500"
                      style={{ width: `${Math.min(100, parseFloat(percent) * 8)}%` }}
                    />
                  </div>
                  <span className="text-slate-400 w-16 text-right">{percent}%</span>
                </div>
              ))}
            </div>
          </div>

          {/* Mapping Editor */}
          <div className="bg-slate-800 rounded-lg p-4 shadow-xl">
            <div className="flex justify-between items-center mb-3">
              <h2 className="text-lg font-bold flex items-center gap-2">
                <span className="text-green-400">🔑</span> Substitution Map
              </h2>
              <button
                onClick={resetMapping}
                className="p-2 bg-slate-700 hover:bg-slate-600 rounded-lg transition-colors"
                title="Reset to initial mapping"
              >
                <RefreshCw className="w-4 h-4" />
              </button>
            </div>
            <div className="grid grid-cols-2 gap-2 max-h-96 overflow-y-auto">
              {Object.entries(mapping).sort().map(([cipher, plain]) => (
                <div key={cipher} className="flex items-center gap-2 bg-slate-700 rounded p-2">
                  <span className="font-mono font-bold text-blue-400">{cipher}</span>
                  <span className="text-slate-400">→</span>
                  <input
                    type="text"
                    maxLength="1"
                    value={plain}
                    onChange={(e) => updateMapping(cipher, e.target.value)}
                    className="w-8 h-8 text-center bg-slate-600 border border-slate-500 rounded font-mono font-bold text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                  />
                </div>
              ))}
            </div>
          </div>

          {/* English Letter Frequencies */}
          <div className="bg-slate-800 rounded-lg p-4 shadow-xl">
            <h2 className="text-lg font-bold mb-3 flex items-center gap-2">
              <span className="text-purple-400">📖</span> English Frequencies
            </h2>
            <div className="space-y-1 text-sm max-h-96 overflow-y-auto">
              {[
                ['e', '12.22%'], ['t', '9.67%'], ['a', '8.05%'], ['o', '7.63%'],
                ['i', '6.28%'], ['n', '6.95%'], ['s', '6.02%'], ['h', '6.62%'],
                ['r', '5.29%'], ['d', '5.10%'], ['l', '4.08%'], ['u', '2.92%'],
                ['c', '2.23%'], ['m', '2.33%'], ['w', '2.60%'], ['f', '2.14%'],
                ['g', '2.30%'], ['y', '2.04%'], ['p', '1.66%'], ['b', '1.67%'],
                ['v', '0.82%'], ['k', '0.95%'], ['j', '0.19%'], ['x', '0.11%'],
                ['q', '0.06%'], ['z', '0.06%']
              ].map(([letter, freq]) => (
                <div key={letter} className="flex justify-between text-slate-300">
                  <span className="font-mono font-bold">{letter}</span>
                  <span className="text-slate-400">{freq}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Decrypted Text */}
        <div className="bg-slate-800 rounded-lg p-6 mt-6 shadow-xl">
          <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
            <span className="text-green-400">✓</span> Decrypted Text
          </h2>
          <div className="bg-slate-900 rounded-lg p-4 font-mono text-sm leading-relaxed border border-slate-700">
            {decrypted}
          </div>
        </div>

        {/* Original Cipher */}
        <div className="bg-slate-800 rounded-lg p-6 mt-6 shadow-xl">
          <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
            <span className="text-red-400">🔒</span> Original Cipher
          </h2>
          <div className="bg-slate-900 rounded-lg p-4 font-mono text-sm leading-relaxed border border-slate-700 text-slate-400">
            {cipherText}
          </div>
        </div>
      </div>
    </div>
  );
};

export default SubstitutionBreaker;