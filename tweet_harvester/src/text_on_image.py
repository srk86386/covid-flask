import time


text_length = 789
max_font_size = 40
text_hight = 45


def get_nm_of_rq_rows(text_length, max_font_size, text_hight):
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
        #print(f""" in loop, {w, h, text_length, font_size, text_hight,
              tot_row_chars,req_rows,allowed_rows}""")

        if req_rows<=allowed_rows :
            #print(f"in if block {font_size, text_hight }")
            #mybool=False
            start_from = text_hight* ((int((int(allowed_rows))-(int(req_rows))))/2)
            break
        else:
            #print(f"in else block {font_size, text_hight }")
            font_size = font_size-10
            text_hight = text_hight -11
            tot_row_chars = ((w*10)/(5*font_size))
            req_rows = text_length / tot_row_chars
            allowed_rows = h/text_hight
            start_from = text_hight* ((int((int(allowed_rows))-(int(req_rows))))/2)

    return font_size, tot_row_chars, req_rows+1,start_from



print(get_nm_of_rq_rows( text_length, max_font_size,text_hight))
