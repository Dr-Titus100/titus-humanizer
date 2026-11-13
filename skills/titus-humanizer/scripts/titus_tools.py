"""titus-humanizer tools: hidden-character cleanup and an AI-pattern score from 0 to 1.

Usage:
  python3 titus_tools.py clean INPUT > CLEANED          (cleanup counts go to stderr)
  python3 titus_tools.py score INPUT                    (score report for one text)
  python3 titus_tools.py report ORIGINAL REWRITE        (before/after report)

Standard library only. The score is a gauge of the patterns this skill targets.
It is not an authorship verdict and does not stand in for any commercial detector.
"""
import math, re, sys, unicodedata
from collections import Counter

# ---------------------------------------------------------------- cleanup

ZERO_WIDTH = {0x200B: "zero-width space", 0x2060: "word joiner", 0xFEFF: "byte-order mark",
              0x00AD: "soft hyphen", 0x180E: "Mongolian vowel separator",
              0x2061: "invisible operator", 0x2062: "invisible operator",
              0x2063: "invisible operator", 0x2064: "invisible operator",
              0x115F: "Hangul filler", 0x1160: "Hangul filler", 0x3164: "Hangul filler", 0xFFA0: "Hangul filler"}
JOINERS = {0x200C: "zero-width non-joiner", 0x200D: "zero-width joiner"}
BIDI = set(range(0x202A, 0x202F)) | set(range(0x2066, 0x206A)) | {0x200E, 0x200F, 0x061C}
SPACES = {0x00A0, 0x202F, 0x205F, 0x3000, 0x1680} | set(range(0x2000, 0x200B))
HOMOGLYPHS = {"а": "a", "е": "e", "о": "o", "р": "p", "с": "c", "у": "y",
              "х": "x", "і": "i", "ј": "j", "ѕ": "s", "А": "A", "В": "B",
              "Е": "E", "К": "K", "М": "M", "Н": "H", "О": "O", "Р": "P",
              "С": "C", "Т": "T", "Х": "X", "ο": "o", "α": "a", "Ο": "O"}
SCRIPT_RANGES = [(0x0600, 0x06FF), (0x0750, 0x077F), (0x0900, 0x0DFF), (0x0F00, 0x0FFF), (0x1780, 0x17FF)]
COMPLEX_SCRIPTS = re.compile("[" + "".join(f"{chr(a)}-{chr(b)}" for a, b in SCRIPT_RANGES) + "]")


def _is_emoji(ch):
    return bool(ch) and (unicodedata.category(ch) == "So" or 0x1F000 <= ord(ch) <= 0x1FAFF)


# Code blocks, inline code and URLs pass through untouched.
PROTECTED = re.compile(r"`{3}.*?`{3}|`[^`\n]*`|\b(?:https?|ftp)://\S+|\bwww\.\S+", re.S)
REMOVED = "\x00"   # marks where a character was removed, so spacing is fixed only there


def _in_flag_tags(chars, i):
    """True when chars[i] is a tag character inside a flag sequence such as England's (U+1F3F4 + tags + U+E007F)."""
    j = i
    while j > 0 and 0xE0020 <= ord(chars[j - 1]) <= 0xE007E:
        j -= 1
    if j == 0 or ord(chars[j - 1]) != 0x1F3F4:
        return False
    k = i
    while k < len(chars) and 0xE0020 <= ord(chars[k]) <= 0xE007E:
        k += 1
    return k < len(chars) and ord(chars[k]) == 0xE007F


