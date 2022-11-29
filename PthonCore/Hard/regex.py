# write your code here

def comp_str(re, txt):
    if re == txt:
        return True
    elif re == '.' and len(txt) == 1:
        return True
    elif re == '':
        return True
    else:
        return False


def comp_literal(re, txt):
    if re == txt:
        return True
    elif re == '':
        return True
    else:
        return False


def comp_recursive(re, txt):
    if re == '':
        return True
    if txt == '':
        if re == '$':
            return True
        return False
    if re[0] == '\\':
        if not comp_literal(re[1], txt[0]):
            return comp_recursive(re, txt[1:])
        else:
            return comp_recursive(re[2:], txt[1:])

    if not comp_str(re[0], txt[0]):
        if len(re[1:]) > 1 and re[1] in ('?', '*'):
            return comp_recursive(re[2:], txt[0:])
        elif len(re[1:]) == 1 and re[1] in ('?', '*'):
            return True
        return False
    if len(re[1:]) > 1:
        if re[1] == '*':
            return comp_recursive(re, txt[1:]) or comp_recursive(re[2:], txt[1:])
        if re[1] == '?':
            return comp_recursive(re[2:], txt[1:])
        if re[1] == '+':
            new_re = re[0] + '*' + re[2:]
            return comp_recursive(new_re, txt[1:]) or comp_recursive(re[2:], txt[1:])
        return comp_recursive(re[1:], txt[1:])
    if len(re[1:]) == 1 and re[1] in ('*', '+', '?'):
        return True
    return comp_recursive(re[1:], txt[1:])


def comp_diff(re, txt):
    if re == '':
        return True
    if re[0] == '^':
        return comp_recursive(re[1:], txt)
    for i in range(len(txt)):
        new_txt = txt[i:]
        if comp_recursive(re, new_txt):
            return True
    return False


comp = input()
lst = comp.split('|')
res = comp_diff(lst[0], lst[1])
print(res)
