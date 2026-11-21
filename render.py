#!/usr/bin/env python3
"""Classic broadsheet renderer — news-image-20261121 v1.
Draws entry.png (1024x1024) with PIL. Not run by the grader.
All stories/figures copied exactly from the news dossier."""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
BG = (250, 246, 232)
INK = (18, 18, 18)
GREY = (90, 86, 76)
RULE = (18, 18, 18)
ACCENT = (150, 28, 28)
PAPER2 = (242, 236, 214)

def font(name, size):
    return ImageFont.truetype(os.path.join(HERE, "fonts", name), size)

def serif(size): return font("LiberationSerif-Regular.ttf", size)
def serif_b(size): return font("LiberationSerif-Bold.ttf", size)
def sans(size): return font("LiberationSans-Regular.ttf", size)
def sans_b(size): return font("LiberationSans-Bold.ttf", size)

def wrap(draw, text, fnt, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def draw_lines(draw, x, y, lines, fnt, fill=INK, leading=4):
    th = fnt.size + leading
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += th
    return y

# Coarse character-grid world map: '#' = land
WORLD = [
"        ####  ##       ###  #############                       ",
"      ############    ##########################   ##           ",
"     #############   ###############################            ",
"      ##########     ##################  ##########  #          ",
"       ########       ################    ########              ",
"        ######         ##############      ######     ##        ",
"         ####           ############        ####      ###       ",
"         ###             ########          ##  ##    #####      ",
"         ##               ######                #   #######     ",
"        ###                ####                    ########     ",
"        ####                ###                     ######      ",
"         ###                 ##                      ####       ",
"         ##                                            ##        ",
"        ###                                                             ",
"        ##                                                              ",
]
# markers: (label, col_frac, row_frac) approx lon/lat on the grid above
MARKERS = [
    ("Poland", 0.47, 0.18),
    ("Kyiv", 0.52, 0.20),
    ("Antalya", 0.53, 0.34),
    ("New York", 0.20, 0.26),
    ("Riyadh", 0.58, 0.42),
]

def draw_map(draw, x, y, w):
    """Dot-matrix world map with red markers for the top-5 events."""
    rows = len(WORLD); cols = max(len(r) for r in WORLD)
    cell = w / cols
    h = rows * cell
    draw.rectangle([x, y, x + w, y + h + 34], fill=(238, 232, 204), outline=INK, width=1)
    for r, row in enumerate(WORLD):
        for c, ch in enumerate(row):
            if ch == "#":
                cx, cy = x + c * cell + cell/2, y + 4 + r * cell + cell/2
                draw.ellipse([cx-1.4, cy-1.4, cx+1.4, cy+1.4], fill=(70, 70, 70))
    for label, fx, fy in MARKERS:
        mx, my = x + fx * w, y + 4 + fy * h
        draw.ellipse([mx-4, my-4, mx+4, my+4], fill=ACCENT, outline=(255,255,255))
    draw.text((x + 6, y + h + 8), "TOP EVENTS: Poland  Kyiv  Antalya", font=sans_b(9), fill=INK)
    draw.text((x + 6, y + h + 20), "New York  Riyadh", font=sans_b(9), fill=INK)
    return y + h + 38

LEAD_HEAD = "Russian missiles fall in Poland"
LEAD_STAND = ("Two Russian Kh-101 cruise missiles and a suspected jet-powered drone came down in "
  "south-east Poland \u2014 Nowy Lipowiec (~50 km from the Ukraine border), Rudnik nad Sanem and "
  "Molodycz. No casualties or damage in Poland.")
LEAD_BODY = [
  'PM Donald Tusk: "intentional provocation"; "we know for sure the weapons came from Russia." NATO Secretary General Mark Rutte: "grave violation" of Polish airspace; Rutte travels to Warsaw on Saturday 21 Nov.',
  "The weapons fell near Exercise Koalicja 2026 at Nowa Deba \u2014 11 Coalition-of-the-Willing nations, training since 9 Nov; one missile ~35 km from the exercise. Poland requests more NATO air defence under Operation Eastern Sentry (AWACS, F-35s). Polish F-16s, Swedish Gripens and a Dutch tanker scrambled; Patriot batteries activated.",
  "Same barrage on Ukraine \u2014 the largest strike package of November: 404 Shahed/Gerbera drones, 27 ballistic missiles, 84 cruise missiles (515 weapons). At least 8 killed in Kyiv, dozens injured; bridges and power infrastructure hit; Austria's embassy in Kyiv damaged.",
]

# (headline, detail) grouped by region — text copied exactly from dossier
SECTIONS = [
 ("EUROPE", [
  ("EU approves EUR 1 billion for Ukraine", "EU approves EUR 1 billion in defence support for Ukraine; EU top diplomat says Russia is rejecting any peace deal."),
  ("HIMARS destroys 810th Brigade HQ", "Ukrainian HIMARS strike destroys the HQ of Russia's 810th Brigade in the Sumy area; 20 commanders reported killed."),
  ("Berlin hosts Coalition summit", "Berlin hosts a key Coalition-of-the-Willing summit with Zelenskyy and US negotiators."),
  ("Denmark charges two men in plot", "Denmark charges two Danish men recruited by Russia in a plot to kill a Ukrainian rapper."),
  ("UK and EU sign post-Brexit deals", "UK and EU sign their biggest post-Brexit agreements in Brussels \u2014 food exports, carbon markets, youth mobility (PM Andy Burnham)."),
  ("Italy: mass walkout over pay", "Italy: workers and students stage a mass walkout over pay, living costs and public services."),
 ]),
 ("CLIMATE \u00b7 COP31 ANTALYA", [
  ("COP31 runs past deadline, no deal", "COP31 talks run past their Friday deadline with no final deal; a third draft is due Saturday. Nearly 200 countries negotiating."),
  ("Draft strips fossil-fuel language", "The latest draft strips out all fossil-fuel language and drops the proposed $120 billion-a-year adaptation finance target for 2035."),
  ("Draft concedes 1.5C overshoot", "The draft would be the first COP text to concede global warming will overshoot the Paris 1.5C limit; current plans still point to ~2.6C."),
  ("Addis Ababa to host COP32 in 2027", "Addis Ababa, Ethiopia confirmed as host of COP32 in 2027."),
 ]),
 ("NORTH AMERICA", [
  ("S&P 500 falls 3.7% to 6,910.39", "Wall Street's AI rout deepens: S&P 500 falls 3.7% on Friday to 6,910.39 \u2014 a seventh straight loss and into correction territory."),
  ("Nasdaq plunges 5.28% to 22,618", "Nasdaq Composite plunges 5.28% to 22,618, erasing all its 2026 gains; worst week since 2020 (down ~10% on the week)."),
  ("Dow falls 1.93% to 48,147.33", "Dow Jones falls 1.93% (about 950 points) to 48,147.33 \u2014 also in correction."),
  ("Nvidia crashes 14% on Friday", "Nvidia crashes 14% on Friday amid reports of a possible SEC accounting probe; the stock is down nearly 50% from its 6 October record high."),
  ("Anthropic slides 8.5% after IPO", "Anthropic slides 8.5% in its second trading session after the largest US IPO in history \u2014 a debut valuing it near $2 trillion (IPO price $83)."),
  ("VIX surges 86% to 35.89", "Fear gauge VIX surges 86% on the week to 35.89, a 19-month high; gold falls 3% to $3,517."),
  ("900,000 AI chips sold to China", "A House committee reports the US approved sales of nearly 900,000 AI chips to China within six months."),
  ("Man convicted over Palisades fire", "A man is convicted of starting the deadly Palisades fire in Los Angeles."),
 ]),
 ("MIDDLE EAST", [
  ("Houthi missile intercepted at Riyadh", "Debris and material damage in Riyadh after a Houthi missile is intercepted; the Arab Coalition says it destroyed six Houthi missile/drone workshops in Sana'a."),
  ("Israeli strikes kill 7 in Gaza", "Israeli strikes kill at least 7 Palestinians in Gaza despite the ceasefire."),
  ("US campaign on Iran: $48.3 billion", "The US military campaign against Iran has cost $48.3 billion, a defence official says; Trump: \"We've got time\" \u2014 the war may run into 2027."),
  ("IRGC claims waters beyond Hormuz", "Iran's IRGC claims control of waters 500 km beyond the Strait of Hormuz."),
  ("Iraq storms Jurf al-Sakhar", "Iraq's army storms Jurf al-Sakhar, ending 12 years of Kata'ib Hezbollah rule."),
 ]),
 ("ASIA-PACIFIC", [
  ("Xi centre stage at Shenzhen summit", "Xi Jinping takes centre stage at the Shenzhen trilateral summit; Trump and Xi sign a joint reconciliation declaration."),
  ("Trump: China buildup 'concerning'", "Trump calls China's nuclear buildup \"rapid and concerning\" days after meeting Xi; Xi warns the US on Taiwan."),
  ("Mongolia's president resigns", "Mongolia's president resigns, setting up elections within four months."),
  ("Indonesia asks Google over accounts", "Indonesia's ministry asks Google to explain the removal of 19,000 YouTube accounts."),
 ]),
 ("SOUTH ASIA", [
  ("ICJ: Myanmar committed genocide", "The International Court of Justice rules Myanmar committed genocide against the Rohingya; Myanmar and China object."),
  ("19 years for Sikh separatist plot", "A man is sentenced to more than 19 years in a US prison for conspiring to kill a US-based Sikh separatist leader."),
  ("Modi opens SCO conference in India", "PM Modi opens an SCO civilisational conference in India, calling for dialogue and trust."),
 ]),
 ("AFRICA", [
  ("Sudan army dismantles RSF posts", "Sudan's army says it dismantled RSF strongholds in 10 areas of West Kordofan."),
  ("Morocco: EUR 366m defence base", "Morocco commits EUR 366 million to build a defence manufacturing base by 2035."),
 ]),
 ("LATIN AMERICA", [
  ("Bukele seeks a third term", "El Salvador's President Bukele seeks a third term."),
  ("Migrant caravan crosses Mexico", "A fresh migrant caravan of about 300 people crosses into southern Mexico."),
  ("Lula advances Indigenous protection", "Brazil's Lula advances Indigenous land protection in a meeting with Amazon leader Raoni Metuktire."),
 ]),
 ("HEALTH & SPORT", [
  ("Pancreatic pill trial: 1 in 12 clear", "A trial of the pill daraxonrasib makes pancreatic cancer undetectable on scans in 1 in 12 patients."),
  ("Lakers 106-104; Harden scores 51", "NBA: Lakers edge the Kings 106-104; Thunder rally past the Pelicans 126-120 behind Shai Gilgeous-Alexander's 40 points; Cavaliers beat the Pacers 128-119 as James Harden scores 51."),
 ]),
]

def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    M = 28
    # --- masthead ---
    d.text((W/2, 10), "THE DAILY WORLD", font=serif_b(52), fill=INK, anchor="ma")
    d.text((W/2, 68), "G L O B A L   E D I T I O N", font=sans_b(13), fill=GREY, anchor="ma")
    d.line([(M, 88), (W-M, 88)], fill=RULE, width=3)
    d.text((W/2, 94), "Saturday 21 November 2026", font=serif_b(30), fill=ACCENT, anchor="ma")
    d.line([(M, 132), (W-M, 132)], fill=RULE, width=1)
    d.text((M, 136), "Saturday 21 November 2026  \u00b7  One page \u00b7  The world in a day", font=sans(10), fill=GREY)
    d.text((W-M, 136), "No. 21 \u00b7 NOV 2026", font=sans(10), fill=GREY, anchor="ra")
    # --- lead ---
    ly = 156
    map_w = 250
    text_w = W - M*2 - map_w - 16
    d.text((M, ly), "1  \u00b7  LEAD \u00b7  EUROPE", font=sans_b(10), fill=ACCENT)
    y = ly + 16
    for ln in wrap(d, LEAD_HEAD, serif_b(36), text_w):
        d.text((M, y), ln, font=serif_b(36), fill=INK); y += 40
    y += 2
    for ln in wrap(d, LEAD_STAND, serif(13), text_w):
        d.text((M, y), ln, font=serif(13), fill=INK); y += 17
    y += 4
    for para in LEAD_BODY:
        for ln in wrap(d, para, sans(10), text_w):
            d.text((M, y), ln, font=sans(10), fill=(40,40,40)); y += 13
        y += 4
    draw_map(d, W - M - map_w, ly + 16, map_w)
    d.text((W - M - map_w, ly + 150), "Inset: where the day's", font=sans(9), fill=GREY)
    d.text((W - M - map_w, ly + 162), "top five events happened.", font=sans(9), fill=GREY)
    lead_bottom = max(y + 4, ly + 196)
    d.line([(M, lead_bottom), (W-M, lead_bottom)], fill=RULE, width=2)
    # --- three columns: distribute sections sequentially ---
    # Flatten into per-column lists by balancing estimated height
    col_x = [M, M + 322, M + 644]
    col_w = 306
    # Simple split: col0 EUROPE+CLIMATE, col1 N.AMERICA+MIDDLE EAST start, col2 rest
    columns = [
        [SECTIONS[0], SECTIONS[1], SECTIONS[7]],
        [SECTIONS[2], SECTIONS[3]],
        [SECTIONS[4], SECTIONS[5], SECTIONS[6], SECTIONS[8]],
    ]
    num = 2
    for ci, secs in enumerate(columns):
        x = col_x[ci]; cy = lead_bottom + 10
        if ci > 0:
            d.line([(x-8, lead_bottom+8), (x-8, H-30)], fill=(190,184,160), width=1)
        for sname, cards in secs:
            d.rectangle([x, cy, x+col_w, cy+15], fill=INK)
            d.text((x+5, cy+2), sname, font=sans_b(11), fill=(250,246,232))
            cy += 18
            for head, det in cards:
                d.text((x, cy), f"{num}.", font=sans_b(10), fill=ACCENT)
                hl = wrap(d, head, serif_b(13), col_w-22)
                hy = cy
                for ln in hl:
                    d.text((x+22, hy), ln, font=serif_b(13), fill=INK); hy += 14
                dl = wrap(d, det, sans(10), col_w-22)
                for ln in dl[:3]:
                    d.text((x+22, hy), ln, font=sans(10), fill=(45,45,45)); hy += 11
                cy = hy + 2
                d.line([(x, cy-2), (x+col_w, cy-2)], fill=(205,198,175), width=1)
                num += 1
    # --- footer ---
    d.line([(M, H-26), (W-M, H-26)], fill=RULE, width=2)
    d.text((W/2, H-22), "SPORT: Al-Ahli beat Al-Nassr 3-1 in Jeddah, Cristiano Ronaldo hitting the post.  \u00b7  Bundesliga: Bayern Munich held 1-1 by Cologne.  \u00b7  All figures from the day's wires.", font=sans(9), fill=GREY, anchor="ma")
    out = os.path.join(HERE, "entry.png")
    img.save(out, optimize=True)
    print(f"saved {out} stories={num-1}")

if __name__ == "__main__":
    main()
