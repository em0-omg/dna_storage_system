from collections import Counter

# 参考https://torina.top/detail/316/
# ファイルサイズ表示をわかりやすく
def approximate_size(size, a_kilobyte_is_1024_bytes=False):

    SUFFIXES = {
        1000: ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'],
        1024: ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']
    }

    if size < 0:
        raise ValueError('number must be non-negative')

    multiple = 1024 if a_kilobyte_is_1024_bytes else 1000
    for suffix in SUFFIXES[multiple]:
        size /= multiple
        if size < multiple:
            return '{0:.1f} {1}'.format(size, suffix)

    raise ValueError('number too large')


# 10進数nをb進数に直す関数
#techtipshoge.blogspot.jp
def base10to(n,b):
    if (int(n/b)):
        return base10to(int(n/b), b) + str(n%b)
    return str(n%b)

# n進数を10進数に
def Base_n_to_10(X,n):
    out = 0
    for i in range(1,len(str(X))+1):
        out += int(X[-i])*(n**(i-1))
    return out

# 10進数を3進数に
def base10_to_base3(n):
    if n == 0:
        return '0'
    s = ''
    while n != 0:
        s = str((n % 3)) + s
        n = n / 3
    return s

# 3進数を10進数に
def base3_to_base10(n):
    n = int(n)
    if n == 0:
        return 0

    res = 0
    b = 1
    while n != 0:
        res = res + (n % 10) * b
        n = n / 10
        b = 3 * b
    return res


# ランダマイズを解く
def reR(list):
    keystream = [
    '002000010110102111112122210011122221010102121222022000221201020221002121121000212222021211121122221',
    '202020122121210120001200210222112020222022222220220001221012111022121120202022211221112202002121022',
    '221221101200221120220011002222100000020200021121021020122100021201010210202002000101020022121100100',
    '100122100011112100120210020011102201122122100100120122212000021220022012202201100010212222110222020']

    for i in range(len(list)):
        base0 = ''
        base1 = ''
        base2 = []
        base3 = ''
        base4 = []
        base5 = ''
        base6 = ''

        # 4進数割り当て
        base0 = list[i]
        for ch in base0:
            if ch == 'A':
                base1 = base1 + '0'
            elif ch == 'C':
                base1 = base1 + '1'
            elif ch == 'G':
                base1 = base1 + '2'
            elif ch == 'T':
                base1 = base1 + '3'

        # 一個隣のから引き算をしていって、
        for t in range(1, len(base1)):
            base2.append((str((int(base1[t]) - int(base1[t - 1])) % 4)))

        # マイナス1
        for t in range(len(base2)):
            base2[t] = str((int(base2[t]) - 1) % 3)


        j = i % 4
        key = keystream[j]

        # keystream引き算
        for t in range(len(base2)):
            ch = (str((int(base2[t]) - int(key[t])) % 3))

            base3 = base3 + ch

        # ここから、やった手順を逆に遡る。プラス1。
        for t in range(len(base3)):
            a = (int(base3[t]) + 1) % 4
            base4.append(str(a))

        # successive differences
        n1 = base1[0]  # 1文字目n1は変わらない
        base5 = base5 + n1

        for t in range(len(base4)):
            sumv = int(n1)
            for s in range(t + 1):
                sumv = (sumv + int(base4[s])) % 4
            base5 = base5 + str(sumv)

        for ch in base5:
            if ch == '0':
                base6 = base6 + 'A'
            elif ch == '1':
                base6 = base6 + 'C'
            elif ch == '2':
                base6 = base6 + 'G'
            elif ch == '3':
                base6 = base6 + 'T'

        list[i] = base6


#  受け取った塩基文字列をreverse, complement
def reverse_complement(s):
    reverse = ''

    complement_dict = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}

    for c in s:
        reverse = complement_dict[c] + reverse

    return reverse


# ローテーション表に従って逆戻し
def r_rotate(text, pre_N):

    ans = ''

    for ch in text:
        if pre_N == "A":
            if ch == "C":
                ans = ans + '0'
                pre_N = "C"
            elif ch == "G":
                ans = ans + '1'
                pre_N = "G"
            elif ch == "T":
                ans = ans + '2'
                pre_N = "T"
            else:
                ans = ans + 'X'
                pre_N = "A"
        elif pre_N == "C":
            if ch == "G":
                ans = ans + '0'
                pre_N = "G"
            elif ch == "T":
                ans = ans + '1'
                pre_N = "T"
            elif ch == "A":
                ans = ans + '2'
                pre_N = "A"
            else:
                ans = ans + 'X'
                pre_N = "A"
        elif pre_N == "G":
            if ch == "T":
                ans = ans + '0'
                pre_N = "T"
            elif ch == "A":
                ans = ans + '1'
                pre_N = "A"
            elif ch == "C":
                ans = ans + '2'
                pre_N = "C"
            else:
                ans = ans + 'X'
                pre_N = "A"
        elif pre_N == "T":
            if ch == "A":
                ans = ans + '0'
                pre_N = "A"
            elif ch == "C":
                ans = ans + '1'
                pre_N = "C"
            elif ch == "G":
                ans = ans + '2'
                pre_N = "G"
            else:
                ans = ans + 'X'
                pre_N = "A"

    return ans

# Fs[['25塩基', '25塩基', '25塩基', '25塩基'], ...
# overlapした各セグメントを1文字ずつ比較して、一番出現頻度の多いものから文字列を作って返す
def checkOL(list):
    ans = []
    comL = []

    # 最初の1セグメントはそのまま
    ans.append(list[0][0])

    # 次のセグメントは2重だから評価できないためとりあえずそのまま
    ans.append(list[0][1])

    #３番目は3重 評価
    comL.append(list[0][2])
    comL.append(list[1][1])
    comL.append(list[2][0])

    text = ''
    for i in range(25):
        comCH = []
        for c in range(len(comL)):
            # 各セグメントのi文字目を比較リストに入れる
            comCH.append(comL[c][i])
        counter = Counter(comCH)
        # 一番出現頻度の多かった文字が正しいとして
        ch_freq = counter.most_common(1)
        text = text + ch_freq[0][0]
    ans.append(text)

    # 4番目以降は4重の繰り返し i=97まで
    for i in range(len(list)-3):
        #print(str(i)+'番目ok')
        comL = []
        comL.append(list[i][3])
        comL.append(list[i+1][2])
        comL.append(list[i+2][1])
        comL.append(list[i+3][0])

        text = ''
        for t in range(25):
            comCH = []
            for c in range(len(comL)):
                comCH.append(comL[c][t])
            counter = Counter(comCH)
            ch_freq = counter.most_common(1)
            text = text + ch_freq[0][0]
        ans.append(text)

    # 後ろ3重部分
    comL = []
    comL.append(list[len(list)-3][3])
    comL.append(list[len(list)-2][2])
    comL.append(list[len(list)-1][1])

    text = ''
    for i in range(25):
        comCH = []
        for c in range(len(comL)):
            comCH.append(comL[c][i])
        counter = Counter(comCH)
        ch_freq = counter.most_common(1)
        text = text + ch_freq[0][0]
    ans.append(text)

    # 残りの2セグメント
    ans.append(list[len(list)-1][2])
    ans.append(list[len(list)-1][3])
    ans = ''.join(ans)

    return ans

