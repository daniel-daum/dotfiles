#!/usr/bin/env python3
"""Build the colored icon sets and icon theme JSON files.

    python3 scripts/build.py
    python3 scripts/build.py --zed-theme ~/.config/zed/themes/flexoki-variants.json

The first form rebuilds everything from palettes.json. The second form first
refreshes the personal palettes in palettes.json from a Zed color theme file
(syntax colors -> icon roles), then rebuilds.

Each glyph in glyphs/ is a one-path Phosphor icon with fill="currentColor".
Each icon key gets one color role (ROLES below); each palette maps roles to
hex colors. Output: icons/<palette>/<key>.svg and icon_themes/*.json.
No dependencies beyond the Python standard library.
"""
import argparse, json, math, os, re, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------- mappings
# key: (glyph, role, suffixes, stems). Suffixes and stems are matched by Zed:
# a full filename is tried first (stems, then suffixes), then each part after a dot.
ICONS = {
    # languages
    "typescript": ("typescript", "blue",    "ts mts cts", ""),
    "javascript": ("javascript", "yellow",  "js mjs cjs", ""),
    "react":      ("react",      "cyan",    "jsx tsx", ""),
    "vue":        ("vue",        "green",   "vue", ""),
    "python":     ("python",     "blue",    "py pyi pyw", ""),
    "go":         ("go",         "cyan",    "go", ""),
    "rust":       ("rust",       "orange",  "rs", ""),
    "ruby":       ("ruby",       "red",     "rb rake", "Gemfile Rakefile"),
    "php":        ("php",        "purple",  "php", ""),
    "java":       ("java",       "red",     "java", ""),
    "c":          ("c",          "blue",    "c h", ""),
    "cpp":        ("cpp",        "blue",    "cpp cc cxx hpp hh", ""),
    "csharp":     ("csharp",     "purple",  "cs", ""),
    "swift":      ("swift",      "orange",  "swift", ""),
    # languages with no Phosphor glyph share the generic code glyph, each in its own color
    "kotlin":     ("code",       "purple",  "kt kts", ""),
    "dart":       ("code",       "cyan",    "dart", ""),
    "elixir":     ("code",       "purple",  "ex exs", ""),
    "scala":      ("code",       "red",     "scala", ""),
    "lua":        ("code",       "blue",    "lua", ""),
    "zig":        ("code",       "orange",  "zig", ""),
    "haskell":    ("code",       "purple",  "hs", ""),
    "clojure":    ("code",       "green",   "clj cljs", ""),
    "perl":       ("code",       "blue",    "pl pm", ""),
    "r":          ("code",       "blue",    "r", ""),
    "solidity":   ("code",       "neutral", "sol", ""),
    "nix":        ("code",       "blue",    "nix", ""),
    "elm":        ("code",       "cyan",    "elm", ""),
    "julia":      ("code",       "purple",  "jl", ""),
    "groovy":     ("code",       "blue",    "groovy", ""),
    "svelte":     ("code",       "orange",  "svelte", ""),
    "astro":      ("code",       "purple",  "astro", ""),
    "graphql":    ("code",       "magenta", "graphql gql", ""),
    "terraform":  ("code",       "purple",  "tf tfvars", ""),
    "prisma":     ("code",       "cyan",    "prisma", ""),
    "docker":     ("code",       "blue",    "", "Dockerfile"),
    "make":       ("code",       "orange",  "", "Makefile"),
    "cmake":      ("code",       "green",   "", "CMakeLists.txt"),
    # web and markup
    "html":       ("html",       "orange",  "html htm", ""),
    "css":        ("css",        "blue",    "css", ""),
    "sass":       ("sass",       "magenta", "scss sass less styl", ""),
    "xml":        ("xml",        "orange",  "xml xsd xsl xslt plist", ""),
    "svg":        ("svg",        "orange",  "svg", ""),
    "markdown":   ("markdown",   "purple",  "md mdx markdown", ""),
    # data and config
    "json":       ("json",       "yellow",  "json jsonc", ""),
    "document":   ("document",   "magenta", "yaml yml", ""),
    "toml":       ("toml",       "neutral", "toml", ""),
    "ini":        ("ini",        "neutral", "ini cfg conf editorconfig", ""),
    "env":        ("env",        "yellow",  "env", ""),
    "csv":        ("csv",        "green",   "csv", ""),
    "database":   ("database",   "yellow",  "db sqlite sqlite3", ""),
    "sql":        ("sql",        "yellow",  "sql", ""),
    "lock":       ("lock",       "neutral", "lock lockb pem key crt cert pub", ""),
    # tools
    "git":        ("git",        "red",     "gitignore gitcommit gitconfig gitrebase gitattributes git diff patch", ""),
    "shell":      ("shell",      "green",   "sh bash zsh fish ksh ps1 bat cmd", ""),
    "license":    ("license",    "yellow",  "", "LICENSE"),
    # documents and media
    "text":       ("text",       "neutral", "txt text log", ""),
    "pdf":        ("pdf",        "red",     "pdf", ""),
    "word":       ("word",       "blue",    "doc docx rtf", ""),
    "excel":      ("excel",      "green",   "xls xlsx", ""),
    "powerpoint": ("powerpoint", "orange",  "ppt pptx", ""),
    "image":      ("image",      "cyan",    "png jpg jpeg gif webp bmp ico tiff", ""),
    "audio":      ("audio",      "magenta", "mp3 wav flac aac ogg m4a", ""),
    "video":      ("video",      "magenta", "mp4 mov webm mkv avi", ""),
    "font":       ("font",       "red",     "ttf otf woff woff2 eot", ""),
    "zip":        ("zip",        "neutral", "zip tar gz tgz rar 7z bz2 xz zst", ""),
    # fallback
    "default":    ("document",   "neutral", "", ""),
}
# Zed merges its built-in file mappings into every icon theme (theme/src/registry.rs),
# so files like .zshrc, Procfile or .prettierrc resolve to built-in keys. Any key the
# theme doesn't define falls back to Zed's own gray icon, so define all of them here.
# key: (glyph, role). The suffixes come from Zed itself.
BUILTIN = {
    "backup": ("text", "neutral"),      "ballerina": ("code", "cyan"),     "bicep": ("code", "blue"),
    "bun": ("lock", "neutral"),         "cairo": ("code", "orange"),       "code": ("code", "neutral"),
    "coffeescript": ("code", "orange"), "crystal": ("code", "neutral"),    "csproj": ("code", "purple"),
    "cue": ("code", "blue"),            "diff": ("git", "red"),            "editorconfig": ("ini", "neutral"),
    "erlang": ("code", "red"),          "eslint": ("ini", "purple"),       "fsharp": ("code", "cyan"),
    "fsproj": ("code", "cyan"),         "gitlab": ("git", "orange"),       "gleam": ("code", "magenta"),
    "hcl": ("code", "purple"),          "helm": ("document", "blue"),      "heroku": ("code", "purple"),
    "ipynb": ("code", "orange"),        "kdl": ("document", "yellow"),     "log": ("text", "neutral"),
    "luau": ("code", "blue"),           "metal": ("code", "neutral"),      "nim": ("code", "yellow"),
    "ocaml": ("code", "orange"),        "odin": ("code", "blue"),          "prettier": ("ini", "cyan"),
    "puppet": ("code", "yellow"),       "roc": ("code", "purple"),         "settings": ("ini", "neutral"),
    "storage": ("database", "yellow"),  "stylelint": ("ini", "neutral"),   "surrealql": ("database", "magenta"),
    "tcl": ("code", "blue"),            "template": ("code", "orange"),    "terminal": ("shell", "green"),
    "v": ("code", "blue"),              "vbproj": ("code", "blue"),        "vcs": ("git", "red"),
    "vs_sln": ("code", "purple"),       "vs_suo": ("code", "purple"),      "vyper": ("code", "neutral"),
    "wgsl": ("code", "blue"),           "yaml": ("document", "magenta"),
}
# tree icons: (glyph, role)
TREE = {
    "folder-closed": ("folder-closed", "folder"),
    "folder-open":   ("folder-open",   "folder"),
    "caret-right":   ("caret-right",   "chevron"),
    "caret-down":    ("caret-down",    "chevron"),
}

