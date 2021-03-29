from datetime import datetime
from intervals.exc import IllegalArgument


def process_str(s):
    return datetime.strptime(s, "%H:%M").strftime("%Y-%m-%d %H:%M")


def process_str_list(str_list):
    return [
        f"[{process_str(s.split('-')[0])}, " f"{process_str(s.split('-')[1])}]"
        for s in str_list
    ]


def process_dti(x):
    return str(x)[12:17] + "-" + str(x)[33:38]


def intersect(seg1, seg2):
    flag = False
    for x in seg1:
        if flag is True:
            break
        for y in seg2:
            try:
                x & y
                flag = True
                break
            except IllegalArgument:
                continue
    return flag
