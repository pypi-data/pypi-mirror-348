import cython
cimport cython
import numpy as np
cimport numpy as np
import pandas as pd

asciifunc = np.frompyfunc(ascii, 1, 1)
reprfunc = np.frompyfunc(repr, 1, 1)
cdef:
    str ResetAll = "\033[0m"
    str Bold = "\033[1m"
    str Dim = "\033[2m"
    str Underlined = "\033[4m"
    str Blink = "\033[5m"
    str Reverse = "\033[7m"
    str Hidden = "\033[8m"
    str ResetBold = "\033[21m"
    str ResetDim = "\033[22m"
    str ResetUnderlined = "\033[24m"
    str ResetBlink = "\033[25m"
    str ResetReverse = "\033[27m"
    str ResetHidden = "\033[28m"
    str Default = "\033[39m"
    str Black = "\033[30m"
    str Red = "\033[31m"
    str Green = "\033[32m"
    str Yellow = "\033[33m"
    str Blue = "\033[34m"
    str Magenta = "\033[35m"
    str Cyan = "\033[36m"
    str LightGray = "\033[37m"
    str DarkGray = "\033[90m"
    str LightRed = "\033[91m"
    str LightGreen = "\033[92m"
    str LightYellow = "\033[93m"
    str LightBlue = "\033[94m"
    str LightMagenta = "\033[95m"
    str LightCyan = "\033[96m"
    str White = "\033[97m"
    str BackgroundDefault = "\033[49m"
    str BackgroundBlack = "\033[40m"
    str BackgroundRed = "\033[41m"
    str BackgroundGreen = "\033[42m"
    str BackgroundYellow = "\033[43m"
    str BackgroundBlue = "\033[44m"
    str BackgroundMagenta = "\033[45m"
    str BackgroundCyan = "\033[46m"
    str BackgroundLightGray = "\033[47m"
    str BackgroundDarkGray = "\033[100m"
    str BackgroundLightRed = "\033[101m"
    str BackgroundLightGreen = "\033[102m"
    str BackgroundLightYellow = "\033[103m"
    str BackgroundLightBlue = "\033[104m"
    str BackgroundLightMagenta = "\033[105m"
    str BackgroundLightCyan = "\033[106m"
    str BackgroundWhite = "\033[107m"



cdef:
    list[str] colors2rotate=[
        LightRed,
        LightGreen,
        LightYellow,
        LightBlue,
        LightMagenta,
        LightCyan,
        White,
    ]

@cython.nonecheck(True)
cpdef printdf(
    object df,
    Py_ssize_t column_rep=70,
    Py_ssize_t max_lines=0,
    Py_ssize_t max_colwidth=300,
    Py_ssize_t ljust_space=2,
    str sep=" | ",
    bint vtm_escape=True,
):
    cdef:
        dict[Py_ssize_t, np.ndarray] stringdict= {}
        dict[Py_ssize_t, Py_ssize_t] stringlendict= {}
        list[str] df_columns, allcolumns_as_string
        Py_ssize_t i, len_a, len_df_columns, lenstr, counter, j, len_stringdict0, k, len_stringdict
        str stringtoprint, dashes, dashesrep
        np.ndarray a
        str tmpstring=""
        list[str] tmplist=[]
        str tmp_newline="\n"
        str tmp_rnewline="\r"
        str tmp_newline2="\\n"
        str tmp_rnewline2="\\r"
    if vtm_escape:
        print('\033[12:2p')
    if len(df) > max_lines and max_lines > 0:
        a = df.iloc[:max_lines].reset_index(drop=False).T.__array__()
    else:
        a = df.iloc[:len(df)].reset_index(drop=False).T.__array__()
    try:
        df_columns = ["iloc"] + [str(x) for x in df.columns]
    except Exception:
        try:
            df_columns = ["iloc",str(df.name)]
        except Exception:
            df_columns = ["iloc",str(0)]
    len_a=len(a)
    for i in range(len_a):
        try:
            stringdict[i] = np.array([repr(qx)[:max_colwidth] for qx in a[i]])
        except Exception:
            stringdict[i] = np.array([ascii(qx)[:max_colwidth] for qx in a[i]])
        stringlendict[i] = (stringdict[i].dtype.itemsize // 4) + ljust_space
    for i in range(len_a):
        lenstr = len(df_columns[i])
        if lenstr > stringlendict[i]:
            stringlendict[i] = lenstr + ljust_space
        if max_colwidth > 0:
            if stringlendict[i] > max_colwidth:
                stringlendict[i] = max_colwidth

    allcolumns_as_string = []
    len_df_columns=len(df_columns)
    for i in range(len_df_columns):
        stringtoprint = str(df_columns[i])[: stringlendict[i]].ljust(stringlendict[i])
        allcolumns_as_string.append(stringtoprint)
    allcolumns_as_string_str = sep.join(allcolumns_as_string) + sep
    dashes = "-" * (len(allcolumns_as_string_str) + 2)
    dashesrep = dashes + "\n" + allcolumns_as_string_str + "\n" + dashes
    counter = 0
    len_stringdict0 = len(stringdict[0])
    len_stringdict=len(stringdict)
    for j in range(len_stringdict0):
        if column_rep > 0:
            if counter % column_rep == 0:
                tmplist.append(dashesrep)
        counter += 1
        tmpstring=""
        for k in range(len_stringdict):
            tmpstring+=((
                f"{colors2rotate[k % len(colors2rotate)] + stringdict[k][j][: stringlendict[k]].replace(tmp_newline,tmp_newline2).replace(tmp_rnewline, tmp_rnewline2).ljust(stringlendict[k])}{ResetAll}{sep}"
            ))
        tmplist.append(tmpstring)
    print("\n".join(tmplist))
    return ""

