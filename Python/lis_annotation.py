#!/usr/bin/env python
# coding: utf-8
import sys
import argparse
from os.path import join, dirname
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def fix_boxes(x, y, w, h, valx=0, valy=0, mode=None):
    """ Fix bounding box coordinates when they are out of the image """
    x, y, w, h = map(int, (x, y, w, h))
    if x < valx: 
        w += x
        x = 0
    if y < valy:
        h += y
        y = 0
    if mode == 'person':
        if y != 0: y = 0
        if y+h < 120: h = 114
    if x+w > 257: w = 257-x
    if y+h > 257: h = 257-y
    return x, y, w, h


def fix_bbox_file(input, output=None):
    if not output:
        output = join(dirname(input), 'fixed_bboxes.txt')

    with open(input) as fin, open(output, 'w') as fout:
        for i, line in enumerate(fin):
            if i == 0 or line.startswith('---') or line.startswith('Modified'):
                fout.write(line)
                continue #header
            # 86 \t person \t (0,51,49,64) \t 0 \t /home/roger/KSCGR/data1/boild-egg/rgb256/86.jpg
            arr = line.strip().split('\t')
            if not arr[2].startswith('(-,'):
                x, y, w, h = eval(arr[2])
                x, y, w, h = fix_boxes(x, y, w, h, valx=0, valy=0)
                fout.write('%s\t%s\t(%d,%d,%d,%d)\t%s\t%s\n' % (arr[0], arr[1], x, y, w, h, arr[3], arr[4]))
            else:
                fout.write(line)


def load_dic_file(input):
    """ Return dictionaries for bounding boxes to keep and bounding boxes to delete """
    with open(input) as fin:
        dkeep = {}
        dremove = {}
        for i, line in enumerate(fin):
            arr  =line.strip().split(';')
            id = int(arr[0][:-1])
            operation = arr[0][-1]
            idframes = arr[1].split(',')
            
            last = -1
            for pair in idframes:
                ids = map(int, pair.split('-'))
                if len(ids) != 2:
                    logger.error('Pair of frames is not correct: {} [LINE: {}]'.format(ids, i))
                    sys.exit(0)
                id_start, id_end = ids
                if id_start > id_end:
                    logger.error('Start frame is greater than end frame: ({} : {}) [LINE: {}]'.format(ids[0], ids[1], i))
                    sys.exit(0)
                if id_start >= last:
                    last = id_end
                else:
                    logger.error('Start frame is lesser than the previous frame: {} - {}'.format(id_end, last))
                    sys.exit(0)
                if operation == '+':
                    if dkeep.has_key(id):
                        dkeep[id]['start'].append(id_start)
                        dkeep[id]['end'].append(id_end)
                    else:
                        dkeep[id] = {'record': False, 'data': None, 'start': [id_start], 'end': [id_end]}
                elif operation == '-':
                    if dremove.has_key(id):
                        dremove[id].append((id_start, id_end))
                    else:
                        dremove[id] = [(id_start, id_end)]
                else:
                    logger.error('There is not an operation: {}  [LINE: {}]'.format(operation, i))
                    sys.exit(0)
    return dkeep, dremove


