def normalize(arr, mulv):
    norm_arr = []
    abs_arr = []
    for val in arr:
        abs_arr.append(abs(val))
    maxv = max(abs_arr)
    for v in arr:
        try:
            norm_arr.append((v*mulv)/maxv)
        except:
            norm_arr.append(0)
    return norm_arr

