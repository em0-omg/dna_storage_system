#from huffman_code import *
#from encode_decode import *

import random
import csv
import binascii
import os.path
import sys
from collections import Counter

# 参考github https://github.com/allanino/DNA/blob/master/dna/dna.py

#https://torina.top/detail/316/ ファイルサイズ表示をわかりやすく
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

def base10_to_base3(n):
    if n == 0:
        return '0'
    s = ''
    while n != 0:
        s = str((n % 3)) + s
        n = n / 3
    return s

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
    seg = ''
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



# Goldman Encoding
class Gld_encode:

    # Huffman code dictionary
    code ={}
    # Dictionary with files 2-trits
    files_trits = {}

    # 8ビット区切りのバイナリデータをセット
    def __init__(self):
        self.inputfilename = ''
        self.strands = {}
        self.n = 0
        self.N = 0
        self.ID = ''
        self.S1 = ''
        self.S2 = ''
        self.S3 = ''
        self.S4 = ''
        self.S5 = ''
        self.Fs = {}

        # 元の符号長 / 最終的な符号長
        self.density = 0
        self.filesize = ''
        self.putnt = 0


        # ハフマン符号表を読み取る
        huff_dict = open("huff3.dict", "r")
        csv_reader = csv.reader(huff_dict, delimiter=',')
        for row in csv_reader:
            self.code[row[0]] = row[1]


    # STEP1 ~ STEP2
    # バイナリデータ変換、ハフマン符号に従って3進数列へと変換
    def read_in_file(self, input_file):
        self.inputfilename = input_file
        trit = base10_to_base3(len(self.files_trits))
        trit = '0' * ( 2 -len(trit))+ trit

        s1 = ""
        with open(input_file, 'rb') as f:
            byte = f.read(1)
            while byte:
                s1 = s1 + self.code[str(int(binascii.hexlify(byte), 16))]
                byte = f.read(1)
        self.S1 = s1
        with open(self.inputfilename+'-origin_s1.txt', 'w') as f:
            f.write(self.S1)


    def makeS4(self):
        self.n = len(self.S1)
        # S2計算
        trits = base10to(self.n, 3)
        for i in range(25-len(trits)):
            self.S2 = self.S2 + '0'
        self.S2 = self.S2 + trits
        print('S2('+str(len(self.S2))+'文字) : ' + self.S2)
        # S3計算してS4生成
        self.S4 = self.S2 + self.S1
        for i in range(25-len(self.S4)%25):
            self.S3  = self.S3 + '0'
        self.S4 = self.S4 + self.S3

    # make S5
    def rotation(self):

        # 初期Previous Nucleotide
        pre_N = "A"

        # ローテーション表に従う
        for ch in self.S4:
            if pre_N == "A":
                if ch == "0":
                    self.S5 = self.S5 +"C"
                    pre_N = "C"
                elif ch == "1":
                    self.S5 = self.S5 +"G"
                    pre_N = "G"
                elif ch == "2":
                    self.S5 = self.S5 +"T"
                    pre_N = "T"
                else:
                    self.S5 = self.S5 +"X"
                    pre_N = "A"
            elif pre_N == "C":
                if ch == "0":
                    self.S5 = self.S5 +"G"
                    pre_N = "G"
                elif ch == "1":
                    self.S5 = self.S5 +"T"
                    pre_N = "T"
                elif ch == "2":
                    self.S5 = self.S5 +"A"
                    pre_N = "A"
                else:
                    self.S5 = self.S5 +"X"
                    pre_N = "A"
            elif pre_N == "G":
                if ch == "0":
                    self.S5 = self.S5 +"T"
                    pre_N = "T"
                elif ch == "1":
                    self.S5 = self.S5 +"A"
                    pre_N = "A"
                elif ch == "2":
                    self.S5 = self.S5 +"C"
                    pre_N = "C"
                else:
                    self.S5 = self.S5 +"X"
                    pre_N = "A"
            elif pre_N == "T":
                if ch == "0":
                    self.S5 = self.S5 +"A"
                    pre_N = "A"
                elif ch == "1":
                    self.S5 = self.S5 +"C"
                    pre_N = "C"
                elif ch == "2":
                    self.S5 = self.S5 +"G"
                    pre_N = "G"
                else:
                    self.S5 = self.S5 +"X"
                    pre_N = "A"


    def addID(self):

        # IDをつける(二桁の3進数)とりあえずランダム
        id_list = ['00', '01', '02', '10', '11', '12', '20', '21', '22']

        self.ID = '12'

    def makeFs(self):

        N = len(self.S5)

        # segmentの個数
        seg_num = int(N/25 - 3)

        # Fiのi
        F_i = int(N/25 - 4)

        t = 0
        for i in range(F_i+1):
            self.Fs['F'+str(i)] = self.S5[t:t+100]
            t = t + 25


    def r_and_complement(self):
        for i in range(len(self.Fs)):
            # 奇数番目は反転
            if i%2 == 1:
                self.Fs['F'+str(i)] = self.Fs['F'+str(i)][::-1]
                # 相補鎖にする
                text = self.Fs['F'+str(i)]
                c_text = ''
                for ch in text:
                    if ch == 'A':
                        c_text = c_text + 'T'
                    elif ch == 'T':
                        c_text = c_text + 'A'
                    elif ch == 'G':
                        c_text = c_text + 'C'
                    elif ch == 'C':
                        c_text = c_text + 'G'
                self.Fs['F'+str(i)] = c_text


    def randomize(self):

        self.keystream = ['002000010110102111112122210011122221010102121222022000221201020221002121121000212222021211121122221',
                     '202020122121210120001200210222112020222022222220220001221012111022121120202022211221112202002121022',
                     '221221101200221120220011002222100000020200021121021020122100021201010210202002000101020022121100100',
                     '100122100011112100120210020011102201122122100100120122212000021220022012202201100010212222110222020']


        for i in range(len(self.Fs)):
            base0 = ''
            base1 = ''
            base2 = []
            base3 = ''
            base4 = []
            base5 = ''
            base6 = ''


            # 4進数割り当て
            base0 = self.Fs['F'+str(i)]
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
                base2.append((str((int(base1[t]) - int(base1[t-1])) % 4)))

            # マイナス1
            for t in range(len(base2)):
                base2[t] = str((int(base2[t]) - 1) % 3)

            j = i % 4
            key = self.keystream[j]

            # keystream足し算
            for t in range(len(base2)):
                ch = (str((int(base2[t]) + int(key[t])) % 3))

                base3 = base3 + ch



            # ここから、やった手順を逆に遡る。プラス1。
            for t in range(len(base3)):
                a = (int(base3[t]) + 1) % 4
                base4.append(str(a))


            # successive differences
            n1 = base1[0] #1文字目n1は変わらない
            base5 = base5 + n1

            for t in range(len(base4)):
                #print('t:'+str(t))
                sumv = int(n1)
                #print('n1+', end='')
                for s in range(t+1):
                    #print('s'+str(s)+'+', end='')
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


            self.Fs['F'+str(i)] = base6

    def computeP_IX(self):

        for t in range(len(self.Fs)):
            P = int(self.ID[0])
            i3 = ''
            a = base10to(t, 3)
            if len(a) < 12:
                i3 = i3 + ('0'*(12-len(a))) + a

            for i in range(1, 13):
                if (i % 2) == 1:
                    # print('i3の' + str(i) + '番目:'+ str(i3[i]))
                    P = P + int(i3[i-1])

            P = P % 3

            IX = self.ID + i3 + str(P)
            pre_N = self.Fs['F'+str(t)][len(self.Fs[('F'+str(t))])-1]

            IX_text = ''
            for ch in IX:
                if pre_N == "A":
                    if ch == "0":
                        IX_text = IX_text + "C"
                        pre_N = "C"
                    elif ch == "1":
                        IX_text = IX_text + "G"
                        pre_N = "G"
                    elif ch == "2":
                        IX_text = IX_text + "T"
                        pre_N = "T"
                    else:
                        IX_text = IX_text + "X"
                        pre_N = "A"
                elif pre_N == "C":
                    if ch == "0":
                        IX_text = IX_text + "G"
                        pre_N = "G"
                    elif ch == "1":
                        IX_text = IX_text + "T"
                        pre_N = "T"
                    elif ch == "2":
                        IX_text = IX_text + "A"
                        pre_N = "A"
                    else:
                        IX_text = IX_text + "X"
                        pre_N = "A"
                elif pre_N == "G":
                    if ch == "0":
                        IX_text = IX_text + "T"
                        pre_N = "T"
                    elif ch == "1":
                        IX_text = IX_text + "A"
                        pre_N = "A"
                    elif ch == "2":
                        IX_text = IX_text + "C"
                        pre_N = "C"
                    else:
                        IX_text = IX_text + "X"
                        pre_N = "A"
                elif pre_N == "T":
                    if ch == "0":
                        IX_text = IX_text + "A"
                        pre_N = "A"
                    elif ch == "1":
                        IX_text = IX_text + "C"
                        pre_N = "C"
                    elif ch == "2":
                        IX_text = IX_text + "G"
                        pre_N = "G"
                    else:
                        IX_text = IX_text + "X"
                        pre_N = "A"

            self.Fs['F'+str(t)] = self.Fs['F'+str(t)] + IX_text


    # 頭と後ろに塩基つける
    def FForm(self):
        for i in range(len(self.Fs)):

            # 頭に塩基
            if self.Fs['F'+str(i)][0] == 'A':
                self.Fs['F'+str(i)] = 'T' + self.Fs['F'+str(i)]
            elif self.Fs['F'+str(i)] == 'T':
                self.Fs['F' + str(i)] = 'A' + self.Fs['F'+str(i)]
            else:
                self.Fs['F' + str(i)] = random.choice(['A', 'T']) + self.Fs['F'+str(i)]

            # 後ろに塩基
            if self.Fs['F'+str(i)][len(self.Fs['F'+str(i)])-1] == 'G':
                self.Fs['F' + str(i)] = self.Fs['F'+str(i)] + 'C'
            elif self.Fs['F'+str(i)][len(self.Fs['F'+str(i)])-1] == 'C':
                self.Fs['F' + str(i)] = self.Fs['F'+str(i)] + 'G'
            else:
                self.Fs['F' + str(i)] = self.Fs['F'+str(i)] + random.choice(['G', 'C'])

        print('\n最終的なput塩基配列')
        print(self.Fs)

        # 外に吐き出し
        # 一旦消去してから
        open(self.inputfilename + '-GoldmanM.fasta', 'w').write('>goldman method ' + self.inputfilename+'\n')
        for i in range(len(self.Fs)):
            open(self.inputfilename + '-GoldmanM.fasta', 'a').write(self.Fs['F'+str(i)]+'\n')

        filesize = os.path.getsize(self.inputfilename)

        fin_length = 0
        for i in range(len(self.Fs)):
            fin_length = fin_length + len(self.Fs['F'+str(i)])
        self.putnt = fin_length

        self.filesize = approximate_size(filesize)

        # dence = ファイルサイズ(bits=byte?) / ヌクレオチドの長さ
        self.density = (filesize * 8) / fin_length


    def decode(self, filename):
        IXs = []
        IDs = []
        i3s = []
        indexs = []
        Parities = []
        Pexpecteds = []
        s5 = ''
        TopEnd = []
        print("\n DECODE ...")

        f = open(filename, 'r')
        line2 = f.read()
        Fs = line2.split('\n')
        Fs.pop()

        for i in range(len(Fs)):
            TopEnd.append((Fs[i][0]))
            TopEnd.append((Fs[i][-1]))
            Fs[i] = Fs[i][1:-1]

        for i in range(len(Fs)):
            IXs.append(Fs[i][-15:])
            Fs[i] = Fs[i][:-15]

        # IXsをtritsに
        for i in range(len(IXs)):
            IXs[i] = r_rotate(IXs[i], Fs[i][-1:])

        # Extract ID
        for i in range(len(IXs)):
            IDs.append(IXs[i][:2])

        # extract i3 and i
        for i in range(len(IXs)):
            i3s.append(IXs[i][2:len(IXs[i]) - 1])
        for i in range(len(i3s)):
            indexs.append(Base_n_to_10(i3s[i], 3))

        #checksum error
        for i in range(len(IXs)):
            Parities.append(IXs[i][-1])

        for i in range(len(IDs)):
            p = int(IDs[i][0])

            for t in range(1, 13):
                if t % 2 == 1:
                    p = p + int(i3s[i][t-1])
                    p = p % 3

            Pexpecteds.append(str(p))

        # ランダマイズをとく
        reR(Fs)

        # IXパリティに従ってエラーをはく
        for p in range(len(Parities)):
            if Parities[p] != Pexpecteds[p]:
                print("Corrupted segment: \nID = %s\ni = %d" %(IDs[p], indexs[p]))
            else:
                if p % 2 == 1:
                    Fs[p] = reverse_complement(Fs[p])

        # Fi to S5
        for_ol_list = []
        for i in range(len(Fs)):
            t = []
            t.append(Fs[i][0:25])
            t.append(Fs[i][25:50])
            t.append(Fs[i][50:75])
            t.append(Fs[i][75:100])
            for_ol_list.append(t)

        s5 = checkOL(for_ol_list)

        # s5 to s4
        s4 = r_rotate(s5, 'A')

        # s4 to s0
        s2 = s4[0:25]

        n = Base_n_to_10(s2, 3)
        s1 = s4[25:25+n]

        #print('s1 : ' + str(s1))
        inverted_code = dict([v,k] for k,v in self.code.items())
        s0 = ''
        i = 0

        while i != n:
            if s1[i:i + 5] in inverted_code.keys():
                s0 = s0 + ''.join('%02x' % int(inverted_code[s1[i:i + 5]]))
                i = i + 5
            else:
                s0 = s0 + ''.join('%02x' % int(inverted_code[s1[i:i + 6]]))
                i = i + 6

        open(filename + '-GoldmanM.decoded', 'wb').write(binascii.unhexlify(s0))

        print('\nDecode success!')




if __name__ == "__main__":

    input_file = sys.argv[1]

    encoder = Gld_encode()

    # エンコードするファイル指定する
    encoder.read_in_file(input_file)

    # 上で生成されたS1からS4まで生成
    encoder.makeS4()

    # ローテーションマッピングでS5生成
    encoder.rotation()

    # 切り分け
    encoder.makeFs()

    # IDをつける
    encoder.addID()

    # ひっくり返して、ほさに
    encoder.r_and_complement()

    # ランダマイズは省略
    #encoder.randomize()

    # 付属させるIXを生成
    encoder.computeP_IX()

    #頭と後ろに一個ずつ塩基
    encoder.FForm()

    #引数に塩基配列リスとを貰ってdeコード
    #encoder.decode(input_file+"-GoldmanM.dna")

