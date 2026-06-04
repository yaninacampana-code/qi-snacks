from PIL import Image, ImageDraw, ImageFont

base = r'C:\Users\YaninaCelesteCampana\Desktop\Welcome offer translations\QI'
font_dir = r'C:\Windows\Fonts'

# ── Load images ───────────────────────────────────────────────────────────────
img = Image.open(base + r'\logo final final.png').convert('RGBA')
new_product_orig = Image.open(
    base + r'\Glisines provenzal\generated-image (8).png'
).convert('RGBA')
draw = ImageDraw.Draw(img)

# ── Fonts ─────────────────────────────────────────────────────────────────────
f_badge = ImageFont.truetype(font_dir + r'\calibri.ttf',  10)
f_title = ImageFont.truetype(font_dir + r'\calibrib.ttf', 19)
f_desc  = ImageFont.truetype(font_dir + r'\calibri.ttf',  12)
f_price = ImageFont.truetype(font_dir + r'\calibrib.ttf', 24)
f_num   = ImageFont.truetype(font_dir + r'\calibrib.ttf', 16)


def draw_gram_badge(draw, x1, y1, x2, y2, text, bg, fg):
    w, h = x2 - x1, y2 - y1
    draw.rounded_rectangle([x1, y1, x2, y2], radius=max(2, h // 2 - 1),
                            fill=bg + (255,))
    bb = draw.textbbox((0, 0), text, font=f_badge)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    draw.text((x1 + (w - tw) // 2, y1 + (h - th) // 2 - 1),
              text, font=f_badge, fill=fg + (255,))


# ════════════════════════════════════════════════════════════════════════════
# PART 1 – Gram value corrections
# ════════════════════════════════════════════════════════════════════════════
draw_gram_badge(draw, 782, 878, 825, 905, "70 gr",
                (249, 241, 227), (30, 23, 6))          # 02: 80→70

draw_gram_badge(draw, 335, 1105, 382, 1128, "70 gr",
                (234, 242, 196), (55, 80, 25))          # 03: 50→70

draw_gram_badge(draw, 762, 1323, 812, 1356, "50 gr",
                (251, 243, 225), (30, 23, 6))           # 06: 60→50

draw_gram_badge(draw, 332, 1498, 377, 1525, "50 gr",
                (240, 247, 215), (55, 80, 25))          # 07: 40→50

# ════════════════════════════════════════════════════════════════════════════
# PART 2 – Item 08  (mirrors card 07 layout in the right column)
# Card 07 occupies x=9-472, y=1385-1570  →  mirror: x=490-953, y=1385-1570
# ════════════════════════════════════════════════════════════════════════════
CX1, CY1, CX2, CY2 = 490, 1385, 953, 1570   # card bounds

# 2a. White card background (same radius as other cards)
draw.rounded_rectangle([CX1, CY1, CX2, CY2], radius=12,
                        fill=(255, 255, 255, 255))

# 2b. "08" leaf badge — copy "07" leaf (x=8-65, y=1385-1455), replace text
leaf = img.crop((8, 1385, 65, 1455)).copy()   # 57×70 px
ld = ImageDraw.Draw(leaf)
leaf_green = (68, 116, 0, 255)
ld.rectangle([6, 6, 51, 54], fill=leaf_green)            # cover "07"
bb = ld.textbbox((0, 0), "08", font=f_num)
tw, th = bb[2] - bb[0], bb[3] - bb[1]
ld.text((6 + (45 - tw) // 2, 6 + (48 - th) // 2),
        "08", font=f_num, fill=(255, 255, 255, 255))
img.paste(leaf, (CX1 + 1, CY1), leaf)

# 2c. Product image — fit in ~185×150 area (card 07 image is ~185 wide)
MAX_W, MAX_H = 185, 150
pw, ph = new_product_orig.size
ratio = min(MAX_W / pw, MAX_H / ph)
nw, nh = int(pw * ratio), int(ph * ratio)
prod = new_product_orig.resize((nw, nh), Image.LANCZOS)
img_x = CX1 + 62
img_y = CY1 + 12 + (MAX_H - nh) // 2
img.paste(prod, (img_x, img_y), prod)

# 2d. Text — same x-offset from column start as card 07 (≈245 px)
TX = CX1 + 243
C_TITLE = (20, 40, 15, 255)
C_DESC  = (90, 90, 90, 255)
C_PRICE = (75, 125, 5, 255)

draw.text((TX, CY1 + 18),  "Grisines a la",    font=f_title, fill=C_TITLE)
draw.text((TX, CY1 + 42),  "provenzal",         font=f_title, fill=C_TITLE)
draw.text((TX, CY1 + 78),  "Altos en proteína", font=f_desc,  fill=C_DESC)
draw.text((TX, CY1 + 93),  "vegetal.",          font=f_desc,  fill=C_DESC)
draw.text((TX, CY1 + 120), "$2500",             font=f_price, fill=C_PRICE)

draw_gram_badge(draw,
                TX + 95, CY1 + 123, TX + 140, CY1 + 147,
                "50 gr", (249, 241, 227), (30, 23, 6))

# ── Save ──────────────────────────────────────────────────────────────────────
out_path = base + r'\logo editado.png'
img.convert('RGB').save(out_path)
print(f'Saved: {out_path}')