def _clean_prose(text, found):
    out = []
    chars = list(text)
    for i, ch in enumerate(chars):
        cp = ord(ch)
        prev = chars[i - 1] if i else ""
        nxt = chars[i + 1] if i + 1 < len(chars) else ""
        if cp in ZERO_WIDTH:
            found[ZERO_WIDTH[cp]] += 1
            out.append(REMOVED)
        elif cp in JOINERS:
            keep = _is_emoji(prev) or _is_emoji(nxt) or COMPLEX_SCRIPTS.match(prev or " ") or COMPLEX_SCRIPTS.match(nxt or " ")
            if keep:
                out.append(ch)
            else:
                found[JOINERS[cp]] += 1
                out.append(REMOVED)
        elif cp in BIDI:
            found["text-direction control"] += 1
            out.append(REMOVED)
        elif 0xE0000 <= cp <= 0xE007F:
            if _in_flag_tags(chars, i) or (cp == 0xE007F and i and 0xE0020 <= ord(prev) <= 0xE007E and _in_flag_tags(chars, i - 1)):
                out.append(ch)
            else:
                found["invisible tag character"] += 1
                out.append(REMOVED)
        elif 0xFE00 <= cp <= 0xFE0F or 0xE0100 <= cp <= 0xE01EF:
            if _is_emoji(prev):
                out.append(ch)
            else:
                found["variation selector"] += 1
                out.append(REMOVED)
        elif 0xE000 <= cp <= 0xF8FF or 0xF0000 <= cp <= 0x10FFFD or 0xFDD0 <= cp <= 0xFDEF or (cp & 0xFFFE) == 0xFFFE:
            found["private-use or non-character"] += 1
            out.append(REMOVED)
        elif cp in SPACES:
            found["unusual space"] += 1
            out.append(" ")
        else:
            out.append(ch)
    text = "".join(out)
    # Where a removal left two spaces side by side ("word \u200b word"), keep one. Other space runs stay as they are.
    text = re.sub(r" *\x00[ \x00]*", lambda m: " " if " " in m.group(0) else "", text)

    def fix_word(m):
        w = m.group(0)
        latin = sum(c.isascii() and c.isalpha() for c in w)
        fake = sum(c in HOMOGLYPHS for c in w)
        if fake and latin and latin + fake == sum(c.isalpha() for c in w):
            found["look-alike letter"] += fake
            return "".join(HOMOGLYPHS.get(c, c) for c in w)
        return w

    return re.sub(r"\w+", fix_word, text)


def clean(text):
    found = Counter()
    parts, last = [], 0
    for m in PROTECTED.finditer(text):
        parts.append(_clean_prose(text[last:m.start()], found))
        parts.append(m.group(0))
        last = m.end()
    parts.append(_clean_prose(text[last:], found))
    return "".join(parts), found


def describe_found(found):
    if not found:
        return "none"
    parts = []
    for name, n in found.most_common():
        parts.append(f"{n} {name}{'' if n == 1 else 's'}")
    return ", ".join(parts)

# ---------------------------------------------------------------- scoring

MIN_WORDS = 30          # below this, no score
FULL_WORDS = 100        # below this, the score is dampened