# icon theme files: file name -> (family name, [(palette id, theme name, appearance)])
FAMILIES = {
    "phosphor-colored.json": ("Phosphor Colored Icons", [
        ("dark",  "Phosphor Colored Dark",  "dark"),
        ("light", "Phosphor Colored Light", "light"),
    ]),
    "phosphor-colored-flexoki-variants.json": ("Phosphor Colored Icons: Flexoki Variants", [
        ("moss",    "Phosphor Colored Moss",    "dark"),
        ("ink",     "Phosphor Colored Ink",     "dark"),
        ("wine",    "Phosphor Colored Wine",    "dark"),
        ("plum",    "Phosphor Colored Plum",    "dark"),
        ("teal",    "Phosphor Colored Teal",    "dark"),
        ("flexoki", "Phosphor Colored Flexoki", "dark"),
    ]),
}
AUTHOR = "Daniel Daum (fork of Phosphor Icons Theme by Theo Luciano)"
SCHEMA = "https://zed.dev/schema/icon_themes/v0.3.0.json"

# ---------------------------------------------------------------- color math (OKLab / OKLCH)
def _lin(c): return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
def _gam(c): return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055

def hex_rgb(h):
    h = h.lstrip("#")[:6]
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))

def rgb_hex(rgb): return "#" + "".join(f"{round(max(0, min(1, c)) * 255):02x}" for c in rgb)

