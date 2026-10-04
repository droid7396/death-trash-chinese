"""解析语言 TSV,生成分批翻译任务 + 合并译文回写"""
import re, json, os, sys

LANG_DIR = os.path.expandvars(r"%USERPROFILE%\AppData\LocalLow\Crafting Legends\Death Trash\Mods\LanguageData")
WORK = r"C:\Games\Death Trash\_localization"
SRC = os.path.join(LANG_DIR, "newLanguage.tsv")
BATCH_DIR = os.path.join(WORK, "batches")
TRANS_DIR = os.path.join(WORK, "translations")
os.makedirs(BATCH_DIR, exist_ok=True)
os.makedirs(TRANS_DIR, exist_ok=True)

def parse(path):
    """返回 sections: [{type: ui|seq, name, entries: [{id, src, dst}]}]"""
    raw = open(path, encoding="utf-8").read()
    lines = raw.split("\n")
    header = lines[:4]
    sections = []
    cur = None
    for l in lines[4:]:
        l = l.rstrip("\r")
        if not l.strip():
            continue
        if l.startswith("------------------------------------------"):
            continue
        m = re.match(r"^SEQUENCE (.+)$", l)
        if m:
            cur = {"type": "seq", "name": m.group(1), "entries": []}
            sections.append(cur)
            continue
        m = re.match(r"^#([^:]+):\t(.*)$", l)
        if m:
            if cur is None or cur["type"] != "ui":
                cur = {"type": "ui", "name": "UI", "entries": []}
                sections.append(cur)
            cur["entries"].append({"id": m.group(1), "src": m.group(2), "dst": ""})
            continue
        # 未匹配行(不应发生)
        print("UNPARSED:", repr(l[:80]))
    return header, sections

def needs_translation(s):
    if not s.strip():
        return False
    if re.fullmatch(r"[\s\.\-…!?\d\{\}\[\]%+/|]*", s):
        return False
    if not re.search(r"[A-Za-z]", s):
        return False
    return True

def flatten(sections):
    items = []
    for si, sec in enumerate(sections):
        for ei, e in enumerate(sec["entries"]):
            if needs_translation(e["src"]):
                items.append((si, ei, e["src"]))
    return items

def make_batches(items, size=450):
    batches = []
    cur = []
    cur_len = 0
    for si, ei, src in items:
        est = max(len(src), 8)
        if cur and cur_len + est > 9500 or len(cur) >= size:
            batches.append(cur)
            cur = []
            cur_len = 0
        cur.append((si, ei, src))
        cur_len += est
    if cur:
        batches.append(cur)
    return batches

def main():
    header, sections = parse(SRC)
    total = sum(len(s["entries"]) for s in sections)
    items = flatten(sections)
    print(f"sections: {len(sections)}, entries: {total}, to translate: {len(items)}")
    batches = make_batches(items)
    print(f"batches: {len(batches)}")
    for i, b in enumerate(batches):
        payload = [{"si": si, "ei": ei, "src": src} for si, ei, src in b]
        with open(os.path.join(BATCH_DIR, f"batch_{i:03d}.json"), "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=0)
    # 保存结构供合并
    with open(os.path.join(WORK, "structure.json"), "w", encoding="utf-8") as f:
        json.dump({"header": header, "sections": sections}, f, ensure_ascii=False)
    chars = sum(len(src) for _, _, src in items)
    print(f"total chars to translate: {chars}")

if __name__ == "__main__":
    main()
