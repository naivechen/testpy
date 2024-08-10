def func(list):
    if len(list)<2:
        return None
    if list[0]>list[1]:
        max_num=list[0]
        sec_num=list[1]
    else:
        max_num=list[1]
        sec_num=list[0]
    for x in list[2:]:
        if x>max_num:
            sec_num=max_num
            max_num=x
        elif x>sec_num and x !=max_num:
            sec_num=x
    return sec_num