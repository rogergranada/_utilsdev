#!/usr/bin/python
#-*- coding: utf-8 -*-

import os
from codecs import open
import sh

def main():
    with open('/home/roger/Desktop/EN_PT/ex.txt', 'r', 'utf-8') as fin:
        with open('/home/roger/Desktop/EN_PT/en_pt.txt', 'w', 'utf-8') as fout:
            fin.next()
            for line in fin:
                _, id1, id2 = line.strip().split()
                fout.write(id1+'::'+id2+'\n')

"""
def main():
    path = '/home/roger/Desktop/SEEDS/done'
    for (path, dirs, files) in os.walk(path):
        for pasta in dirs:
            command = 'python tfwiki.py -lin1 pt -lin2 fr -c 1 dsm_corpora wikipt wikifr '+path+'/'+pasta+'/'+pasta+'.txt '+path+'/'+pasta+'/'
            os.system(command)

def main():
    path = '/home/roger/Desktop/SEEDS/out/'
    for (path, dirs, files) in os.walk(path):
        for fin in files:
            if not fin.endswith('~'):
                fin = fin.replace('docs','')
                fin = fin.replace('.txt','')
                command = 'mkdir /home/roger/Desktop/SEEDS/out/out/'+fin
                os.system(command)
                datain = open('/home/roger/Desktop/SEEDS/out/docs'+fin+'.txt', 'r', 'utf-8')
                dataout = open('/home/roger/Desktop/SEEDS/out/out/'+fin+'/'+fin+'.txt', 'w', 'utf-8')
                for line in datain:
                    id1, id2 = line.strip().split()
                    dataout.write(id1+'::'+id2+'\n')
                datain.close()
                dataout.close()

    #for line in files:
    #    print line

def main():
    lista = open('/home/roger/Desktop/HDRoger_pdf.txt', 'r', 'utf-8')
    papers = open('/home/roger/Desktop/Rep.txt', 'r', 'utf-8')
    #out = open('/home/roger/Desktop/Diff.txt', 'w', 'utf-8')
    docs = {}
    for linha in papers:
        docs[linha.strip()] = linha.strip()

    for line in lista:
        line = line.encode('utf-8')
        if docs.has_key(line.strip()):
            print line.strip()
            sh.rm('"/media/roger/Musics/HDRoger/pdf/'+line.strip()+'"')

    lista.close()
    papers.close()
    #out.close()

def main():
    lista = open('/home/roger/Workspace/cl_dsm/src/test/Goodenough_list.txt', 'r', 'utf-8')
    por = open('/home/roger/Desktop/por.txt', 'r', 'utf-8')
    en_pt = open('/home/roger/Desktop/Terms_en_pt.txt', 'w', 'utf-8')
    pt_fr = open('/home/roger/Desktop/Terms_pt_fr.txt', 'w', 'utf-8')
    terms = []
    for linha in por:
        t1, t2 = linha.strip().split(' - ')
        terms.append(t1)
        terms.append(t2)
    n = 0
    for line in lista:
        if not line.startswith('#'):
            termen, temp, _ = line.split('\t')
            termfr = temp.split()[0]
            en_pt.write(termen+'\t'+terms[n]+'\n')
            pt_fr.write(terms[n]+'\t'+termfr+'\n')
            n += 1
"""            

if __name__ == "__main__":
    main()
