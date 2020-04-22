from PIL import Image, ImageDraw, ImageFont

image = Image.new('RGB', (900, 700), (255, 255, 150))
drawer = ImageDraw.Draw(image)
font_zise = 18
font = ImageFont.truetype('/Windows/Fonts/Arial.ttf', font_zise)

# drawing text
#STRING = 'Hello, python language!'
STRING = """Centre suspends MPLAD funds for 2 years to oppose 'arbitrary diktat' #LockdownPeCharcha Report Nepal government extends ongoing nationwide lockdown till April 15. shares a Harry Potter-inspired lockdown message RT . Government eases export curbs on 24 pharma ingredients medicines #CoronavirusLockdown. ब रह रणनीति मोद सरका ऐस हटाएग लॉकडाउ #CoronavirusLockdown. In Pics Limited operations post lockdown. East Coast Railways deploys drones to guard assets amid #lockdown. RT . shares a Harry Potter-inspired lockdown message. RT ."""
#drawer.text((10, 10), STRING, fill='black', font=font)

# drawing rectangle surrounding text
size = drawer.textsize(STRING, font=font)
offset = font.getoffset(STRING)
print(len(STRING), font_zise*len(STRING), size, offset)
import textwrap
margin = offset = 20
novo = textwrap.wrap(STRING, width=45)
for line in novo:
    #print(margin, offset)
    drawer.text((margin, offset), line, font=font, fill="#aa0000", outline='black')
    print(font.getsize(line)[1])
    offset += font.getsize(line)[1]
print(offset)
drawer.rectangle((10, 10, 10 + size[0] + 0, 10 + size[1] + offset), outline='black')

image.save('example.png', 'PNG')
