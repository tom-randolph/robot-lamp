import tensorflow as tf
import cv2
import numpy as np
import time

capture = cv2.VideoCapture(0)
capture.set(3,1280)
capture.set(4,1024)
capture.set(15, -8.0)


# Path to frozen_inference_graph.pb
weightPath = 'C:\\Users\\Nate\\Anaconda3\\Lib\\site-packages\\tensorflow\\models\\research\\latestModel\\frozen_inference_graph.pb'


# Load in the model
with tf.gfile.FastGFile(weightPath) as f:
    graph_def = tf.GraphDef()
    with tf.gfile.GFile(weightPath, 'rb') as fid:
        serialized_graph = fid.read()
        graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(graph_def, name='')


with tf.Session() as sess:
    # Restore session
    sess.graph.as_default()
    tf.import_graph_def(graph_def, name='')

    while(1):

        ret, frame = capture.read()
        rows = frame.shape[0]
        cols = frame.shape[1]
        last = time.time()
        out = sess.run([sess.graph.get_tensor_by_name('num_detections:0'),
                        sess.graph.get_tensor_by_name('detection_scores:0'),
                        sess.graph.get_tensor_by_name('detection_boxes:0'),
                        sess.graph.get_tensor_by_name('detection_classes:0')],
                        feed_dict={'image_tensor:0': frame.reshape(1, frame.shape[0], frame.shape[1], 3)})
        print(time.time() - last)

        # Theres a faster way to do this but I dont feel like fixing it, bottleneck is model run
        num_detections = int(out[0][0])
        for i in range(num_detections):
            classId = int(out[3][0][i])
            score = float(out[1][0][i])
            bbox = [float(v) for v in out[2][0][i]]
            if score > 0.50:
                x = bbox[1] * cols
                y = bbox[0] * rows
                w = bbox[3] * cols - x
                h = bbox[2] * rows - y
                cv2.rectangle(frame, (int(x), int(y)), (int(x) + int(w), int(y) + int(h)), color=(255, 255, 255),thickness=2)


        cv2.imshow('hand detections', frame)
        cv2.waitKey(1)


