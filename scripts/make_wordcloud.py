#!/usr/bin/env python3
"""Draws the Research page word cloud as a static SVG.

Each topic's size is the number of publication titles in
_publications/index.html that match its pattern. Rerun after adding papers:

  python3 scripts/make_wordcloud.py   # writes images/research-wordcloud.svg
"""
import html
import math
import re

PAGE = "_publications/index.html"
OUT = "images/research-wordcloud.svg"

# (topic, regex over titles). A title can count toward several topics.
TOPICS = [
    ("Static Analysis", r"static|soundy|pointer|taint|codeql"),
    ("Fuzzing", r"fuzz"),
    ("Embedded Systems", r"embedded|firmware|iot|peripheral|rehost|smart devices|cyber-physical"),
    ("Android", r"android|\bapps?\b|mobile"),
    ("Vulnerability Detection", r"vulnerab|\bbugs?\b|defects?|misuse|detect"),
    ("Memory Safety", r"memory safety|checked c|\b3c\b|spatial"),
    ("Rust", r"\brust\b"),
    ("UEFI & Bootloaders", r"uefi|edk|tianocore|bootloader|bootstomp"),
    ("Binary Analysis", r"binar|reassembl|ramblr|debloat"),
    ("Linux Kernel", r"kernel|drivers?\b"),
    ("Trusted Execution", r"trusted|trustzone|\btee\b|confidential"),
    ("Isolation & Partitioning", r"partition|isolat|sandbox|virtualization"),
    ("Software Supply Chain", r"supply chain|dependenc|repositor"),
    ("CI/CD Security", r"github|workflow|actions"),
    ("Machine Learning", r"learning|neural|generative|language model|\bai\b"),
    ("Formal Verification", r"verif|proofs?\b|model checking"),
    ("Patch Analysis", r"patch"),
    ("Hardware Security", r"glitch|hardware|accelerator"),
    ("Empirical Studies", r"empirical|experience|insights|study"),
    ("Type Systems", r"\btype"),
    ("Autonomous Hacking", r"hacking|phish"),
    ("Privacy", r"privacy"),
    ("Distributed Systems", r"distributed|crowdsourced"),
    ("Program Testing", r"testing|test |input generation|mutation"),
]

COLORS = ["#2a6f86", "#52adc8", "#494e52", "#8a6d2f"]
FONT = '-apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
WIDTH, HEIGHT = 900, 340
MIN_SIZE, MAX_SIZE = 13, 40


def text_width(text, size):
    """Rough width of bold sans-serif text; errs wide so words never overlap."""
    em = 0.0
    for ch in text:
        if ch in "iljI.,'|!:; ":
            em += 0.32
        elif ch in "mwMW":
            em += 0.92
        elif ch.isupper() or ch in "&/":
            em += 0.72
        else:
            em += 0.6
    return em * size


def main():
    page = open(PAGE, encoding="utf-8").read()
    titles = [html.unescape(re.sub(r"<[^>]+>", "", t)).lower()
              for t in re.findall(r"<strong>(.*?)</strong>", page, re.S)]
    counts = [(name, sum(bool(re.search(rx, t)) for t in titles)) for name, rx in TOPICS]
    counts = sorted([c for c in counts if c[1] > 0], key=lambda c: -c[1])
    top = counts[0][1]

    placed = []  # (x, y, w, h) boxes, centered coordinates
    words = []
    for i, (name, n) in enumerate(counts):
        size = MIN_SIZE + (MAX_SIZE - MIN_SIZE) * math.sqrt((n - 1) / max(top - 1, 1))
        w, h = text_width(name, size) + 10, size * 1.15
        # Walk an elliptical spiral out from the center until the word fits.
        for step in range(4000):
            t = step * 0.12
            x = WIDTH / 2 + 2.2 * t * math.cos(t)
            y = HEIGHT / 2 + 0.9 * t * math.sin(t)
            if not (w / 2 <= x <= WIDTH - w / 2 and h / 2 <= y <= HEIGHT - h / 2):
                continue
            if all(abs(x - px) * 2 >= w + pw or abs(y - py) * 2 >= h + ph for px, py, pw, ph in placed):
                placed.append((x, y, w, h))
                words.append((name, n, x, y, size, COLORS[i % len(COLORS)]))
                break
        else:
            print(f"no room for {name!r}; skipped")

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" '
           f'role="img" aria-labelledby="title">',
           '<title id="title">Research topics, sized by number of publications: ' +
           html.escape(", ".join(f"{n} ({c})" for n, c, *_ in words)) + "</title>",
           f'<g font-family=\'{FONT}\' font-weight="700" text-anchor="middle">']
    for name, n, x, y, size, color in words:
        out.append(f'<text x="{x:.0f}" y="{y + 0.35 * size:.0f}" font-size="{size:.0f}" fill="{color}">'
                   f'{html.escape(name)}</text>')
    out += ["</g>", "</svg>", ""]
    open(OUT, "w", encoding="utf-8").write("\n".join(out))
    print(f"wrote {OUT}: " + ", ".join(f"{n} ({c})" for n, c, *_ in words))


if __name__ == "__main__":
    main()
