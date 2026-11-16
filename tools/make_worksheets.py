# 產生「譬喻練功單」假學生作答圖（全部虛構，座號代替姓名）＋教師答案卷
import os, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
FD = "/System/Library/AssetsV2/com_apple_MobileAsset_Font8/"
def find(name):
    for root, _, fs in os.walk(FD):
        for f in fs:
            if f == name: return os.path.join(root, f)
PRINT = find("Yuanti.ttc"); HANDS = [find("Hanzipen.ttc"), find("Hannotate.ttc")]
OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "assets", "files", "學習單")
os.makedirs(OUT, exist_ok=True)
W, H = 1654, 2339  # A4 200dpi
f = lambda s, p=PRINT, i=0: ImageFont.truetype(p, s, index=i)

Q = [
 ("一、下列哪一句用了「譬喻」？（　　）", ["① 這間教室裡有很多書。", "② 弟弟今天跑得非常快。", "③ 天上的白雲像一團團棉花糖。", "④ 他長得好像他的爸爸。"]),
 ("二、找出譬喻句裡被比的 A 和拿來比的 B。", ["(1) 友誼像一座橋，把我們連在一起。　A：＿＿＿　B：＿＿＿", "(2) 月亮是夜空裡的小燈籠。　　　　　A：＿＿＿　B：＿＿＿"]),
 ("三、把「操場上的人很多。」改寫成譬喻句。", []),
 ("四、「時間像流水。」時間和流水有什麼相似的地方？", []),
 ("五、下面的句子是不是譬喻？是的打○，不是的打×。", ["(1) 妹妹的笑容好像溫暖的陽光。（　　）", "(2) 我好像忘了帶數學作業。（　　）"]),
]
# 每位學生的作答（虛構）
ANS = {
 "答案卷": {"1":"③","2a":("友誼","橋"),"2b":("月亮","小燈籠"),"3":"操場上的人像螞蟻一樣多，密密麻麻擠在一起。（參考：要有 A、B、喻詞）","4":"都會一直往前走，過去了就回不來。","5a":"○","5b":"×（「好像」是猜測，不是比喻）"},
 "01":{"1":"③","2a":("友誼","橋"),"2b":("月亮","小燈籠"),"3":"操場上的人多得像下課時的福利社。","4":"都一直往前，不會回頭。","5a":"○","5b":"×"},
 "02":{"1":"③","2a":("友誼","橋"),"2b":("月亮","夜空"),"3":"操場上的人像沙丁魚一樣。","4":"都會流走。","5a":"○","5b":"○"},
 "03":{"1":"④","2a":("友誼","橋"),"2b":("月亮","燈籠"),"3":"操場上的人好像很多。","4":"時間過的很快","5a":"○","5b":"○"},
 "04":{"1":"③","2a":("友誼","橋"),"2b":("月亮","小燈籠"),"3":"操場上的人像一群螞蟻，在地上爬來爬去。","4":"","5a":"○","5b":"×"},
 "05":{"1":"③","2a":("我們","橋"),"2b":("月亮","小燈籠"),"3":"操場上的人多得像夜市。","4":"都是一直流，停不下來","5a":"○","5b":"○"},
 "06":{"1":"①","2a":("友誼","一座橋"),"2b":("夜空","小燈籠"),"3":"操場好像菜市場。","4":"流水會流，時間也會流","5a":"×","5b":"×"},
}
def page(who, a):
    random.seed(who)
    im = Image.new("RGB", (W, H), (252, 251, 246)); d = ImageDraw.Draw(im)
    hand = HANDS[int(who) % 2] if who.isdigit() else PRINT
    hc = (40, 50, 120) if who.isdigit() else (200, 30, 30)
    def hw(xy, s, size=50):
        x, y = xy
        if who.isdigit(): x += random.randint(-6, 6); y += random.randint(-5, 5)
        d.text((x, y), s, font=f(size, hand), fill=hc)
    d.text((110, 90), "五年級　國語　譬喻練功單（研習示範用，虛構資料）", font=f(54), fill=(20, 30, 60))
    d.text((110, 175), "五年　　班　　號", font=f(44), fill=(20, 30, 60))
    if who.isdigit():
        x1 = 110 + d.textlength("五年", font=f(44)); x2 = 110 + d.textlength("五年　　班", font=f(44))
        hw((x1 + 20, 160), "2", 50); hw((x2 + 20, 160), who.lstrip("0"), 50)
    else: d.text((560, 175), "【教師答案卷】", font=f(44), fill=hc)
    d.line((110, 250, W - 110, 250), fill=(60, 70, 110), width=3)
    y = 300
    for qi, (q, opts) in enumerate(Q):
        d.text((110, y), q, font=f(44), fill=(20, 30, 60)); y += 80
        if qi == 0:
            for o in opts: d.text((170, y), o, font=f(40), fill=(30, 30, 30)); y += 64
            hw((800, 290), a["1"], 54)
        elif qi == 1:
            for k, o in zip(("2a", "2b"), opts):
                d.text((170, y), o, font=f(40), fill=(30, 30, 30))
                A, B = a[k]; base = 170 + int(d.textlength(o.split("A：")[0], font=f(40)))
                hw((base + 80, y - 16), A, 46); hw((base + 330, y - 16), B, 46); y += 90
        elif qi in (2, 3):
            for _ in range(3): d.line((170, y + 70, W - 140, y + 70), fill=(170, 175, 195), width=2); y += 90
            txt = a[str(qi + 1)]; yy = y - 270
            while txt:
                hw((180, yy), txt[:26], 48); txt = txt[26:]; yy += 90
            y += 20
        else:
            for k, o in zip(("5a", "5b"), opts):
                d.text((170, y), o, font=f(40), fill=(30, 30, 30))
                x0 = 170 + int(d.textlength(o.split("（")[0], font=f(40))) + 30
                hw((x0, y - 10), a[k], 46); y += 80
        y += 40
    if who.isdigit():  # 稍微旋轉、模糊，像手機拍的
        im = im.rotate(random.uniform(-1.2, 1.2), expand=False, fillcolor=(235, 233, 225)).filter(ImageFilter.GaussianBlur(0.6))
    name = f"譬喻練功單_{who}號.jpg" if who.isdigit() else "譬喻練功單_教師答案卷.jpg"
    im.save(os.path.join(OUT, name), quality=85)
for k, v in ANS.items(): page(k, v)
print(sorted(os.listdir(OUT)))
