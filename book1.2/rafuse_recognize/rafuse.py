import numpy as np
import os, sys
sys.path.append('textcnn')
from .textcnn.predict import RefuseClassification
from .classify_image import *


class RafuseRecognize():
    
    def __init__(self):
        
        self.refuse_classification = RefuseClassification()
        self.init_classify_image_model()
        self.node_lookup = NodeLookup(uid_chinese_lookup_path='data/imagenet_2012_challenge_label_chinese_map.pbtxt',
                                model_dir = '/tmp/imagenet')
        
        
    def init_classify_image_model(self):
        
        create_graph('/tmp/imagenet')

        self.sess = tf.Session()
        self.softmax_tensor = self.sess.graph.get_tensor_by_name('softmax:0')
        
        
    def recognize_image(self, image_data):
        
        predictions = self.sess.run(self.softmax_tensor,
                               {'DecodeJpeg/contents:0': image_data})
        predictions = np.squeeze(predictions)

        top_k = predictions.argsort()[-5:][::-1]
        result_list = []
        kind=''
        max = 0
        name = ''
        for node_id in top_k:
            human_string = self.node_lookup.id_to_string(node_id)
            score = predictions[node_id]
            print(score)
            #print(human_string)
            human_string = ''.join(list(set(human_string.replace('，', ',').split(','))))
            #print(human_string)
            classification = self.refuse_classification.predict(human_string)
            result_list.append('%s  =>  %s' % (human_string, classification))
            if score > max:
                name = human_string
                max = score
                kind=classification
        return_word = [kind,name]
        return return_word
        

def main(word):
    test = RafuseRecognize()
    image_data = tf.gfile.FastGFile(word, 'rb').read()
    res = test.recognize_image(image_data)
    print(res)