def coordinates_objects(file_input, file_frames, output=None):
    if not output:
        output = join(dirname(file_input), 'person_norm.txt')

    dobj, drem = load_dic_file(file_frames)
    for k in drem: print k, drem[k]
    last_idfr = -1
    recorded_idfr = False
    with open(file_input) as fin, open(output, 'w') as fout:
        for i, line in enumerate(fin):
            if i == 0 or line.startswith('---') or line.startswith('Modified'):
                fout.write(line)
                continue #header
            # 86 \t person \t (0,51,49,64) \t 0 \t /home/roger/KSCGR/data1/boild-egg/rgb256/86.jpg
            arr = line.strip().split('\t')
            idfr = int(arr[0])
            if idfr != last_idfr:
                if idfr > 0 and not recorded_idfr:
                    last_path = join(dirname(arr[4]), str(last_idfr)+'.jpg')
                    fout.write('%d\tNone\t(-,-,-,-)\tNone\t%s\n' % (last_idfr, last_path))
                last_idfr = idfr
                recorded_idfr = False
            if not arr[2].startswith('(-,'):
                obj = arr[1]
                x, y, w, h = eval(arr[2])
                x, y, w, h = fix_boxes(x, y, w, h, valx=0, valy=0, mode=obj)
                idobj = int(arr[3])

                if drem.has_key(idobj):
                    remove = False
                    for j in range(len(drem[idobj])):
                        id_start, id_end = drem[idobj][j]
                        if idfr >= id_start and idfr <= id_end:
                            remove = True
                    if remove: continue
                #if idfr == 1952:
                #    print '\n',idobj, drem[idobj]
                if not dobj.has_key(idobj):
                    #print('Dictionary does not contain object: {} - {}'.format(obj, idfr))
                    logger.debug('Dictionary does not contain object: {}'.format(obj))
                    fout.write('%d\t%s\t(%d,%d,%d,%d)\t%s\t%s\n' % (idfr, arr[1], x, y, w, h, arr[3], arr[4]))
                else:
                    if idfr in dobj[idobj]['start']:
                        dobj[idobj]['record'] = True
                        dobj[idobj]['data'] = (x, y, w, h)

                    if dobj[idobj]['record']:
                        stored_x, stored_y, stored_w, stored_h = dobj[idobj]['data']
                        fout.write('%d\t%s\t(%d,%d,%d,%d)\t%s\t%s\n' % (idfr, arr[1], stored_x, stored_y, stored_w, stored_h, arr[3], arr[4]))
                    else:
                        fout.write('%d\t%s\t(%d,%d,%d,%d)\t%s\t%s\n' % (idfr, arr[1], x, y, w, h, arr[3], arr[4]))
                    recorded_idfr = True
                    if idfr in dobj[idobj]['end']:
                        dobj[idobj]['record'] = False
                        dobj[idobj]['data'] = None
            else:
                fout.write(line)


def remove_negative_file(input, output=None):
    if not output:
        output = join(dirname(input), 'bbox_nonneg.txt')

    with open(input) as fin, open(output, 'w') as fout:
        for i, line in enumerate(fin):
            if i == 0 or line.startswith('---') or line.startswith('Modified'):
                fout.write(line)
                continue #header
            # 86 \t person \t (0,51,49,64) \t 0 \t /home/roger/KSCGR/data1/boild-egg/rgb256/86.jpg
            arr = line.strip().split('\t')
            id = int(arr[0])
            if not arr[2].startswith('(-,'):
                x, y, w, h = eval(arr[2])
                #vals = (0,0,140,135)
                if x < 0: x = 0
                if y < 0: y = 0
                if x+w > 256: w = 256-x
                if y+h > 256: h = 256-y
                fout.write('%d\t%s\t(%d,%d,%d,%d)\t0\t%s\n' % (id, arr[1], x, y, w, h, arr[4]))
            else:
                fout.write(line)


