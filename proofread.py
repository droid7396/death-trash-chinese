"""按术语表校对全部已翻译文的一致性"""
import json, os, re

WORK = r"C:\Games\Death Trash\_localization"
TRANS = os.path.join(WORK, "translations")

# 术语 -> 唯一译名;检查译文中是否出现错误变体
checks = [
    # (正则, 说明)
    (r"赛博子宫|机械子宫", "Cyberwomb 应为:义体子宫"),
    (r"全子宫|万物胎", "Omniwomb 应为:万物子宫"),
    (r"血肉之网|血肉网络|肉之枢纽", "Flesh Nexus 应为:血肉枢纽"),
    (r"蠕洞|虫伤|蠕虫之伤", "Wormwound 应为:蠕伤"),
    (r"摩罗肉|莫罗肉|毛罗肉", "Morrowmeat 应为:摩罗肉铺(检查变体)"),
    (r"吞噬者|吞噬体|食者(?!希布)", "Feeder 应为:吞食者(检查变体)"),
    (r"记忆印痕|印刻", "engram/imprint 应为:核心印记/记忆印痕检查"),
    (r"阿克沙|阿克撒", "Aksa 应为:阿克萨"),
    (r"海夫拉|黑芙拉", "Hevla 应为:海芙拉"),
    (r"塞内斯查|总管大人(需检查语境)", "Seneschal 应为:总管"),
    (r"圣主(?!之塔)", "Hierarch 圣主 OK"),
    (r"屠夫切割|屠夫之切", "Butcher's Cut 应为:「屠夫切肉」"),
    (r"甜眼(?!睛)", "Eyelicious 应为:甜眼睛"),
    (r"血肉克拉肯|克拉肯海妖", "Fleshkraken 应为:血肉海妖"),
    (r"陶里(?!斯)", "Tauris 应为:陶里斯"),
    (r"水泡井|沸腾井|起泡井", "Blistering Wells 应为:沸泡井"),
    (r"机器之神(?!的)", "Machine God OK"),
    (r"米尔贾|米利亚|米尔加", "Millja 应为:米爾娅(检查)"),
    (r"加瓦(?!斯)", "Gavas 应为:加瓦斯"),
    (r"玛尔加斯(?!女王)", "Queen Margas OK"),
    (r"海妖神庙", "Fleshkraken 神庙地点名检查"),
    (r"普罗塔(?!斯)", "Protas 应为:普罗塔斯"),
    (r"卡斯特(?!罗)", "Custer OK"),
    (r"埃尔德雷|艾尔德雷", "Eldred 应为:埃尔德雷德"),
    (r"诺瓦|努尔", "Noor 应为:诺尔"),
    (r"莱娜得拉|列娜德拉", "Lenadra 应为:莱娜德拉"),
]

issues = {}
total = 0
for fn in sorted(os.listdir(TRANS)):
    if not fn.endswith(".json"):
        continue
    items = json.load(open(os.path.join(TRANS, fn), encoding="utf-8"))
    for it in items:
        total += 1
        dst = it["dst"]
        for pat, desc in checks:
            for m in re.finditer(pat, dst):
                # 过滤已知合法匹配
                s = m.group(0)
                if s == "吞食者" or s == "圣主" or s == "机器之神" or s == "玛尔加斯女王" or s == "摩罗肉铺":
                    continue
                key = (pat, desc)
                issues.setdefault(key, []).append((fn, it["si"], it["ei"], dst[:60]))

print(f"scanned entries: {total}")
if not issues:
    print("ALL CONSISTENT")
for (pat, desc), lst in issues.items():
    print(f"\n[{desc}] pattern={pat} -> {len(lst)} hits")
    for fn, si, ei, prev in lst[:6]:
        print(f"   {fn} si={si} ei={ei}: {prev}")
