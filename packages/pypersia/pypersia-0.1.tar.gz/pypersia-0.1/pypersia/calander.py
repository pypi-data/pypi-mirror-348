def jalali_to_gregorian(j_y, j_m, j_d):
    g_days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    j_days_in_month = [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29]
    
    gy = j_y + 621
    leap_j = (j_y % 33 in [1, 5, 9, 13, 17, 22, 26, 30])
    leap_g = (gy % 4 == 0 and (gy % 100 != 0 or gy % 400 == 0))
    
    j_day_no = sum(j_days_in_month[:j_m-1]) + j_d
    if leap_j and j_m > 6:
        j_day_no += 1
    
    g_day_no = j_day_no + 79
    if leap_g and g_day_no > 365:
        g_day_no -= 1
        gy += 1
    
    for i, days in enumerate(g_days_in_month):
        if g_day_no <= days:
            return gy, i+1, g_day_no
        g_day_no -= days
    
def gregorian_to_jalali(g_y, g_m, g_d):
    g_days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    j_days_in_month = [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29]
    
    jy = g_y - 621
    leap_j = (jy % 33 in [1, 5, 9, 13, 17, 22, 26, 30])
    
    g_day_no = sum(g_days_in_month[:g_m-1]) + g_d
    if (g_y % 4 == 0 and (g_y % 100 != 0 or g_y % 400 == 0)) and g_m > 2:
        g_day_no += 1

    j_day_no = g_day_no - 79
    for i, days in enumerate(j_days_in_month):
        if j_day_no <= days:
            return jy, i+1, j_day_no
        j_day_no -= days

def hijri_to_gregorian(h_y, h_m, h_d):
    hijri_epoch = 1948439  # Reference: 1 Muharram 1 AH = July 16, 622 CE
    g_day_no = (h_y - 1) * 354 + (h_m - 1) * 29.5 + h_d + hijri_epoch
    gy = 622 + int(g_day_no // 365.25)
    
    remaining_days = g_day_no - int((gy - 622) * 365.25)
    g_days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    for i, days in enumerate(g_days_in_month):
        if remaining_days <= days:
            return gy, i+1, int(remaining_days)
        remaining_days -= days

def gregorian_to_hijri(g_y, g_m, g_d):
    hijri_epoch = 1948439
    g_days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    g_day_no = (g_y - 622) * 365.25 + sum(g_days_in_month[:g_m-1]) + g_d
    h_y = 1 + int((g_day_no - hijri_epoch) // 354)
    
    remaining_days = g_day_no - hijri_epoch - int((h_y - 1) * 354)
    h_days_in_month = [30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 29]
    
    for i, days in enumerate(h_days_in_month):
        if remaining_days <= days:
            return h_y, i+1, int(remaining_days)
        remaining_days -= days

