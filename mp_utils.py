
def check_url(sub_url, start_url):
    if len(sub_url) == 0:
        return ""
    if sub_url[0] == "/":
        return sub_url
    relative_path = start_url[start_url.find('/', 10):]
    base_path = relative_path[0: relative_path.rfind('/') + 1]
    if sub_url.find(":") >= 0:
        return relative_path
    # path parsing
    num = 0
    i = 0
    while True:
        if sub_url[i: i+3] == "../":
            num += 1
        else:
            break
        i += 3
    sub_url = sub_url[3 * num:]
    if num > 0:
        j = len(base_path) - 2
        while True:
            if base_path[j] == '/':
                num -= 1
            if num == 0:
                break
            j -= 1
        base_path = base_path[0: j + 1]
    return base_path + sub_url
