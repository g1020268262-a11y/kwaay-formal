from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "figures"
OUT.mkdir(parents=True, exist_ok=True)

FONT_CJK = Path(r"C:\Windows\Fonts\msyh.ttc")
FONT_CJK_B = Path(r"C:\Windows\Fonts\msyhbd.ttc")
FONT_LATIN = Path(r"C:\Windows\Fonts\times.ttf")
FONT_LATIN_B = Path(r"C:\Windows\Fonts\timesbd.ttf")


def font(size, bold=False, latin=False):
    p = FONT_LATIN_B if latin and bold else FONT_LATIN if latin else FONT_CJK_B if bold else FONT_CJK
    return ImageFont.truetype(str(p), size)


def center_text(draw, xy, text, fnt, fill="#111111"):
    box = draw.textbbox((0, 0), text, font=fnt)
    w = box[2] - box[0]
    h = box[3] - box[1]
    draw.text((xy[0] - w / 2, xy[1] - h / 2), text, font=fnt, fill=fill)


def arrow(draw, start, end, fill="#222222", width=4, dash=False):
    x1, y1 = start
    x2, y2 = end
    if dash:
        seg = 15
        gap = 9
        length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        ux, uy = (x2 - x1) / length, (y2 - y1) / length
        pos = 0
        while pos < length - 15:
            a = pos
            b = min(pos + seg, length - 15)
            draw.line((x1 + ux * a, y1 + uy * a, x1 + ux * b, y1 + uy * b), fill=fill, width=width)
            pos += seg + gap
    else:
        draw.line((x1, y1, x2, y2), fill=fill, width=width)
    import math
    ang = math.atan2(y2 - y1, x2 - x1)
    for delta in (2.55, -2.55):
        draw.line((x2, y2, x2 + 18 * math.cos(ang + delta), y2 + 18 * math.sin(ang + delta)), fill=fill, width=width)


def svg_header(w, h):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'


def svg_text(x, y, text, size=24, anchor="middle", weight="normal", family="Microsoft YaHei"):
    return (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" '
        f'font-family="{family}" font-size="{size}" font-weight="{weight}" fill="#111111">'
        f'{escape(text)}</text>'
    )


def svg_rect(x, y, w, h, fill="#f5f7f8", stroke="#333333", rx=12, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="3"{d}/>'


def svg_arrow(x1, y1, x2, y2, dash=False):
    d = ' stroke-dasharray="12 8"' if dash else ""
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#222222" stroke-width="4" '
        f'marker-end="url(#arrow)"{d}/>'
    )


