import random
import csv
import binascii
import os.path
import sys
import PyMyLib

# 参考github https://github.com/allanino/DNA/blob/master/dna/dna.py
# 自環境向けに改編

# Goldman Encoding
class Goldman_method:

    # ハフマン符号表
    code ={}
    # 3進数対応表
    files_trits = {}

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
        # アルゴリズムの品質を図る尺度
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
        trit = PyMyLib.base10_to_base3(len(self.files_trits))
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
        trits = PyMyLib.base10to(self.n, 3)
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

        # 簡易化のため固定
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
            a = PyMyLib.base10to(t, 3)
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
        with open(self.inputfilename + '-GoldmanM.dna', 'w') as fw:
            pass
        # シーケンサーシミュレート用ファイル作成
        for i in range(len(self.Fs)):
            open(self.inputfilename + '-GoldmanM.fasta', 'a').write(self.Fs['F'+str(i)]+'\n')
        # シーケンサーシミュレート用ファイル作成
        for i in range(len(self.Fs)):
            open(self.inputfilename + '-GoldmanM.dna', 'a').write(self.Fs['F'+str(i)]+'\n')

        filesize = os.path.getsize(self.inputfilename)

        fin_length = 0
        for i in range(len(self.Fs)):
            fin_length = fin_length + len(self.Fs['F'+str(i)])
        self.putnt = fin_length

        self.filesize = PyMyLib.approximate_size(filesize)

        # dence = ファイルサイズ(bits=byte?) / ヌクレオチドの長さ
        self.density = (filesize * 8) / fin_length


    def decode(self, filename):
            IXs = []
            IDs = []
            i3s = []
            Fs = []
            indexs = []
            Parities = []
            Pexpecteds = []
            s5 = ''
            TopEnd = []
            print("\n DECODE ...")
    
            f = open(filename, 'r')
            line2 = f.read()
            Fasta = line2.split('\n')
            Fasta.pop(0)
            Fasta.pop()
    
            text = ''
            for line in Fasta:
                text = text + line
            for i in range(0, len(text), 117):
                Fs.append(text[i:i+117])
    
            print("\n 117 to 115 nt")
            for i in range(len(Fs)):
                TopEnd.append((Fs[i][0]))
                TopEnd.append((Fs[i][-1]))
                Fs[i] = Fs[i][1:-1]
    
            for i in range(len(Fs)):
                IXs.append(Fs[i][-15:])
                Fs[i] = Fs[i][:-15]
    
            # IXsをtritsに
            for i in range(len(IXs)):
                IXs[i] = PyMyLib.r_rotate(IXs[i], Fs[i][-1:])
    
            # Extract ID
            for i in range(len(IXs)):
                IDs.append(IXs[i][:2])
    
            # extract i3 and i
            for i in range(len(IXs)):
                i3s.append(IXs[i][2:len(IXs[i]) - 1])
            for i in range(len(i3s)):
                if len(i3s[i]):
                    indexs.append(PyMyLib.base3_to_base10(i3s[i]))
    
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
            #reR(Fs)
    
            # IXパリティに従ってエラーをはく
            for p in range(len(Parities)):
                if Parities[p] != Pexpecteds[p]:
                    print("Corrupted segment: \nID = %s\ni = %d" % (IDs[p], indexs[p]))
                else:
                    if p % 2 == 1:
                        print('')
    
            for i in range(len(Fs)):
                if i % 2 == 1:
                    Fs[i] = PyMyLib.reverse_complement(Fs[i])
    
            # Fi to S5
            for_ol_list = []
            print('Fs')
            print(Fs)
            for i in range(len(Fs)):
                t = []
    
                a = Fs[i][0:25]
                t.append(a)
    
                a = Fs[i][25:50]
                t.append(a)
    
                a = Fs[i][50:75]
                t.append(a)
    
                a = Fs[i][75:100]
                t.append(a)
    
                for_ol_list.append(t)
            s5 = PyMyLib.checkOL(for_ol_list)
    
            # s5 to s4
            s4 = PyMyLib.r_rotate(s5, 'A')
    
            # s4 to s0
            s2 = s4[0:25]
    
            n = PyMyLib.Base_n_to_10(s2, 3)
            s1 = s4[25:25+n]
    
            inverted_code = dict([v,k] for k,v in self.code.items())
            s0 = ''
            i = 0
    
            # reliability比較用のS1出力
            with open(filename+'-decode_s1.txt', 'w') as f:
                f.write(s1)
    
            while i != n:
                if s1[i:i + 5] in inverted_code.keys():
                    s0 = s0 + ''.join('%02x' % int(inverted_code[s1[i:i + 5]]))
                    i = i + 5
                else:
                    s0 = s0 + ''.join('%02x' % int(inverted_code[s1[i:i + 6]]))
                    i = i + 6
    
            open(filename + '.decoded', 'wb').write(binascii.unhexlify(s0))
    
            print('\nDecode success!')


if __name__ == "__main__":

    input_file = sys.argv[1]
    mode = sys.argv[2]

    Gm = Goldman_method()
    if mode == "encode":

    
        # エンコードするファイル指定する
        Gm.read_in_file(input_file)
    
        # 上で生成されたS1からS4まで生成
        Gm.makeS4()
    
        # ローテーションマッピングでS5生成
        Gm.rotation()
    
        # 切り分け
        Gm.makeFs()
    
        # IDをつける
        Gm.addID()
    
        # ひっくり返して、補鎖に
        Gm.r_and_complement()
    
        # ランダマイズは省略, 本実験ではオーバヘッドが大きいため
        #encoder.randomize()
    
        # 付属させるIXを生成
        Gm.computeP_IX()
    
        #頭と後ろに一個ずつ塩基
        Gm.FForm()

    elif mode == "decode":
        #引数に塩基配列リストを貰ってdeコード
        #本来はシーケンサーをシミュレートしてエラーを付与する
        #Gm.decode(input_file+"-GoldmanM.dna")
        pass
        
    else:
        print("modeを指定してください.")
