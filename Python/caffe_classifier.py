import numpy as np
import matplotlib.pyplot as plt

# Make sure that caffe is on the python path:
caffe_root = '../'  # this file is expected to be in {caffe_root}/examples
import sys
sys.path.insert(0, caffe_root + 'python')

import caffe

# Set the right path to your model definition file, pretrained model weights,
# and the image you would like to classify.
MODEL_FILE = '/usr/share/datasets/Trainman/Kitchen/Model/AlexNet/exp2_160610/Proto/deploy2.prototxt'
PRETRAINED = '/usr/share/datasets/Trainman/Kitchen/Model/AlexNet/exp2_160610/Snapshots/_iter_33840.caffemodel'
IMAGE_FILE = '/usr/share/datasets/Trainman/Kitchen/Data/data2/boild-egg/img256/5865.jpg'

caffe.set_mode_gpu()
net = caffe.Classifier(MODEL_FILE, PRETRAINED,
                       mean=np.asarray([129.7599,120.094,123.9113]),
                       channel_swap=(2,1,0),
                       raw_scale=255,
                       image_dims=(224, 224))
input_image = caffe.io.load_image(IMAGE_FILE)
plt.imshow(input_image)

#input_image = np.transpose([2,0,1]).reshape((1,3,224,224))
#print input_image.shape

prediction = net.predict([input_image])  # predict takes any number of images, and formats them for the Caffe net automatically
print 'prediction shape:', prediction[0].shape
plt.plot(prediction[0])
print 'predicted class:', prediction[0].argmax()
plt.show()