# (label, regex, weight). Weights are per hit. Patterns follow the skill's own parts.
PATTERNS = [
    # Part 1 hard rules
    ("em dash", r"—", 1.0),
    ("dash used as a break", r"(?<=\S)[ \t]+[–-][ \t]+(?=\S)", 0.6),
    ("semicolon", r";(?=\s)", 0.8),
    ("arrow, bar or inline dot", r"(?<=\S)[ \t]+(?:→|->|=>|⇒|\||•|·|●|▪)[ \t]+(?=\S)", 0.8),
    ("reject-then-assert", r"\b(?:is|are|was|were|it'?s|this is|that'?s)\s*(?:n't|not)\s+(?:just|only|merely|simply|about)?\b[^.!?]{0,70}?[,.—]\s*(?:it'?s|it is|they'?re|but|this is)\b", 1.0),
    ("not only / not just ... but", r"\bnot\s+(?:only|just|merely)\b[^.!?]{1,80}\bbut\b", 1.0),
    ("rather than contrast", r"\brather\s+than\b", 0.4),
    ("passive voice (heuristic)", r"\b(?:is|are|was|were|be|been|being)\s+(?:\w+ly\s+)?(?:\w+ed|built|done|made|given|taken|seen|known|shown|written|held|kept|led|set|found)\b", 0.35),
    ("slogan fragment", r"(?:^|[.!?]\s+)(?:One|No|Every)\s+\w+\.\s+(?:One|No|Every)\s+\w+\.", 1.2),
    ("illustrative hedging", r"\b(?:illustrative|for reference only|for discussion only|directional(?:ly)?|placeholder (?:data|values?))\b", 0.9),
    ("chatbot residue", r"\b(?:certainly!|great question|i hope this helps|let me know if|happy to help|as an ai\b|here(?:'s| is) (?:a|an|the) (?:polished|revised|rewritten)|below is (?:a|an|the))", 1.5),
    # Part 3 substance and tone
    ("inflated significance", r"\b(?:pivotal (?:moment|role)|a testament to|stands? as a|plays? a (?:vital|crucial|key|pivotal) role|evolving landscape|indelible mark|deeply rooted|marks? a (?:shift|turning point|new era)|setting the stage|broader (?:trend|movement|shift))\b", 1.0),
    ("vague authority", r"\b(?:experts (?:say|argue|note|agree|believe)|observers (?:note|say)|research (?:shows|suggests|consistently)|studies (?:show|suggest)|several sources|industry reports|critics (?:say|argue))\b", 0.8),
    ("tacked-on -ing clause", r",\s+(?:highlighting|underscoring|emphasizing|ensuring|reflecting|symbolizing|showcasing|contributing to|fostering|cementing|solidifying|paving the way)\b", 0.9),
    ("copula avoidance", r"\b(?:serves? as|stands? as|functions? as|boasts?)\b", 0.6),
    ("synthetic balance", r"\bwhile\b[^.!?]{3,60}\b(?:offers?|provides?|brings?)\b[^.!?]{3,60}\balso (?:presents?|poses?|brings?|comes with)\b", 0.9),
    ("canned ending", r"(?:^|[.!?]\s+)(?:in conclusion|in summary|overall|ultimately|to sum up|all in all|at the end of the day)\b", 0.8),
    ("over-hedging", r"\b(?:may potentially|could possibly|might possibly|it may be worth considering)\b", 0.8),
    ("bureaucratic filler", r"\b(?:at this point in time|in order to|due to the fact that|the process of|each and every|first and foremost)\b", 0.6),
    # Part 4 vocabulary
    ("AI vocabulary", r"\b(?:delve[sd]?|tapestry|testament|pivotal|crucial|underscor(?:e|es|ed|ing)|showcas(?:e|es|ed|ing)|foster(?:s|ed|ing)?|intricate|interplay|landscape|realm|navigat(?:e|es|ing) (?:the|a)|embark(?:s|ed|ing)?|meticulous(?:ly)?|vibrant|enduring|garner(?:s|ed)?|bolster(?:s|ed)?|resonat(?:e|es|ed)|robust|seamless(?:ly)?|holistic|synerg(?:y|ies|istic)|multifaceted|transformative|groundbreaking|game[- ]changer|paradigm shift|nestled|leverag(?:e|es|ed|ing)|harness(?:es|ed|ing)?|unlock(?:s|ed|ing)?|elevat(?:e|es|ed)|empower(?:s|ed|ing)?|utiliz(?:e|es|ed|ing)|facilitat(?:e|es|ed)|commence[sd]?)\b", 0.6),
    ("stock opener", r"\b(?:in today's (?:(?:fast-paced|digital|ever-changing|modern|rapidly changing)\s+){1,2}(?:world|landscape|era|age)|when it comes to|it'?s (?:important|worth) (?:to note|noting)|it is important to (?:note|remember))\b", 0.9),
    ("sentence-initial connector", r"(?:^|[.!?]\s+)(?:Additionally|Moreover|Furthermore|Notably)\b", 0.6),
    # Part 5 formatting
    ("bold-label bullet", r"(?m)^\s*[-*•]\s+\*\*[^*]{1,40}:\*\*", 0.6),
    # Part 6 narrative tells
    ("stated lesson", r"\b(?:(?:she|he|they|i|we) (?:finally |now |at last )?(?:realized|understood|learned) (?:that|now|at last)|and so (?:she|he|they|i) learned|the lesson was)\b", 0.8),
    ("emotion as body sensation", r"\b(?:(?:chest|throat|stomach|jaw) (?:tightened|clenched|dropped|knotted|closed)|heart (?:pounded|hammered|raced|sank)|breath (?:caught|hitched)|(?:a )?(?:chill|shiver|ice) (?:ran|crawled|crept) (?:down|up) (?:her|his|their|my) spine|cold sweat)\b", 0.8),
    ("setting as mirror", r"\b(?:mirroring (?:the|her|his|their|my)|as if the (?:sky|weather|world|room|storm) (?:knew|understood|mourned|felt)|(?:the|a) storm (?:inside|within) (?:her|him|them|me))\b", 0.9),
    ("decorative smell", r"\b(?:smelled of|scent of|aroma of|the smell of)\b", 0.4),
    ("tidy inner resolution", r"\b(?:made peace with|for the first time in (?:years|a long time|forever)|(?:finally|at last) (?:felt|understood|accepted))\b", 0.8),
]
COMPILED = [(label, re.compile(rx, re.IGNORECASE), w) for label, rx, w in PATTERNS]
MONTH = r"(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|june?|july?|aug(?:ust)?|sep(?:t|tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\.?"
RANGE_END = re.compile(r"(?:\d+(?:[./]\d+)*|" + MONTH + r"|spring|summer|fall|autumn|winter|q[1-4]|h[12]|fy\d{2,4}|present|current|now|today|ongoing)$", re.IGNORECASE)