def rgb_oklab(rgb):
    r, g, b = map(_lin, rgb)
    l = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    m = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    s = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    return (0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
            1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
            0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s)

def oklab_rgb(lab):
    L, a, b = lab
    l = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    return tuple(map(_gam, (4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
                            -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
                            -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s)))

def in_gamut(rgb): return all(-1e-4 <= c <= 1 + 1e-4 for c in rgb)

def oklch_hex(L, C, H):
    """OKLCH -> hex, reducing chroma until the color fits in sRGB."""
    while True:
        rgb = oklab_rgb((L, C * math.cos(math.radians(H)), C * math.sin(math.radians(H))))
        if in_gamut(rgb) or C <= 0: return rgb_hex(rgb)
        C -= 0.002

def hex_oklch(h):
    L, a, b = rgb_oklab(hex_rgb(h))
    return L, math.hypot(a, b), math.degrees(math.atan2(b, a)) % 360

def luminance(h):
    r, g, b = map(_lin, hex_rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)

# ---------------------------------------------------------------- personal palettes from a Zed theme
VARIANTS = ["Moss", "Ink", "Wine", "Plum", "Teal", "Flexoki"]
FLEXOKI_MAGENTA = ("#F4A4C2", "#E47DA8")  # Flexoki magenta 200 and 300

def palette_from_zed_theme(style):
    syn = lambda k: style["syntax"][k]["color"][:7]
    return {
        "red": syn("variable"), "orange": syn("number"), "yellow": syn("type"),
        "green": syn("string"), "cyan": syn("string.escape"), "blue": syn("function"),
        "purple": syn("keyword"), "neutral": style["text.muted"][:7],
        "folder": style["text.muted"][:7], "chevron": syn("comment"),
        "_bg": style["panel.background"][:7],
    }

def add_magenta(pals):
    """The Zed theme has no magenta role. Build one from Flexoki magenta, set to the
    average lightness of the other syntax colors, then shift it by the same average
    OKLab offset that each variant applies to the untinted Flexoki variant."""
    hues = ["red", "orange", "yellow", "green", "cyan", "blue", "purple"]
    ref = pals["flexoki"]
    target_L = sum(hex_oklch(ref[h])[0] for h in hues) / len(hues)
    a, b = (rgb_oklab(hex_rgb(c)) for c in FLEXOKI_MAGENTA)
    t = max(0, min(1, (a[0] - target_L) / (a[0] - b[0])))
    base = tuple(a[i] + (b[i] - a[i]) * t for i in range(3))
    for name, p in pals.items():
        off = [sum(rgb_oklab(hex_rgb(p[h]))[i] - rgb_oklab(hex_rgb(ref[h]))[i] for h in hues) / len(hues)
               for i in range(3)]
        p["magenta"] = rgb_hex(oklab_rgb(tuple(base[i] + off[i] for i in range(3))))

def refresh_personal(theme_path, pal_path):
    d = json.load(open(os.path.expanduser(theme_path)))
    by_name = {t["name"]: t["style"] for t in d["themes"]}
    pals = json.load(open(pal_path))
    personal = {v.lower(): palette_from_zed_theme(by_name[v]) for v in VARIANTS}
    add_magenta(personal)
    for k, p in personal.items():
        p["_note"] = f"from Zed theme '{VARIANTS[[v.lower() for v in VARIANTS].index(k)]}' in {os.path.basename(theme_path)}"
        pals[k] = p
    json.dump(pals, open(pal_path, "w"), indent=2)
    print("refreshed personal palettes from", theme_path)

