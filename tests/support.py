"""Shared helpers for the titus-humanizer tests. Standard library only."""
import difflib
import importlib.util
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, "skills", "titus-humanizer", "scripts", "titus_tools.py")
FIXTURES = os.path.join(ROOT, "tests", "fixtures")
EXPECTED = os.path.join(ROOT, "tests", "expected")
REWRITE_SUFFIX = "_rewrite.txt"


def load_tools():
    """Import scripts/titus_tools.py as a module without installing anything."""
    spec = importlib.util.spec_from_file_location("titus_tools", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


tools = load_tools()


def run_cli(*args):
    """Run the script the way a user would and return its stdout and stderr."""
    proc = subprocess.run([sys.executable, SCRIPT, *args], capture_output=True, text=True,
                          encoding="utf-8", check=True)
    return proc.stdout, proc.stderr


def fixtures():
    """Every fixture as a path relative to tests/fixtures, sorted, for example 'resume/ai_resume.txt'."""
    found = []
    for folder, _, files in os.walk(FIXTURES):
        for name in files:
            if name.endswith(".txt"):
                found.append(os.path.relpath(os.path.join(folder, name), FIXTURES).replace(os.sep, "/"))
    return sorted(found)


def pairs():
    """(original, rewrite) fixture pairs, matched by the _rewrite.txt suffix."""
    names = set(fixtures())
    return [(n.replace(REWRITE_SUFFIX, ".txt"), n) for n in sorted(names)
            if n.endswith(REWRITE_SUFFIX) and n.replace(REWRITE_SUFFIX, ".txt") in names]


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def _blank_code(text):
    """Blank out code, quoted text, links and file paths the same way the scorer skips them, but keep every newline
    so line numbers stay right."""
    blank = lambda m: re.sub(r"[^\n]", " ", m.group(0))
    text = re.sub(r"`{3}.*?`{3}", blank, text, flags=re.S)
    text = re.sub(r"`[^`]*`", blank, text)
    for rx in (tools.BLOCK_QUOTE, tools.QUOTED):
        text = rx.sub(blank, text)
    return tools._blank_links_and_paths(text)


def quotations(text):
    """Every quotation the script finds, in reading order. Nested quotes come back inside their outer quote."""
    return tools.quotations(text)


def hits_by_line(text):
    """Every pattern hit as (line number, label, matched text), in reading order."""
    cleaned, _ = tools.clean(text)
    body = _blank_code(cleaned)
    hits = []
    for label, rx, _ in tools.COMPILED:
        keep = tools.FILTERS.get(label, lambda b, m: True)
        for m in rx.finditer(body):
            if keep(body, m):
                hits.append((body.count("\n", 0, m.start()) + 1, label, m.group(0).strip()))
    return sorted(hits)


def hard_rule_labels():
    """Labels of the Part 1 hard-rule patterns, which should never be left in a finished rewrite.

    Part 1 runs from the top of PATTERNS to "chatbot residue". The passive-voice pattern is left out
    because it is a heuristic: it also matches sentences that describe a state, which the skill allows.
    """
    labels = []
    for label, _, _ in tools.PATTERNS:
        if label != "passive voice (heuristic)":
            labels.append(label)
        if label == "chatbot residue":
            return labels
    raise AssertionError('PATTERNS no longer contains "chatbot residue"; update hard_rule_labels()')


def snapshot(name):
    """The text stored in tests/expected for one fixture: the CLI score output plus each hit with its line."""
    path = os.path.join(FIXTURES, name)
    out, _ = run_cli("score", path)
    lines = [f"# fixture: tests/fixtures/{name}", "", out.rstrip("\n"), "", "Hits by line:"]
    hits = hits_by_line(read(path))
    lines += [f"  line {n}: {label}: \"{sample[:60]}\"" for n, label, sample in hits] or ["  none"]
    return "\n".join(lines) + "\n"


def pair_snapshot(original, rewrite):
    """The text stored in tests/expected for a before-and-after pair: the CLI report output."""
    out, _ = run_cli("report", os.path.join(FIXTURES, original), os.path.join(FIXTURES, rewrite))
    return f"# before: tests/fixtures/{original}\n# after:  tests/fixtures/{rewrite}\n\n{out}"


def expected_path(name, kind):
    return os.path.join(EXPECTED, name.replace("/", "__").replace(".txt", f".{kind}.txt"))


def all_snapshots():
    """Every snapshot the suite checks, as {path in tests/expected: text}."""
    snaps = {expected_path(n, "score"): snapshot(n) for n in fixtures()}
    for original, rewrite in pairs():
        snaps[expected_path(original, "report")] = pair_snapshot(original, rewrite)
    return snaps


def diff(expected, actual, path):
    rel = os.path.relpath(path, ROOT)
    return "".join(difflib.unified_diff(expected.splitlines(True), actual.splitlines(True),
                                        fromfile=f"{rel} (stored)", tofile=f"{rel} (script now)"))
