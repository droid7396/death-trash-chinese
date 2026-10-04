"""按 (si, ei) 精确回写译文,生成官方三列 TSV。
build_mod3.py 以 (type, name, id) 匹配,但 UI 段与 SEQUENCE 段的数字 id 大量重复,
导致译文被覆盖丢失;本脚本复刻 prepare_batches.parse 的状态机,
重建 每行 -> (si, ei) 映射后精确替换。
"""
import re, json, os

WORK = r"C:\Games\Death Trash\_localization"
SRC = os.path.expandvars(r"%USERPROFILE%\AppData\LocalLow\Crafting Legends\Death Trash\Mods\LanguageData\newLanguage.tsv")
MOD_DIR = os.path.expandvars(r"%USERPROFILE%\AppData\LocalLow\Crafting Legends\Death Trash\Mods\ChineseLanguageMod")
os.makedirs(MOD_DIR, exist_ok=True)

struct = json.load(open(os.path.join(WORK, "structure.json"), encoding="utf-8"))["sections"]

trans = {}
for fn in sorted(os.listdir(os.path.join(WORK, "translations"))):
    if fn.endswith(".json"):
        for item in json.load(open(os.path.join(WORK, "translations", fn), encoding="utf-8")):
            trans[(item["si"], item["ei"])] = item["dst"]
print("translations:", len(trans))

lines = open(SRC, encoding="utf-8").read().split("\n")

mapping = {}
si = -1
ei = 0
in_ui = False
for li in range(4, len(lines)):
    l = lines[li].rstrip("\r")
    if not l.strip() or l.startswith("---"):
        continue
    if re.match(r"^SEQUENCE (.+)$", l):
        si += 1
        in_ui = False
        continue
    m = re.match(r"^#([^:]+):\t(.*)$", l)
    if m:
        if not in_ui:
            si += 1
            ei = 0
            in_ui = True
        mapping[li] = (si, ei, m.group(1))
        ei += 1

assert si == len(struct) - 1, (si, len(struct))
bad = sum(1 for li, (s, e, k) in mapping.items()
          if struct[s]["entries"][e]["src"] != lines[li].rstrip("\r").split("\t")[1])
print("sections matched:", si + 1, "entries:", len(mapping), "src mismatch:", bad)

out = []
replaced = 0
for li, raw in enumerate(lines):
    line = raw.rstrip("\r")
    if li < 4:
        if line.startswith("Death Trash Language File"):
            out.append("Death Trash Language File\t\t")
        elif line.startswith("File Format Version:"):
            out.append("File Format Version:\t1\t")
        elif line.startswith("Language Id:"):
            out.append("Language Id:\tChinese\t简体中文")
        else:
            out.append(line)
        continue
    if li in mapping:
        s, e, key = mapping[li]
        english = line.split("\t")[1]
        dst = trans.get((s, e), "")
        out.append(f"#{key}:\t{english}\t{dst}")
        if dst:
            replaced += 1
        continue
    if line.startswith("---"):
        out.append(line + "\t\t")
        continue
    if line.startswith("ASSET"):
        out.append(line + "\t")
        continue
    out.append(line)

print("translated entries:", replaced)
target = os.path.join(MOD_DIR, "chinese.tsv")
with open(target, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(out))
print("wrote", target)