def _is_range(body, m):
    """True when a spaced dash sits between dates, years or numbers, as in 'Jul 2020 – Jun 2021'."""
    left = re.search(r"(\S+)\s*$", body[:m.start()])
    right = re.match(r"\s*(\S+)", body[m.end():])
    if not left or not right:
        return False
    lw = left.group(1).strip(",;:().")
    rw = right.group(1).strip(",;:().")
    return bool(RANGE_END.match(lw)) and bool(RANGE_END.match(rw))


# Matches that a filter rejects are not counted (for example, date ranges on a resume).
FILTERS = {"dash used as a break": lambda body, m: not _is_range(body, m)}

# Words keep their apostrophes, straight or curly, so "don't" and "don’t" each count as one word.
WORD_RE = re.compile(r"[A-Za-z0-9À-ɏ'\u2019]+")


# Quoted text is left as written, so it isn't scored. A quotation needs an opening and a closing
# mark in the same paragraph. The opening mark comes after a space, a bracket, a dash, another
# quote mark or the start of a line. The closing mark comes before a space, punctuation, a bracket,
# a dash, another quote mark or the end of a line. That keeps apostrophes ("don't", "students'")
# and inch marks (a 12" tablet) in the score. Block-quote lines starting with ">" are skipped too.
_OPEN_AFTER = r"(?<![^\s(\[{\u2014\u2013\"'\u201c\u2018])"
_CLOSE_BEFORE = r"(?=[\s.,;:!?)\]}\u2014\u2013\"'\u201d\u2019]|$)"
_INSIDE = r"(?=\S)(?:(?!\n\s*\n).)*?(?<=\S)"
# One pattern for both kinds, so the outer quote wins when one sits inside the other.
QUOTED = re.compile(_OPEN_AFTER + r"(?:[\"\u201c]" + _INSIDE + r"[\"\u201d]|['\u2018]" + _INSIDE + r"['\u2019])"
                    + _CLOSE_BEFORE, re.S | re.M)
BLOCK_QUOTE = re.compile(r"^[ \t]*>.*$", re.M)


def _strip_code(text):
    """Remove code, quoted text, links and file paths before scoring."""
    text = re.sub(r"`{3}.*?`{3}", " ", text, flags=re.S)
    text = re.sub(r"`[^`]*`", " ", text)
    # When a quote ends a sentence, leave a period in its place so the script still finds the next sentence.
    def blank(m):
        return " . " if re.search(r"[.!?]\W*$", m.group(0)) else " "
    for rx in (BLOCK_QUOTE, QUOTED):
        text = rx.sub(blank, text)
    return _blank_links_and_paths(text)


