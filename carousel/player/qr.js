/* Minimalus QR kodo generatorius (byte mode, klaidu taisymo lygis M, 1-10 versijos).
   Be jokiu isoriniu biblioteku — veikia offline, kioske, be interneto.
   Naudojimas:  QR.toSvg("https://sleepingexpert.lt/...")  ->  SVG tekstas  */
window.QR = (function () {
  "use strict";

  /* ---------- GF(256) aritmetika ---------- */
  var EXP = new Uint8Array(512), LOG = new Uint8Array(256);
  (function () {
    var x = 1;
    for (var i = 0; i < 255; i++) {
      EXP[i] = x; LOG[x] = i;
      x <<= 1;
      if (x & 0x100) x ^= 0x11d;
    }
    for (var j = 255; j < 512; j++) EXP[j] = EXP[j - 255];
  })();

  function mul(a, b) {
    if (a === 0 || b === 0) return 0;
    return EXP[LOG[a] + LOG[b]];
  }

  function rsGenerator(degree) {
    var gen = [1], root = 1;
    for (var i = 0; i < degree; i++) {
      var next = new Array(gen.length + 1);
      for (var k = 0; k < next.length; k++) next[k] = 0;
      for (var j = 0; j < gen.length; j++) {
        next[j] ^= gen[j];
        next[j + 1] ^= mul(gen[j], root);
      }
      gen = next;
      root = mul(root, 2);
    }
    return gen; // gen[0] === 1
  }

  function rsRemainder(data, degree) {
    var gen = rsGenerator(degree);
    var res = new Uint8Array(degree);
    for (var i = 0; i < data.length; i++) {
      var factor = data[i] ^ res[0];
      res.copyWithin(0, 1);
      res[degree - 1] = 0;
      for (var j = 0; j < degree; j++) res[j] ^= mul(gen[j + 1], factor);
    }
    return res;
  }

  /* ---------- lenteles (EC lygis M) ---------- */
  // versija: [ec kodo zodziai bloke, 1 grupes blokai, ju duomenu zodziai, 2 grupes blokai, ju duomenu zodziai]
  var ECM = {
    1: [10, 1, 16, 0, 0],
    2: [16, 1, 28, 0, 0],
    3: [26, 1, 44, 0, 0],
    4: [18, 2, 32, 0, 0],
    5: [24, 2, 43, 0, 0],
    6: [16, 4, 27, 0, 0],
    7: [18, 4, 31, 0, 0],
    8: [22, 2, 38, 2, 39],
    9: [22, 3, 36, 2, 37],
    10: [26, 4, 43, 1, 44]
  };

  var ALIGN = {
    1: [], 2: [6, 18], 3: [6, 22], 4: [6, 26], 5: [6, 30],
    6: [6, 34], 7: [6, 22, 38], 8: [6, 24, 42], 9: [6, 26, 46], 10: [6, 28, 50]
  };

  function dataCodewords(version) {
    var t = ECM[version];
    return t[1] * t[2] + t[3] * t[4];
  }

  function countBits(version) {
    return version < 10 ? 8 : 16;
  }

  /* ---------- teksto kodavimas ---------- */
  function toUtf8(text) {
    var out = [];
    var encoded = unescape(encodeURIComponent(text));
    for (var i = 0; i < encoded.length; i++) out.push(encoded.charCodeAt(i) & 0xff);
    return out;
  }

  function pickVersion(byteLen) {
    for (var v = 1; v <= 10; v++) {
      var capacity = dataCodewords(v) * 8;
      if (4 + countBits(v) + byteLen * 8 <= capacity) return v;
    }
    return null;
  }

  function buildDataCodewords(bytes, version) {
    var bits = [];
    function push(value, len) {
      for (var i = len - 1; i >= 0; i--) bits.push((value >>> i) & 1);
    }
    push(4, 4);                       // byte mode
    push(bytes.length, countBits(version));
    for (var i = 0; i < bytes.length; i++) push(bytes[i], 8);

    var capacity = dataCodewords(version) * 8;
    var terminator = Math.min(4, capacity - bits.length);
    push(0, terminator);
    while (bits.length % 8 !== 0) bits.push(0);

    var words = [];
    for (var b = 0; b < bits.length; b += 8) {
      var byte = 0;
      for (var k = 0; k < 8; k++) byte = (byte << 1) | bits[b + k];
      words.push(byte);
    }
    var pads = [0xec, 0x11], p = 0;
    while (words.length < dataCodewords(version)) {
      words.push(pads[p % 2]);
      p++;
    }
    return words;
  }

  function interleave(words, version) {
    var t = ECM[version];
    var ecLen = t[0];
    var blocks = [], ecBlocks = [];
    var offset = 0;
    var specs = [];
    for (var i = 0; i < t[1]; i++) specs.push(t[2]);
    for (var j = 0; j < t[3]; j++) specs.push(t[4]);
    for (var s = 0; s < specs.length; s++) {
      var chunk = words.slice(offset, offset + specs[s]);
      offset += specs[s];
      blocks.push(chunk);
      ecBlocks.push(rsRemainder(chunk, ecLen));
    }
    var result = [];
    var maxData = Math.max.apply(null, specs);
    for (var c = 0; c < maxData; c++) {
      for (var bi = 0; bi < blocks.length; bi++) {
        if (c < blocks[bi].length) result.push(blocks[bi][c]);
      }
    }
    for (var e = 0; e < ecLen; e++) {
      for (var bj = 0; bj < ecBlocks.length; bj++) result.push(ecBlocks[bj][e]);
    }
    return result;
  }

  /* ---------- matricos formavimas ---------- */
  function makeMatrix(version) {
    var size = version * 4 + 17;
    var modules = [], isFunc = [];
    for (var y = 0; y < size; y++) {
      modules.push(new Array(size).fill(false));
      isFunc.push(new Array(size).fill(false));
    }
    return { size: size, modules: modules, isFunc: isFunc, version: version };
  }

  function setFunc(m, x, y, dark) {
    if (x < 0 || y < 0 || x >= m.size || y >= m.size) return;
    m.modules[y][x] = !!dark;
    m.isFunc[y][x] = true;
  }

  function drawFinder(m, ox, oy) {
    for (var dy = -1; dy <= 7; dy++) {
      for (var dx = -1; dx <= 7; dx++) {
        var dist = Math.max(Math.abs(dx - 3), Math.abs(dy - 3));
        setFunc(m, ox + dx, oy + dy, dist !== 2 && dist !== 4);
      }
    }
  }

  function drawAlignment(m, cx, cy) {
    for (var dy = -2; dy <= 2; dy++) {
      for (var dx = -2; dx <= 2; dx++) {
        setFunc(m, cx + dx, cy + dy, Math.max(Math.abs(dx), Math.abs(dy)) !== 1);
      }
    }
  }

  function formatBits(mask) {
    var data = (0 << 3) | mask;           // EC lygis M -> 0b00
    var rem = data;
    for (var i = 0; i < 10; i++) rem = (rem << 1) ^ ((rem >>> 9) * 0x537);
    return ((data << 10) | (rem & 0x3ff)) ^ 0x5412;
  }

  function versionBits(version) {
    var rem = version;
    for (var i = 0; i < 12; i++) rem = (rem << 1) ^ ((rem >>> 11) * 0x1f25);
    return (version << 12) | (rem & 0xfff);
  }

  function bitAt(value, index) {
    return ((value >>> index) & 1) === 1;
  }

  function drawFormat(m, mask) {
    var bits = formatBits(mask);
    var i;
    for (i = 0; i <= 5; i++) setFunc(m, 8, i, bitAt(bits, i));
    setFunc(m, 8, 7, bitAt(bits, 6));
    setFunc(m, 8, 8, bitAt(bits, 7));
    setFunc(m, 7, 8, bitAt(bits, 8));
    for (i = 9; i < 15; i++) setFunc(m, 14 - i, 8, bitAt(bits, i));
    for (i = 0; i < 8; i++) setFunc(m, m.size - 1 - i, 8, bitAt(bits, i));
    for (i = 8; i < 15; i++) setFunc(m, 8, m.size - 15 + i, bitAt(bits, i));
    setFunc(m, 8, m.size - 8, true); // tamsus modulis
  }

  function drawFunctionPatterns(m) {
    var i;
    for (i = 0; i < m.size; i++) {
      setFunc(m, 6, i, i % 2 === 0);
      setFunc(m, i, 6, i % 2 === 0);
    }
    drawFinder(m, 0, 0);
    drawFinder(m, m.size - 7, 0);
    drawFinder(m, 0, m.size - 7);

    var centers = ALIGN[m.version];
    for (var a = 0; a < centers.length; a++) {
      for (var b = 0; b < centers.length; b++) {
        var skipTL = (a === 0 && b === 0);
        var skipTR = (a === 0 && b === centers.length - 1);
        var skipBL = (a === centers.length - 1 && b === 0);
        if (!skipTL && !skipTR && !skipBL) drawAlignment(m, centers[b], centers[a]);
      }
    }

    if (m.version >= 7) {
      var vb = versionBits(m.version);
      for (i = 0; i < 18; i++) {
        var bit = bitAt(vb, i);
        var x = m.size - 11 + (i % 3);
        var y = Math.floor(i / 3);
        setFunc(m, x, y, bit);
        setFunc(m, y, x, bit);
      }
    }
    drawFormat(m, 0); // vietos rezervavimas, tikra reiksme irasoma veliau
  }

  function drawCodewords(m, words) {
    var i = 0;
    for (var right = m.size - 1; right >= 1; right -= 2) {
      if (right === 6) right = 5;
      for (var vert = 0; vert < m.size; vert++) {
        for (var j = 0; j < 2; j++) {
          var x = right - j;
          var upward = ((right + 1) & 2) === 0;
          var y = upward ? m.size - 1 - vert : vert;
          if (!m.isFunc[y][x] && i < words.length * 8) {
            m.modules[y][x] = bitAt(words[i >>> 3], 7 - (i & 7));
            i++;
          }
        }
      }
    }
  }

  function maskBit(mask, x, y) {
    switch (mask) {
      case 0: return (x + y) % 2 === 0;
      case 1: return y % 2 === 0;
      case 2: return x % 3 === 0;
      case 3: return (x + y) % 3 === 0;
      case 4: return (Math.floor(x / 3) + Math.floor(y / 2)) % 2 === 0;
      case 5: return ((x * y) % 2) + ((x * y) % 3) === 0;
      case 6: return (((x * y) % 2) + ((x * y) % 3)) % 2 === 0;
      case 7: return (((x + y) % 2) + ((x * y) % 3)) % 2 === 0;
    }
    return false;
  }

  function applyMask(m, mask) {
    for (var y = 0; y < m.size; y++) {
      for (var x = 0; x < m.size; x++) {
        if (!m.isFunc[y][x] && maskBit(mask, x, y)) m.modules[y][x] = !m.modules[y][x];
      }
    }
  }

  var FINDER_LIKE = [true, false, true, true, true, false, true];

  function lineHasFinderAt(line, start) {
    for (var i = 0; i < 7; i++) {
      if (line[start + i] !== FINDER_LIKE[i]) return false;
    }
    return true;
  }

  function penaltyForLines(lines, size) {
    var score = 0;
    for (var l = 0; l < lines.length; l++) {
      var line = lines[l];
      // 1 taisykle: 5+ vienodu moduliu serija
      var run = 1;
      for (var i = 1; i < size; i++) {
        if (line[i] === line[i - 1]) {
          run++;
        } else {
          if (run >= 5) score += 3 + (run - 5);
          run = 1;
        }
      }
      if (run >= 5) score += 3 + (run - 5);
      // 3 taisykle: 1011101 su 4 sviesiais moduliais viename sone
      for (var s = 0; s + 6 < size; s++) {
        if (!lineHasFinderAt(line, s)) continue;
        // uz matricos ribu esanti tyli zona laikoma sviesia (ISO/IEC 18004)
        var before = true, after = true;
        for (var b = 1; b <= 4; b++) {
          if (s - b >= 0 && line[s - b] !== false) { before = false; break; }
        }
        for (var a = 1; a <= 4; a++) {
          if (s + 6 + a < size && line[s + 6 + a] !== false) { after = false; break; }
        }
        if (before || after) score += 40;
      }
    }
    return score;
  }

  function penalty(m) {
    var size = m.size, score = 0, x, y;
    var rows = m.modules;
    var cols = [];
    for (x = 0; x < size; x++) {
      var col = new Array(size);
      for (y = 0; y < size; y++) col[y] = rows[y][x];
      cols.push(col);
    }
    score += penaltyForLines(rows, size);
    score += penaltyForLines(cols, size);

    // 2 taisykle: 2x2 vienodos spalvos blokai
    for (y = 0; y < size - 1; y++) {
      for (x = 0; x < size - 1; x++) {
        var v = rows[y][x];
        if (v === rows[y][x + 1] && v === rows[y + 1][x] && v === rows[y + 1][x + 1]) score += 3;
      }
    }

    // 4 taisykle: tamsiu moduliu proporcija
    var dark = 0;
    for (y = 0; y < size; y++) for (x = 0; x < size; x++) if (rows[y][x]) dark++;
    var ratio = Math.abs((100 * dark) / (size * size) - 50) / 5;
    score += Math.floor(ratio) * 10;
    return score;
  }

  function encode(text, forcedMask) {
    var bytes = toUtf8(String(text == null ? "" : text));
    var version = pickVersion(bytes.length);
    if (!version) throw new Error("QR: tekstas per ilgas (max ~200 simboliu)");
    var words = interleave(buildDataCodewords(bytes, version), version);

    var best = null, bestScore = Infinity;
    var masks = (forcedMask === undefined || forcedMask === null) ? [0, 1, 2, 3, 4, 5, 6, 7] : [forcedMask];
    for (var mi = 0; mi < masks.length; mi++) {
      var m = makeMatrix(version);
      drawFunctionPatterns(m);
      drawCodewords(m, words);
      applyMask(m, masks[mi]);
      drawFormat(m, masks[mi]);
      var score = penalty(m);
      if (score < bestScore) {
        bestScore = score;
        best = m;
        best.mask = masks[mi];
      }
    }
    return { size: best.size, modules: best.modules, version: version, mask: best.mask };
  }

  function toSvg(text, options) {
    var opts = options || {};
    var quiet = opts.quiet === undefined ? 2 : opts.quiet;
    var dark = opts.dark || "#142b6f";
    var light = opts.light || "#ffffff";
    var qr = encode(text);
    var dim = qr.size + quiet * 2;
    var path = [];
    for (var y = 0; y < qr.size; y++) {
      for (var x = 0; x < qr.size; x++) {
        if (qr.modules[y][x]) path.push("M" + (x + quiet) + " " + (y + quiet) + "h1v1h-1z");
      }
    }
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + dim + " " + dim +
      '" shape-rendering="crispEdges" role="img" aria-label="QR kodas">' +
      '<rect width="' + dim + '" height="' + dim + '" fill="' + light + '"/>' +
      '<path fill="' + dark + '" d="' + path.join("") + '"/></svg>';
  }

  return { encode: encode, toSvg: toSvg };
})();
