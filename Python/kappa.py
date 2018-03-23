#!/usr/bin/python
#-*- coding: utf-8 -*-
"""
Receive a file having an evaluator by subject matrix, such as:
      s1 s2 s3 s4 (subjects)
ev1:  1  2  3  4
ev2:  1  3  3  5  (votes)
ev3:  1  2  2  2
"""

from os.path import join
from codecs import open
from collections import Counter

HOME='/home/roger/Desktop/sort/'

def fleiss():
    subjects = ['0', '1', '2', '3', '4']
    #subjects = ['1', '2', '3', '4', '5']
    dic = {}
    greatest = 0.00
    smallest = 1.00
    fout = open(join(HOME, 'fileout.txt'), 'w', 'utf-8')
    with open(join(HOME, 'filein.txt'), 'r', 'utf-8') as fin:
        for n, line in enumerate(fin):
            arr = line.strip().split()
            dic[n] = Counter(arr)
    
    for n in range(0, len(dic)):
        counter = dic[n]
        values = ''
        for subj in subjects:
            values += str(counter[subj])+' '
        fout.write('%s\n' % values[0:-1])
    fout.close()

def cohens():
    dic = {}
    greatest = 0.00
    smallest = 1.00
    fout = open(join(HOME, 'fileout.txt'), 'w', 'utf-8')
    with open(join(HOME, 'filein.txt'), 'r', 'utf-8') as fin:
        for n, line in enumerate(fin):
            dic[n] = line.strip().split()
    for n1 in range(0,len(dic)):
        ev1 = dic[n1]
        values = ''
        for n2 in range(0,len(dic)):
            if False: #n1 > n2:
                values += ' '
            else:
                r00 = 0
                r01 = 0
                r02 = 0
                r03 = 0
                r04 = 0
                r10 = 0
                r11 = 0
                r12 = 0
                r13 = 0
                r14 = 0
                r20 = 0
                r21 = 0
                r22 = 0
                r23 = 0
                r24 = 0
                r30 = 0
                r31 = 0
                r32 = 0
                r33 = 0
                r34 = 0
                r40 = 0
                r41 = 0
                r42 = 0
                r43 = 0
                r44 = 0
                ev2 = dic[n2]
                for n3 in range(0,len(dic[n2])):
                    ev1[n3] = int(ev1[n3])
                    ev2[n3] = int(ev2[n3])
                    if ev1[n3] == 0 and ev2[n3] == 0:
                        r00 += 1
                    if ev1[n3] == 0 and ev2[n3] == 1:
                        r01 += 1
                    if ev1[n3] == 0 and ev2[n3] == 2:
                        r02 += 1
                    if ev1[n3] == 0 and ev2[n3] == 3:
                        r03 += 1
                    if ev1[n3] == 0 and ev2[n3] == 4:
                        r04 += 1
                    if ev1[n3] == 1 and ev2[n3] == 0:
                        r10 += 1
                    if ev1[n3] == 1 and ev2[n3] == 1:
                        r11 += 1
                    if ev1[n3] == 1 and ev2[n3] == 2:
                        r12 += 1
                    if ev1[n3] == 1 and ev2[n3] == 3:
                        r13 += 1
                    if ev1[n3] == 1 and ev2[n3] == 4:
                        r14 += 1
                    if ev1[n3] == 2 and ev2[n3] == 0:
                        r20 += 1
                    if ev1[n3] == 2 and ev2[n3] == 1:
                        r21 += 1
                    if ev1[n3] == 2 and ev2[n3] == 2:
                        r22 += 1
                    if ev1[n3] == 2 and ev2[n3] == 3:
                        r23 += 1
                    if ev1[n3] == 2 and ev2[n3] == 4:
                        r24 += 1
                    if ev1[n3] == 3 and ev2[n3] == 0:
                        r30 += 1
                    if ev1[n3] == 3 and ev2[n3] == 1:
                        r31 += 1
                    if ev1[n3] == 3 and ev2[n3] == 2:
                        r32 += 1
                    if ev1[n3] == 3 and ev2[n3] == 3:
                        r33 += 1
                    if ev1[n3] == 3 and ev2[n3] == 4:
                        r34 += 1
                    if ev1[n3] == 4 and ev2[n3] == 0:
                        r40 += 1
                    if ev1[n3] == 4 and ev2[n3] == 1:
                        r41 += 1
                    if ev1[n3] == 4 and ev2[n3] == 2:
                        r42 += 1
                    if ev1[n3] == 4 and ev2[n3] == 3:
                        r43 += 1
                    if ev1[n3] == 4 and ev2[n3] == 4:
                        r44 += 1

                # Totals
                tr0 = r00 + r01 + r02 + r03 + r04
                tr1 = r10 + r11 + r12 + r13 + r14
                tr2 = r20 + r21 + r22 + r23 + r24
                tr3 = r30 + r31 + r32 + r33 + r34
                tr4 = r40 + r41 + r42 + r43 + r44 

                tc0 = r00 + r10 + r20 + r30 + r40
                tc1 = r01 + r11 + r21 + r31 + r41
                tc2 = r02 + r12 + r22 + r32 + r42
                tc3 = r03 + r13 + r23 + r33 + r43
                tc4 = r04 + r14 + r24 + r34 + r44

                ttl = tr0 + tr1 + tr2 + tr3 + tr4

                # Agreements
                tag = r00 + r11 + r22 + r33 + r44

                # By chance
                bc0 = float(tc0 * tr0) / ttl
                bc1 = float(tc1 * tr1) / ttl
                bc2 = float(tc2 * tr2) / ttl
                bc3 = float(tc3 * tr3) / ttl
                bc4 = float(tc4 * tr4) / ttl

                tbc = bc0 + bc1 + bc2 + bc3 + bc4

                # Cohen's Kappa
                kappa = (tag - tbc) / (ttl - tbc)

                #Complete table
                """
                print r00,r01,r02,r03,r04,tr0
                print r10,r11,r12,r13,r14,tr1
                print r20,r21,r22,r23,r24,tr2
                print r30,r31,r32,r33,r34,tr3
                print r40,r41,r42,r43,r44,tr4
                print tc0,tc1,tc2,tc3,tc4,
                print tr0+tr1+tr2+tr3+tr4
                print ''
                print r00,r11,r22,r33,r44,tag
                print "%.2f %.2f %.2f %.2f %.2f %.2f" % (bc0,bc1,bc2,bc3,bc4,tbc)
                print ''
                print 'kappa: %.2f' % kappa
                """
                kappastr = '%.2f' % kappa
                if kappa > greatest and kappa != 1.00:
                    greatest = kappa
                if kappa < smallest:
                    smallest = kappa
                values += '%s ' % str(kappastr)
        fout.write('%s\n' % values)

    fout.write('\ngreatest: %s\nsmallest: %s\n' % (greatest, smallest))            
    fout.close()

if __name__ == "__main__":
	fleiss()
