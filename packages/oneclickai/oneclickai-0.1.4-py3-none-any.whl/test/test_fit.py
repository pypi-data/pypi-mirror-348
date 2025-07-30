from oneclickai.YOLO import fit_yolo_model


#% encode data
# # encode training data
# train_data_path = 'C:/Users/osy04/Desktop/image'
# train_label_path = 'C:/Users/osy04/Desktop/image'

# # # encode validation data
# val_data_path = 'C:/Users/osy04/Desktop/image'
# val_label_path = 'C:/Users/osy04/Desktop/image'


# encode training data
train_data_path = './test/yolo_dataset'
train_label_path = './test/yolo_dataset'

# # encode validation data
val_data_path = './test/yolo_dataset'
val_label_path = './test/yolo_dataset'

# fit model
fit_yolo_model(train_data_path, train_label_path, val_data_path, val_label_path, epochs=10)