def _quotation_spans(text):
    """(start, end) of every quotation and block-quote line, in reading order."""
    spans = [m.span() for m in BLOCK_QUOTE.finditer(text)]
    blanked = BLOCK_QUOTE.sub(lambda m: " " * len(m.group(0)), text)
    spans += [m.span() for m in QUOTED.finditer(blanked)]
    return sorted(spans)


def quotations(text):
    """Every quotation and block-quote line the script skips, in reading order. A quote nested
    inside another one comes back as part of the outer quote."""
    return [text[a:b] for a, b in _quotation_spans(text)]


# Items the rewrite must carry over exactly. The report checks each one from the original against the
# same kind of item found in the rewrite, so a link that gains or loses characters counts as changed.
KEPT_CODE = re.compile(r"`{3}.*?`{3}|`[^`\n]+`", re.S)
KEPT_LINK = re.compile(r"\b(?:https?|ftp)://[^\s<>\"'`]+|\bwww\.[^\s<>\"'`]+")
# A Unix or home path (~/notes/plan.md, /etc/hosts, ./run.sh) or a Windows path (C:\\data\\run.csv).
KEPT_PATH = re.compile(r"(?<![\w/:.])(?:~|\.{1,2})?/(?:[\w.\-]+/)*[\w.\-]+|\b[A-Za-z]:\\(?:[\w.\-]+\\)*[\w.\-]+")
_TRAILING = ".,;:!?)]}"
KEPT_KINDS = ("quotation", "code snippet", "file path", "link", "emoji")


def _is_regional(ch):
    return 0x1F1E6 <= ord(ch) <= 0x1F1FF


def _trim_link(link):
    """Drop the sentence punctuation that follows a link. A closing bracket stays when the link
    opened one, as in https://en.wikipedia.org/wiki/Function_(mathematics)."""
    while link and link[-1] in _TRAILING:
        close = link[-1]
        opener = {")": "(", "]": "[", "}": "{"}.get(close)
        if opener and link.count(opener) >= link.count(close):
            break
        link = link[:-1]
    return link


def _emoji_runs(text):
    """Each emoji, with its joiners, variation selectors and skin tones, as one item."""
    runs, i, chars = [], 0, list(text)
    while i < len(chars):
        if not _is_emoji(chars[i]):
            i += 1
            continue
        # A flag is two regional-indicator letters, such as U+1F1FA U+1F1F8 for the US flag.
        if _is_regional(chars[i]) and i + 1 < len(chars) and _is_regional(chars[i + 1]):
            runs.append(chars[i] + chars[i + 1])
            i += 2
            continue
        j = i + 1
        while j < len(chars):
            cp = ord(chars[j])
            if cp in (0x200D, 0xFE0F) or 0x1F3FB <= cp <= 0x1F3FF or (0xE0020 <= cp <= 0xE007F):
                j += 1
            elif ord(chars[j - 1]) == 0x200D and _is_emoji(chars[j]):
                j += 1
            else:
                break
        runs.append("".join(chars[i:j]))
        i = j
    return runs


def _is_path(item):
    # A path needs at least two parts or a file extension, so "and/or" and "/s" don't count.
    return item.count("/") + item.count("\\") >= 2 or bool(re.search(r"\.\w+$", item))


def _blank_links_and_paths(text):
    """Blank out links and file paths with spaces of the same length. Punctuation that ends the
    sentence after one stays, so the script still finds the sentence break."""
    def link(m):
        item = _trim_link(m.group(0))
        return " " * len(item) + m.group(0)[len(item):]
    def path(m):
        item = m.group(0).rstrip(_TRAILING)
        return " " * len(item) + m.group(0)[len(item):] if _is_path(item) else m.group(0)
    return KEPT_PATH.sub(path, KEPT_LINK.sub(link, text))


