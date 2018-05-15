#!/usr/bin/python
#-*- coding: utf-8 -*-

import argparse

def main(inputfile):
    content = '| '
    drop = False
    lr, v1, v2, v3, v4, v5 = '', '', '', '', '', ''
    
    with open(inputfile) as fin:
        for line in fin:
            line = line.strip()
            if drop:
                arr = line.split('&')
                for  i in range(len(arr)):
                    v = arr[i]
                    v = v.replace('\\', '')
                    v = v.replace('textbf{', '')
                    v = v.replace('}', '')
                    arr[i] = v.strip()
                
                if len(arr) == 6:
                    _, t1, t2, t3, t4, t5 = arr
                elif len(arr) == 7:
                    _, _, t1, t2, t3, t4, t5 = arr
                lr += t1+'<br>'
                v1 += t2+'<br>'
                v2 += t3+'<br>'
                v3 += t4+'<br>'
                v4 += t5+'<br>'
            if '&\multirow' in line:
                content += (line.split('{')[3]).split('}')[0]
                content += '    | '
                drop = True

    content += lr[:-4]+' | '+v1[:-4]+' | '+v2[:-4]+' | '+v3[:-4]+' | '+v4[:-4]+' |'
    print content
               


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfile', metavar='file_input', help='File containing paths to images and true labels')
    args = parser.parse_args()

    main(args.inputfile)
