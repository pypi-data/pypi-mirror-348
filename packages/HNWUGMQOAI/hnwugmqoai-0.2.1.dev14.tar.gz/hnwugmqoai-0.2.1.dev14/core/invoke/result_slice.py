def split_sum_res(sum_res, max_length):
    """
    将 sum_res 分组，每组的字符串总长度不超过 max_length。
    若某个元素的字符串长度超过 max_length，则单独成组。
    """
    groups = []
    current_group = []
    current_length = 0

    for item in sum_res:
        s = str(item)
        len_s = len(s)

        if len_s > max_length:
            if current_group:
                groups.append(current_group)
                current_group = []
                current_length = 0
            groups.append([item])
        else:
            if current_length + len_s > max_length:
                groups.append(current_group)
                current_group = [item]
                current_length = len_s
            else:
                current_group.append(item)
                current_length += len_s

    if current_group:
        groups.append(current_group)

    return groups