def kept_items(text):
    """The quotations, code snippets, file paths, links and emoji in a text, by kind. The script
    counts each piece of text once. A link inside code counts as code, and code inside a quotation
    counts as part of the quotation."""
    found = {kind: [] for kind in KEPT_KINDS}
    blank = lambda m: " " * len(m.group(0))
    # The script finds quotations with code blanked out, so a backtick or quote mark inside code
    # can't end one early. It compares each quotation with its code in place, so swapping the code
    # inside a quote changes it.
    code = [m.span() for m in KEPT_CODE.finditer(text)]
    quotes = _quotation_spans(KEPT_CODE.sub(blank, text))
    found["quotation"] = [text[a:b] for a, b in quotes]
    found["code snippet"] = [text[a:b] for a, b in code if not any(qa <= a and b <= qb for qa, qb in quotes)]
    rest = list(text)
    for a, b in code + quotes:
        rest[a:b] = " " * (b - a)
    rest = "".join(rest)
    for m in KEPT_LINK.finditer(rest):
        found["link"].append(_trim_link(m.group(0)))
    rest = KEPT_LINK.sub(blank, rest)
    for m in KEPT_PATH.finditer(rest):
        item = m.group(0).rstrip(_TRAILING)
        if _is_path(item):
            found["file path"].append(item)
    found["emoji"] = _emoji_runs(rest)
    return found


def _kept_line(original, rewrite):
    """Report lines saying which quotations, code snippets, file paths, links and emoji came through
    unchanged, and which changed."""
    before, after = kept_items(original), kept_items(rewrite)
    kept, changed = [], []
    for kind in KEPT_KINDS:
        items = before[kind]
        if not items:
            continue
        pool = list(after[kind])
        ok = 0
        for item in items:
            if item in pool:
                pool.remove(item)
                ok += 1
        n = len(items)
        if ok == n:
            kept.append(_count(n, kind))
        else:
            changed.append(f"{n - ok} of {_count(n, kind)}")
    lines = []
    if kept:
        lines.append(f"Left as-is: {_join(kept)}")
    if changed:
        lines.append(f"Changed in the rewrite: {_join(changed)}. Restore them from the original.")
    return lines


def _skipped_line(text):
    """The score report's line naming the quotations, code snippets, file paths, links and emoji
    that a rewrite keeps as written and the score leaves out."""
    found = kept_items(text)
    parts = [_count(len(found[kind]), kind) for kind in KEPT_KINDS if found[kind]]
    return f"Left as-is and not scored: {_join(parts)}" if parts else None


def _count(n, kind):
    return f"{n} {kind if n == 1 or kind == 'emoji' else kind + 's'}"


def _join(parts):
    return parts[0] if len(parts) == 1 else ", ".join(parts[:-1]) + " and " + parts[-1]


def _sentences(text):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    chunks = re.split(r"(?<=[.!?])\s+|\n+", "\n".join(lines))
    return [c for c in (s.strip() for s in chunks) if WORD_RE.search(c)]


def _mattr(words, window=50):
    if not words:
        return 0.0
    if len(words) <= window:
        return len(set(words)) / len(words)
    counts = Counter(words[:window])
    total = len(counts) / window
    for i in range(1, len(words) - window + 1):
        old, new = words[i - 1], words[i + window - 1]
        counts[old] -= 1
        if counts[old] == 0:
            del counts[old]
        counts[new] += 1
        total += len(counts) / window
    return total / (len(words) - window + 1)


