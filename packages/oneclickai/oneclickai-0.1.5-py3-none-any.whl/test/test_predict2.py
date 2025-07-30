from oneclickai.YOLO import load_model, predict, draw_result
import cv2
import numpy as np

model = load_model("YOLO_coco")

# image path
image = cv2.imread('./test/test5.jpg')/255.0

# coco dataset cls names
coco_cls_names = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat',
                'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog',
                'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella',
                'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat',
                'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork',
                'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog',
                'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv',
                'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink',
                'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']



result_annotation = predict(model, image, conf=0.4)
result_image = draw_result(np.array(image), result_annotation, class_names = coco_cls_names)
cv2.imshow('image', result_image)


# Close the window when 'Esc' is pressed
if cv2.waitKey(0) & 0xFF == 27:
    cv2.destroyAllWindows()