def make_figure1():
    w, h = 1200, 1030
    img = Image.new("RGB", (w, h), "white")
    d = ImageDraw.Draw(img)
    f20, f22, f24, f28, f32 = font(20), font(22), font(24), font(28), font(32, True)
    d.text((55, 38), "K-Waay源接口（一次BatchReceive调用）", font=f32, fill="#111111")

    boxes = [(90, 120, 470, 260), (730, 120, 1110, 260)]
    labels = [
        ("位置 ℓ=1；参与方索引 j_1", "(pk_j1, prek_j1, m_j1)"),
        ("位置 ℓ=2；参与方索引 j_2", "(pk_j2, prek_j2, m_j2)"),
    ]
    for box, (a, b) in zip(boxes, labels):
        d.rounded_rectangle(box, radius=16, fill="#eef3f6", outline="#333333", width=4)
        center_text(d, ((box[0] + box[2]) / 2, box[1] + 52), a, f24)
        center_text(d, ((box[0] + box[2]) / 2, box[1] + 103), b, f24)
    d.rounded_rectangle((350, 330, 850, 480), radius=18, fill="#ffffff", outline="#111111", width=5)
    center_text(d, (600, 375), "BatchReceive(sk_i, st_i, S)", f28)
    center_text(d, (600, 425), "共享接收方状态；逐分量输出 k_j", f22)
    arrow(d, (280, 260), (470, 330))
    arrow(d, (920, 260), (730, 330))
    d.text((160, 505), "输出 k_j1", font=f24, fill="#111111")
    d.text((850, 505), "输出 k_j2", font=f24, fill="#111111")
    arrow(d, (470, 480), (280, 500))
    arrow(d, (730, 480), (920, 500))
    d.rounded_rectangle((155, 555, 1045, 625), radius=12, fill="#f2f2f2", outline="#555555", width=3)
    center_text(d, (600, 590), "j_1 ≠ j_2：原规范规定同一调用中的输入对应不同参与方", f24)

    arrow(d, (600, 625), (600, 715), dash=True)
    center_text(d, (600, 670), "分析投影（不表示已建立 refinement）", f22, "#333333")
    d.text((55, 720), "固定两槽接纳抽象", font=f32, fill="#111111")
    lower = [(90, 795, 520, 905), (680, 795, 1110, 905)]
    lower_labels = ["E_1=(A_1, oid_1, m_1)", "E_2=(A_2, oid_2, m_2)"]
    for box, lab in zip(lower, lower_labels):
        d.rounded_rectangle(box, radius=16, fill="#e9eef1", outline="#222222", width=4)
        center_text(d, ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2), lab, f28)
    d.rounded_rectangle((390, 940, 810, 1000), radius=14, fill="#ffffff", outline="#444444", width=3)
    center_text(d, (600, 970), "共享批次/接收方上下文 (bid, rst)", f22)
    arrow(d, (305, 905), (480, 940))
    arrow(d, (895, 905), (720, 940))
    img.save(OUT / "figure-1.png", dpi=(300, 300))

    s = [svg_header(w, h), '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#222222"/></marker></defs>']
    s += [svg_text(55, 70, "K-Waay源接口（一次BatchReceive调用）", 32, "start", "bold")]
    for box, (a, b) in zip(boxes, labels):
        x1, y1, x2, y2 = box
        s += [svg_rect(x1, y1, x2-x1, y2-y1, "#eef3f6"), svg_text((x1+x2)/2, y1+58, a, 24), svg_text((x1+x2)/2, y1+112, b, 24)]
    s += [svg_rect(350,330,500,150,"#ffffff","#111111",18), svg_text(600,385,"BatchReceive(sk_i, st_i, S)",28), svg_text(600,435,"共享接收方状态；逐分量输出 k_j",22)]
    s += [svg_arrow(280,260,470,330), svg_arrow(920,260,730,330), svg_arrow(470,480,280,500), svg_arrow(730,480,920,500)]
    s += [svg_text(160,530,"输出 k_j1",24,"start"), svg_text(850,530,"输出 k_j2",24,"start")]
    s += [svg_rect(155,555,890,70,"#f2f2f2","#555555",12), svg_text(600,600,"j_1 ≠ j_2：原规范规定同一调用中的输入对应不同参与方",24)]
    s += [svg_arrow(600,625,600,715,True), svg_text(600,682,"分析投影（不表示已建立 refinement）",22)]
    s += [svg_text(55,752,"固定两槽接纳抽象",32,"start","bold")]
    for box, lab in zip(lower, lower_labels):
        x1,y1,x2,y2=box
        s += [svg_rect(x1,y1,x2-x1,y2-y1,"#e9eef1","#222222",16), svg_text((x1+x2)/2,y1+70,lab,28)]
    s += [svg_rect(390,940,420,60,"#ffffff","#444444",14), svg_text(600,979,"共享批次/接收方上下文 (bid, rst)",22), svg_arrow(305,905,480,940), svg_arrow(895,905,720,940), "</svg>"]
    (OUT / "figure-1.svg").write_text("\n".join(s), encoding="utf-8")