def generate_relations(input, output=None):
    """ Create file containing relations. Input file has the form:
        idfr_start-idfr_end-id_obj1-id_relation-id_obj2
    """
    if not output:
        output = join(dirname(input), 'relations.txt')
    do = {
        0: 'person',
        1: 'bowl',
        2: 'ham',
        3: 'egg',
        4: 'knife',
        5: 'cutting board',
        6: 'oil bottle',
        7: 'frying pan',
        8: 'hashi',
        9: 'saltshaker',
        10: 'spoon',
        11: 'glass',
        12: 'egg ham',
        13: 'pan lid',
        14: 'turner',
        15: 'plate',
        16: 'beaten egg',
        17: 'egg crepe',
        18: 'boild egg',
        19: 'pan handler',
        20: 'pan',
        21: 'ham egg',
        22: 'milk carton',
        23: 'omelette'
    }
    dr = {
        0: 'hold',
        1: 'in',
        2: 'on',
        3: 'cut',
        4: 'move'
    }

    relations = []
    max_fr = 0
    with open(input) as fin:
        for i, line in enumerate(fin):
            arr = map(int, line.strip().split('-'))
            start, end, o1, r, o2 = arr
            if start >= end:
                logger.error('Start is greater than end frame: {} - {} [LINE: {}]'.format(start, end, i))
                sys.exit(0)
            relations.append((start, end, o1, r, o2))
            if end > max_fr:
                max_fr = end
    max_fr += 1

    with open(output, 'w') as fout:
        # header
        fout.write('Frame\tSubject\tRelation\tObject\n')
        for idfr in range(max_fr):
            recorded = False
            for start, end, o1, r, o2 in relations:
                if idfr >= start and idfr <= end:
                    fout.write('%d\t%s\t%s\t%s\n' % (idfr, do[o1], dr[r], do[o2]))
                    recorded = True
            if not recorded:
                fout.write('%d\tNone\tNone\tNone\n' % idfr)


def merge_objects_person(input_object, input_person, output=None):
    if not output:
        output = join(dirname(input_object), 'person_objects.txt')
    d, dids = {}, {}
    with open(input_object) as fo:
        for line in fo:
            if line.startswith('Frame') or line.startswith('---') or line.startswith('Modified'):
                continue #header
            # 86 \t person \t (0,51,49,64) \t 0 \t /home/roger/KSCGR/data1/boild-egg/rgb256/86.jpg
            arr = line.strip().split('\t')
            dids[int(arr[3])] = arr[1]
            if d.has_key(int(arr[0])):
                d[int(arr[0])].append(line)
            else:
                d[int(arr[0])] = [line]

    id_person = max(dids.keys())+1
    print dids.keys()

    with open(input_person) as fp, open(output, 'w') as fout:
        for line in fp:
            if line.startswith('Frame') or line.startswith('---') or line.startswith('Modified'):
                fout.write(line)
                continue #header
            arr = line.strip().split('\t')
            id = int(arr[0])
            recorded = False
            if d.has_key(id):
                recorded = True
                for l in d[id]:
                    fout.write(l)
            if not arr[2].startswith('(-,'):
                fout.write('%d\tperson\t%s\t%d\t%s\n' % (id, arr[2], id_person, arr[4]))
                recorded = True
            if not recorded:
                fout.write(line)


def change_name_object(input, output=None):
    # Remove this function
    if not output:
        output = join(dirname(input), 'object_beaten.txt')

    with open(input) as fin, open(output, 'w') as fout:
        for i, line in enumerate(fin):
            if i == 0 or line.startswith('---') or line.startswith('Modified'):
                fout.write(line)
                continue #header
            # 86 \t person \t (0,51,49,64) \t 0 \t /home/roger/KSCGR/data1/boild-egg/rgb256/86.jpg

            arr = line.strip().split('\t')
            idfr = int(arr[0])
            if not arr[2].startswith('(-,'):
                idobj = int(arr[3])
                obj = arr[1]

                if obj == 'egg' and idfr >= 3757:
                    fout.write('%d\tbeaten egg\t(65,126,33,25)\t14\t%s\n' % (idfr, arr[4]))
                elif obj == 'omelette' and idfr <= 5060:
                    fout.write('%d\tbeaten egg\t%s\t14\t%s\n' % (idfr, arr[2], arr[4]))
                else:
                    fout.write(line)
            else:
                fout.write(line)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_1', metavar='input_object', help='Plain text file')
    #parser.add_argument('input_2', metavar='input_person', help='Plain text file')
    args = parser.parse_args()
    
    #fix_bbox_file(args.input_1)
    #coordinates_objects(args.input_1, args.input_2)
    #remove_negative_file(args.input_1)
    generate_relations(args.input_1)
    #merge_objects_person(args.input_1, args.input_2)
    #change_name_object(args.input_1)