# ---------------------------------------------------------------- build
def build():
    pals = json.load(open(os.path.join(ROOT, "palettes.json")))
    glyphs = {f[:-4]: open(os.path.join(ROOT, "glyphs", f)).read()
              for f in os.listdir(os.path.join(ROOT, "glyphs")) if f.endswith(".svg")}
    out_icons = os.path.join(ROOT, "icons")
    shutil.rmtree(out_icons, ignore_errors=True)

    def write(pal_id, name, glyph, role):
        color = pals[pal_id][role]
        svg = glyphs[glyph].replace('fill="currentColor"', f'fill="{color}"')
        assert f'fill="{color}"' in svg, (glyph, "has no currentColor fill")
        d = os.path.join(out_icons, pal_id)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, name + ".svg"), "w").write(svg)
        return f"./icons/{pal_id}/{name}.svg"

    for fname, (family, themes) in FAMILIES.items():
        out = []
        for pal_id, tname, appearance in themes:
            suffixes, stems, file_icons = {}, {}, {}
            for key, (glyph, role, sfx, stm) in ICONS.items():
                file_icons[key] = {"path": write(pal_id, key, glyph, role)}
                for s in sfx.split(): suffixes[s] = key
                for s in stm.split(): stems[s] = key
            for key, (glyph, role) in BUILTIN.items():
                file_icons.setdefault(key, {"path": write(pal_id, key, glyph, role)})
            tree = {k: write(pal_id, k, g, r) for k, (g, r) in TREE.items()}
            out.append({
                "name": tname, "appearance": appearance,
                "directory_icons": {"collapsed": tree["folder-closed"], "expanded": tree["folder-open"]},
                "chevron_icons": {"collapsed": tree["caret-right"], "expanded": tree["caret-down"]},
                "file_stems": stems, "file_suffixes": suffixes, "file_icons": file_icons,
            })
        doc = {"$schema": SCHEMA, "name": family, "author": AUTHOR, "themes": out}
        json.dump(doc, open(os.path.join(ROOT, "icon_themes", fname), "w"), indent=2)
        print(f"wrote icon_themes/{fname}: {', '.join(t['name'] for t in out)}")

def report():
    """Contrast of every role against each palette's panel background(s)."""
    pals = json.load(open(os.path.join(ROOT, "palettes.json")))
    roles = ["red", "orange", "yellow", "green", "cyan", "blue", "purple", "magenta", "neutral", "folder", "chevron"]
    for pid, p in pals.items():
        bgs = p["_bg"] if isinstance(p["_bg"], list) else [p["_bg"]]
        for bg in bgs:
            cs = {r: contrast(p[r], bg) for r in roles}
            Ls = {r: hex_oklch(p[r])[0] for r in roles}
            print(f"{pid:<8} on {bg}: min {min(cs.values()):.2f} ({min(cs, key=cs.get)})  "
                  + " ".join(f"{r[:3]}={cs[r]:.1f}" for r in roles))

def check():
    """Fail on: a suffix/stem pointing at a missing key, a path with no file,
    a dead key (nothing maps to it), or an SVG on disk that no theme uses."""
    used, ok = set(), True
    for fname in FAMILIES:
        for t in json.load(open(os.path.join(ROOT, "icon_themes", fname)))["themes"]:
            fi = t["file_icons"]; refs = set(t["file_suffixes"].values()) | set(t["file_stems"].values())
            paths = [v["path"] for v in fi.values()] + [t[b][s] for b in ("directory_icons", "chevron_icons")
                                                        for s in ("collapsed", "expanded")]
            problems = {
                "missing keys": sorted(refs - set(fi)),
                "missing files": [p for p in paths if not os.path.exists(os.path.join(ROOT, p[2:]))],
                "dead keys": sorted(set(fi) - refs - set(BUILTIN) - {"default"}),
            }
            for k, v in problems.items():
                if v: ok = False; print(f"{t['name']}: {k}: {v}")
            used |= {p[2:] for p in paths}
    on_disk = {os.path.relpath(os.path.join(dp, f), ROOT) for dp, _, fs in os.walk(os.path.join(ROOT, "icons"))
               for f in fs if f.endswith(".svg")}
    if on_disk - used: ok = False; print("orphaned svgs:", sorted(on_disk - used))
    print("check:", "OK" if ok else "FAILED"); return ok

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--zed-theme", help="refresh personal palettes from this Zed theme JSON first")
    ap.add_argument("--report", action="store_true", help="print contrast report and exit")
    a = ap.parse_args()
    if a.zed_theme: refresh_personal(a.zed_theme, os.path.join(ROOT, "palettes.json"))
    if a.report: report(); sys.exit()
    build()
    sys.exit(0 if check() else 1)
