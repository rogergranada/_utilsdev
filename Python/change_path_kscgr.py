#!/usr/bin/python
#-*- coding: utf-8 -*-

#/usr/share/datasets/Juarez_Kitchen_Dataset/Train/data1/boild-egg-1/image_res_256_jpg/0.jpg 0
#/usr/share/datasets/ACE/data1/boild-egg

OLD_PATH = '/usr/share/datasets/Kitchen_Dataset/Train/'
NEW_PATH = '/usr/share/datasets/ACE/'
ACTIVITIES = ['boild-egg', 'ham-egg', 'kinshi-egg', 'omelette', 'scramble-egg']

"""
dic {id_data: {activity: [(img, class)]}}
dic [0]['boild-egg'] = [(0, 0), (1, 0), (2, 4), ...]
"""
dic = {}

### Extract from Train examples ###
with open('path_train_256.txt') as fin:
    print 'Extracting elements...'
    for k, line in enumerate(fin):
        path, y = line.strip().split()
        path = path.replace(OLD_PATH, '')
        arr = path.split('/')
        id_data = int((arr[0])[-1])
        activity = arr[1].replace('-'+str(id_data), '')
        id_img = int(arr[-1].replace('.jpg', ''))
        y = int(y)
        if dic.has_key(id_data):
            if dic[id_data].has_key(activity):
                dic[id_data][activity].append((id_img, y))
            else:
                dic[id_data][activity] = [(id_img, y)]
        else:
            dic[id_data] = {activity: [(id_img, y)]} 

### Extract from Test examples ###

#/usr/share/datasets/Juarez_Kitchen_Dataset/Test/data10/test_data_01/image_res_256_jpg/564.jpg 5
#/usr/share/datasets/ACE/data6/boild-egg
#OLD_PATH = '/usr/share/datasets/Juarez_Kitchen_Dataset/Test/'

print 'Extracting elements Test...'
for i in range(2):
    id_data = i+10
    for id_act in range(1,6):
        filein = 'labels/data'+str(id_data)+'_0'+str(id_act)+'.txt'
        with open(filein) as fin:
            for k, line in enumerate(fin):
                id_img, y = map(int, line.strip().split('\t'))
                if y == -1000:
                    y = 0
                activity = ACTIVITIES[id_act-1]
            
                new_id_data = i+6
                if dic.has_key(new_id_data):
                    if dic[new_id_data].has_key(activity):
                        dic[new_id_data][activity].append((id_img, y))
                    else:
                        dic[new_id_data][activity] = [(id_img, y)]
                else:
                    dic[new_id_data] = {activity: [(id_img, y)]}
        
with open('path_trainRoger.txt', 'w') as fout:
    print 'Generating file...'
    for id_data in sorted(dic):
        print 'saving data: ', id_data
        for activity in sorted(dic[id_data]):
            print '\t - saving activity: ', activity
            print '\t\t - images: ', len(dic[id_data][activity])
            for img, y in sorted(dic[id_data][activity]):
                fout.write('%sdata%d/%s/%d.jpg %d\n' % (NEW_PATH, id_data, activity, img, y))
print 'Done!'
