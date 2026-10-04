"""字体分析:渲染模式、内嵌 ttf、字形覆盖"""
import UnityPy, os

DATA = r"C:\Games\Death Trash\DeathTrash_Data"
OUT = r"C:\Games\Death Trash\_localization\extracted"

def font_info(path, label):
    env = UnityPy.load(path)
    for obj in env.objects:
        if obj.type.name != "Font":
            continue
        try:
            d = obj.read()
        except Exception as e:
            print(label, obj.path_id, "read err", e)
            continue
        fd = getattr(d, "m_FontData", None)
        if isinstance(fd, list):
            fd = bytes(fd)
        size = len(fd) if fd else 0
        names = getattr(d, "m_FontNames", None)
        chars = getattr(d, "m_CharacterRects", None)
        nrects = len(chars) if chars is not None else "?"
        print(f"{label}: {d.m_Name} render={getattr(d, 'm_FontRenderingMode', '?')} "
              f"names={names} ttfbytes={size} charRects={nrects}")
        if fd and size > 1000:
            with open(os.path.join(OUT, f"font_{d.m_Name}.ttf"), "wb") as f:
                f.write(fd)

font_info(os.path.join(DATA, "resources.assets"), "resources")
font_info(os.path.join(DATA, "sharedassets1.assets"), "shared1")
font_info(os.path.join(DATA, "sharedassets0.assets"), "shared0")
