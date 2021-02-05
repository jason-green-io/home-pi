#!/usr/bin/env python3
from collections import defaultdict
import qrcode
import sys

a = [[0, 1, 1, 1, 0, 1, 0],
     [1, 0, 0, 0, 1, 1, 0],
     [0, 1, 1, 1, 0, 1, 0],
     [0, 1, 1, 1, 0, 1, 0],
     [0, 1, 1, 1, 0, 1, 0],
     [0, 1, 1, 1, 0, 1, 0],
     [0, 1, 1, 1, 0, 1, 0]]

map = [[1,8],
       [2,16],
       [4,32],
       [64,128]]


data = "does this work? and if so, how big could I make this text? do large QRcodes still fit on the screen? .. is this text way too big?"

brailledecimal = 10240
qrdecimal = 60928

def qrunicode(data):

    code = qrcode.QRCode()

    code.add_data(data)
    code.border=1
    matrix = code.get_matrix()


    chars = defaultdict(int)

    for y, r in enumerate(matrix):
        yc, ymap = divmod(y, 4)
        ymax = yc
        for x, b in enumerate(r):
            xc, xmap = divmod(x, 2)
            xmax = xc
            if b:
                chars[yc,xc] += map[ymap][xmap]

    stringList = []

    for y in range(0, ymax + 1):
        string = ""
        for x in range(0, xmax + 1):
            string += chr(qrdecimal + chars[y, x])
        stringList.append(string) 

    return "\n".join(stringList)

if __name__ == "__main__":
    print(qrunicode(sys.argv[1]))
