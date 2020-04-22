from PIL import Image, ImageDraw, ImageFont
import textwrap
from pathlib import Path # to work with path

img_dir = str(Path(__file__).parents[1])+"/static/images/"
def get_nm_of_rq_rows(text_length, max_font_size=40, text_hight=45):
    # Note: the hight of the text pixel decrease by 11 by decrease of 10 in font size
    # total_chars_in_row = ((width*10)/(5*max_font_size))
    # rows required = text_length/ total_chars_in_row
    # valid rows =
    # maximum allowed columns = text_hight * rows required

    w = 900
    h = 700
    font_size = 0
    start_from = 0
    #max_chars = 0
    font_size = max_font_size
    tot_row_chars = ((w*10)/(5*max_font_size))
    req_rows = text_length / tot_row_chars
    allowed_rows = h/text_hight
    max_hieght = 0
    print(w, max_font_size, tot_row_chars,text_length,req_rows, allowed_rows)
    mybool=True
    while mybool:
        print(f""" in loop, {w, h, text_length, font_size, text_hight,
              tot_row_chars,req_rows,allowed_rows}""")

        if req_rows<=allowed_rows :
            print(f""" in loop, {w, h, text_length, font_size, text_hight,
              tot_row_chars,req_rows,allowed_rows}""")
            #mybool=False
            start_from = text_hight* ((int((int(allowed_rows))-(int(req_rows))))/2)
            break
        else:
            print(f"in else block {font_size, text_hight }")
            font_size = font_size-10
            text_hight = text_hight -11
            tot_row_chars = ((w*10)/(5*font_size))
            req_rows = text_length / tot_row_chars
            allowed_rows = h/text_hight
            start_from = text_hight* ((int((int(allowed_rows))-(int(req_rows))))/2)

    return font_size, tot_row_chars, req_rows+1,start_from

def generate_image(data):
    font_size, tot_row_chars, req_rows, start_from = get_nm_of_rq_rows(len(data))

    # mainprogram to draw image
    image = Image.new('RGB', (900, 700), (173, 173, 173))
    drawer = ImageDraw.Draw(image)
    #font_zise = 18
    #font = ImageFont.truetype('/Windows/Fonts/Arial.ttf', font_size)
    font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", font_size)

    size = drawer.textsize(data, font=font)
    #offset = font.getoffset(STRING)
    margin = 10
    offset = start_from
    novo = textwrap.wrap(data, width=tot_row_chars)
    for line in novo:
        #print(margin, offset)
        drawer.text((margin, offset), line, font=font, fill="#f9f9f9", outline='black')
        #print(font.getsize(line)[1])
        offset += font.getsize(line)[1]

    ract_shap=[(margin-5, tot_row_chars), (10 + size[1] + offset, 10+ size[1] + tot_row_chars +offset)]
    print(ract_shap)
    #drawer.rectangle(ract_shap, outline='black')
    image.save(img_dir + '/summary.png', 'PNG')




# drawing text
#STRING = 'Hello, python language!'
#STRING = """Centre suspends MPLAD funds for 2 years to oppose 'arbitrary diktat' #LockdownPeCharcha Report Nepal government extends ongoing nationwide lockdown till April 15. shares a Harry Potter-inspired lockdown message RT . Government eases export curbs on 24 pharma ingredients medicines #CoronavirusLockdown. ब रह रणनीति मोद सरका ऐस हटाएग लॉकडाउ #CoronavirusLockdown. In Pics Limited operations post lockdown. East Coast Railways deploys drones to guard assets amid #lockdown. RT . shares a Harry Potter-inspired lockdown message. RT ."""
#drawer.text((10, 10), STRING, fill='black', font=font)

# drawing rectangle surrounding text
#size = drawer.textsize(STRING, font=font)
#offset = font.getoffset(STRING)
#print(len(STRING), font_zise*len(STRING), size, offset)

#margin = offset = 20
#novo = textwrap.wrap(STRING, width=45)
#for line in novo:
#    #print(margin, offset)
#    drawer.text((margin, offset), line, font=font, fill="#aa0000", outline='black')
#    print(font.getsize(line)[1])
#    offset += font.getsize(line)[1]
#print(offset)
#drawer.rectangle((10, 10, 10 + size[0] + 0, 10 + size[1] + offset), outline='black')

#image.save('example.png', 'PNG')