def make_figure2():
    w, h = 1200, 1160
    img = Image.new("RGB", (w, h), "white")
    d = ImageDraw.Draw(img)
    f20, f22, f24, f28, f32 = font(20), font(22), font(24), font(28), font(32, True)
    d.text((55, 35), "同一精确来源在宽松接纳模型中的两次接受", font=f32, fill="#111111")
    d.rounded_rectangle((135, 105, 1065, 205), radius=16, fill="#eef3f6", outline="#222222", width=4)
    center_text(d, (600, 140), "SendMessage at s：Send(A, oid, m)", f28)
    center_text(d, (600, 180), "公开 E=(A, oid, m)；该精确三元组只有一个匹配 Send", f22)
    arrow(d, (600, 205), (600, 285))
    for x, title in [(100, "Slot 1 = E"), (690, "Slot 2 = E")]:
        d.rounded_rectangle((x, 285, x + 410, 390), radius=15, fill="#f7f7f7", outline="#333333", width=4)
        center_text(d, (x + 205, 335), title, f28)
    arrow(d, (600, 245), (305, 285))
    arrow(d, (600, 245), (895, 285))
    d.rounded_rectangle((250, 465, 950, 580), radius=16, fill="#ececec", outline="#111111", width=5)
    center_text(d, (600, 505), "AdmitRelaxedBatch at b", f28)
    center_text(d, (600, 548), "BatchReceive(bid, rst)；无 A/m 不等条件", f22)
    arrow(d, (305, 390), (500, 465))
    arrow(d, (895, 390), (700, 465))
    d.rounded_rectangle((120, 665, 1080, 760), radius=16, fill="#f5f5f5", outline="#333333", width=4)
    center_text(d, (600, 710), "ProcessSlot1 at r_1 → ReceiverAccept(A, oid, m, bid, rst)", f24)
    d.rounded_rectangle((120, 835, 1080, 930), radius=16, fill="#f5f5f5", outline="#333333", width=4)
    center_text(d, (600, 880), "ProcessSlot2 at r_2 → ReceiverAccept(A, oid, m, bid, rst)", f24)
    arrow(d, (600, 580), (600, 665))
    arrow(d, (600, 760), (600, 835))
    d.rounded_rectangle((100, 990, 1100, 1070), radius=14, fill="#ffffff", outline="#555555", width=3)
    center_text(d, (600, 1030), "同一 (bid, rst)，且 s < b < r_1 < r_2", f28)
    arrow(d, (600, 930), (600, 990))
    d.rounded_rectangle((20, 480, 220, 900), radius=15, fill="#ffffff", outline="#777777", width=3)
    center_text(d, (120, 520), "持久来源事实", f22)
    center_text(d, (120, 565), "!Sent(A,oid,m)", f22)
    d.line((220, 650, 360, 705), fill="#555555", width=4)
    d.line((220, 700, 360, 880), fill="#555555", width=4)
    d.text((30, 1100), "虚线/侧线表示两个处理规则读取同一持久来源事实，不表示发生第二次发送。", font=f20, fill="#333333")
    img.save(OUT / "figure-2.png", dpi=(300, 300))

    s = [svg_header(w,h), '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#222222"/></marker></defs>']
    s += [svg_text(55,70,"同一精确来源在宽松接纳模型中的两次接受",32,"start","bold")]
    s += [svg_rect(135,105,930,100,"#eef3f6","#222222",16), svg_text(600,150,"SendMessage at s：Send(A, oid, m)",28), svg_text(600,190,"公开 E=(A, oid, m)；该精确三元组只有一个匹配 Send",22)]
    s += [svg_arrow(600,205,600,285), svg_rect(100,285,410,105,"#f7f7f7"), svg_rect(690,285,410,105,"#f7f7f7"), svg_text(305,350,"Slot 1 = E",28), svg_text(895,350,"Slot 2 = E",28), svg_arrow(600,245,305,285), svg_arrow(600,245,895,285)]
    s += [svg_rect(250,465,700,115,"#ececec","#111111",16), svg_text(600,515,"AdmitRelaxedBatch at b",28), svg_text(600,558,"BatchReceive(bid, rst)；无 A/m 不等条件",22), svg_arrow(305,390,500,465), svg_arrow(895,390,700,465)]
    s += [svg_rect(120,665,960,95,"#f5f5f5"), svg_text(600,720,"ProcessSlot1 at r_1 → ReceiverAccept(A, oid, m, bid, rst)",24), svg_rect(120,835,960,95,"#f5f5f5"), svg_text(600,890,"ProcessSlot2 at r_2 → ReceiverAccept(A, oid, m, bid, rst)",24), svg_arrow(600,580,600,665), svg_arrow(600,760,600,835)]
    s += [svg_rect(100,990,1000,80,"#ffffff","#555555",14), svg_text(600,1042,"同一 (bid, rst)，且 s < b < r_1 < r_2",28), svg_arrow(600,930,600,990)]
    s += [svg_rect(20,480,200,420,"#ffffff","#777777",15), svg_text(120,530,"持久来源事实",22), svg_text(120,575,"!Sent(A,oid,m)",22), '<line x1="220" y1="650" x2="360" y2="705" stroke="#555555" stroke-width="4" stroke-dasharray="10 7"/>', '<line x1="220" y1="700" x2="360" y2="880" stroke="#555555" stroke-width="4" stroke-dasharray="10 7"/>', svg_text(30,1130,"虚线表示两个处理规则读取同一持久来源事实，不表示发生第二次发送。",20,"start"), "</svg>"]
    (OUT / "figure-2.svg").write_text("\n".join(s), encoding="utf-8")


if __name__ == "__main__":
    make_figure1()
    make_figure2()
    print("created", OUT / "figure-1.svg", OUT / "figure-2.svg")