def score(text):
    body = _strip_code(text)
    words = [w.lower() for w in WORD_RE.findall(body)]
    n = len(words)
    sents = _sentences(body)
    hits = []
    weighted = 0.0
    for label, rx, w in COMPILED:
        keep = FILTERS.get(label, lambda b, m: True)
        found = [m.group(0) for m in rx.finditer(body) if keep(body, m)]
        if found:
            hits.append((label, len(found), found[0].strip()))
            weighted += w * len(found)
    result = {"words": n, "sentences": len(sents), "patterns": hits}
    if n < MIN_WORDS:
        result.update(status="too short to score", score=None, tier="not scored")
        return result

    density = weighted / (n / 100.0)
    pattern_part = min(1.0, density / 4.0)

    lengths = [len(WORD_RE.findall(s)) for s in sents]
    if len(lengths) >= 3:
        mean = sum(lengths) / len(lengths)
        sd = math.sqrt(sum((x - mean) ** 2 for x in lengths) / (len(lengths) - 1))
        cv = sd / mean if mean else 0.0
        band = sum(8 <= x <= 20 for x in lengths) / len(lengths)
        rhythm_part = max(0.0, min(1.0, (0.6 - cv) / 0.4))
        if band >= 0.85 and len(lengths) >= 5:
            rhythm_part = max(rhythm_part, 0.7)
        firsts = Counter(WORD_RE.findall(s)[0].lower() for s in sents if WORD_RE.findall(s))
        opener_part = min(1.0, max(0.0, (firsts.most_common(1)[0][1] / len(sents) - 0.2) / 0.3))
    else:
        cv, rhythm_part, opener_part = None, None, 0.0

    mattr = _mattr(words)
    diversity_part = 0.6 if 0.68 <= mattr <= 0.78 else 0.15

    if rhythm_part is None:
        raw = (pattern_part * 0.6 + opener_part * 0.1 + diversity_part * 0.1) / 0.8
    else:
        raw = pattern_part * 0.55 + rhythm_part * 0.25 + opener_part * 0.1 + diversity_part * 0.1
    raw = max(raw, pattern_part * 0.8)
    damp = 1.0 if n >= FULL_WORDS else 0.6 + 0.4 * (n - MIN_WORDS) / (FULL_WORDS - MIN_WORDS)
    s = round(max(0.0, min(1.0, raw * damp)), 2)
    tier = "high" if s >= 0.6 else "medium" if s >= 0.35 else "low"
    result.update(status="scored", score=s, tier=tier, density=round(density, 2),
                  sentence_cv=None if cv is None else round(cv, 2), mattr=round(mattr, 2),
                  dampened=damp < 1.0)
    return result


def _score_line(r):
    if r["score"] is None:
        return f"not scored ({r['words']} words, needs at least {MIN_WORDS})"
    return f"{r['score']:.2f} ({r['tier']})"


def _pattern_line(r, limit=6):
    if not r["patterns"]:
        return "none"
    items = sorted(r["patterns"], key=lambda h: -h[1])[:limit]
    return ", ".join(f"{label} x{count}" for label, count, _ in items)


def report(original, rewrite):
    clean_orig, found_orig = clean(original)
    clean_new, found_new = clean(rewrite)
    before, after = score(clean_orig), score(clean_new)
    lines = [
        f"AI-pattern score: {_score_line(before)} before, {_score_line(after)} after",
        f"Patterns before: {_pattern_line(before)}",
        f"Patterns left after: {_pattern_line(after)}",
        f"Hidden characters removed: {describe_found(found_orig)}",
    ]
    lines += _kept_line(clean_orig, clean_new)
    if found_new:
        lines.append(f"Hidden characters removed from the rewrite: {describe_found(found_new)}")
    if before.get("dampened") or after.get("dampened"):
        lines.append("Note: the text is short, so the script dampened the score and it is less reliable.")
    return "\n".join(lines), clean_new


def _read(path):
    return sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()


if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] not in ("clean", "score", "report"):
        sys.exit(__doc__)
    cmd = sys.argv[1]
    if cmd == "clean":
        cleaned, found = clean(_read(sys.argv[2]))
        sys.stdout.write(cleaned)
        sys.stderr.write(f"Hidden characters removed: {describe_found(found)}\n")
    elif cmd == "score":
        cleaned, found = clean(_read(sys.argv[2]))
        r = score(cleaned)
        print(f"AI-pattern score: {_score_line(r)}")
        print(f"Words: {r['words']}, sentences: {r['sentences']}")
        if r["score"] is not None:
            print(f"Pattern density: {r['density']} per 100 words, sentence-length variation: {r['sentence_cv']}, word variety: {r['mattr']}")
        for label, count, sample in sorted(r["patterns"], key=lambda h: -h[1]):
            print(f"  {label} x{count}, e.g. \"{sample[:60]}\"")
        print(f"Hidden characters found: {describe_found(found)}")
        skipped = _skipped_line(cleaned)
        if skipped:
            print(skipped)
    else:
        text, _ = report(_read(sys.argv[2]), _read(sys.argv[3]))
        print(text)
