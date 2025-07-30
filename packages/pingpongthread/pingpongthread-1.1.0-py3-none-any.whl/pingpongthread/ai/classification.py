import os
import datetime
import collections
import json
import numpy as np
# from tensorflow.python.framework.tensor_util import FastAppendBFloat16ArrayToTensorProto
keras = None
from ai.aiutils import AiUtils

def _process_image_path(img_path):
    img = keras.preprocessing.image.load_img(img_path, target_size=(224, 224), color_mode='rgb', interpolation='bilinear')
    img = keras.preprocessing.image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = keras.applications.mobilenet.preprocess_input(img)
    return img
def _process_image(img):
    img = keras.preprocessing.image.smart_resize(img, size=(224, 224), interpolation='bilinear')
    img = keras.preprocessing.image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = keras.applications.mobilenet.preprocess_input(img)
    return img

# mode 1: human mask classification, mode 2: others
def _get_mobilenet_model(mode):
    mobilenet_model = keras.applications.mobilenet.MobileNet(weights='imagenet') # Do not use MobileNetV2
    if mode==1:
        pass
    elif mode==2:
        conv_preds_layer_output = mobilenet_model.get_layer(name='conv_preds').output
        mobilenet_model = keras.Model(inputs=mobilenet_model.inputs, outputs=conv_preds_layer_output, name='') # Rerouted 
    else:
        raise ValueError("Undefined mode is passed.")
    return mobilenet_model
def _process_logits(logits, mode):
    if mode==1:
        logits = logits[0]
    elif mode==2:
        logits = np.transpose(np.squeeze(logits, axis=(0,1))) # res: (1000, 1)
    else:
        raise ValueError("Undefined mode is passed.")
    return logits
def _process_train_logits(logits, mode):
    if mode==1:
        pass
    elif mode==2:
        logits = np.squeeze(logits, axis=(1,2)) # res: (n, 1000)
    else:
        raise ValueError("Undefined mode is passed.")
    return logits

class Classification():
    def __init__(self, tensorflow_no_warnings=True):
        global keras
        if tensorflow_no_warnings == True:
            os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'   
        from tensorflow import keras
    
    def train_classes(self, save_model_path=None, knn_k=5, model_mode=1, *image_classes):
        def predict_train_model():
            train_arr = np.empty((0, 224, 224, 3), int)
            classes_label = []
            classes_group_len = []
            for i in range(len(image_classes)):
                train_arr = np.append(train_arr, image_classes[i].image_arr, axis=0)
                classes_label.append(image_classes[i].label)
                classes_group_len.append(len(image_classes[i].image_group_list))
                print("Class", image_classes[i].label, ":", len(image_classes[i].image_group_list), "images.")
            train_logits = _get_mobilenet_model(model_mode).predict(train_arr) 
            train_logits = _process_train_logits(train_logits, model_mode)
            model_dict = {
                "train_logits": train_logits, 
                "classes_label": classes_label, 
                "classes_group_len": classes_group_len, 
                "knn_k": knn_k,
                "model_mode": model_mode}
            print("Training done.")
            return model_dict
        if save_model_path == False or save_model_path == None:
            model_dict = predict_train_model()
        else:
            save_model_path = AiUtils.validate_file_path(save_model_path, 'json', 'model')
            model_dict = predict_train_model()
            model_dict["train_logits"] = model_dict["train_logits"].tolist()
            with open(save_model_path, 'w+') as json_file:
                json.dump(model_dict, json_file)
            print(save_model_path, "saved.")
            model_dict["train_logits"] = np.array(model_dict["train_logits"])
            model_dict["model_path"] = save_model_path
        return model_dict

    def get_classification_model(self, model_path):
        with open(model_path, "r") as model_json:
            model_dict = json.load(model_json)
        model_dict["train_logits"] = np.array(model_dict["train_logits"])
        model_dict["model_path"] = model_path
        return model_dict

    def _processed_image_prediction(self, model, processed_img):
        model_mode = model["model_mode"]
        logits = _get_mobilenet_model(model_mode).predict(processed_img)
        logits = _process_logits(logits, model_mode)
        sample_distance = np.dot(model["train_logits"], logits)
        sample_result = sorted(enumerate(sample_distance), key=lambda x: x[1])[-self._knn_k:]
        # Traning
        class_number = len(model["classes_label"])
        count = [0]*class_number
        if class_number > 2:
            for i in range(len(sample_result)):
                if sample_result[i][0] < model["classes_group_len"][0]:
                    count[0] += 1
                else:
                    j = 0
                    sum_len_af = model["classes_group_len"][0]
                    sum_len_be = sum_len_af
                    for j in range(1, class_number-1):
                        sum_len_af += model["classes_group_len"][j]
                        if sum_len_be <= sample_result[i][0] < sum_len_af:
                            count[j] += 1
                            break
                        sum_len_be = sum_len_af
                    else: 
                        count[j+1] += 1
        else:
            for i in range(len(sample_result)):
                if sample_result[i][0] < model["classes_group_len"][0]:
                    count[0] += 1
                else:
                    count[1] += 1
        score_dict = {}
        for i2 in range(class_number):
            score_dict[model["classes_label"][i2]] = count[i2]
        return score_dict

    def image_predict(self, model, image):
        processed_img = _process_image(image)
        score_dict = self._processed_image_prediction(model, processed_img)
        return score_dict

    def image_predict_path(self, model, image_path):
        processed_img = _process_image_path(image_path)
        score_dict = self._processed_image_prediction(model, processed_img)
        return score_dict

    def set_knn_k(self, model, knn_k):
        model["knn_k"] = knn_k
        return model

    class FramesPredictor():
        def __init__(self, model, timer_sec):
            if timer_sec <= 0:
                raise(ValueError("'timer_sec' muste be bigger than 0."))
            self._mobilenet_model = _get_mobilenet_model(model["model_mode"])
            self._model = model
            self._timer_sec = timer_sec
            self._class_deque = collections.deque()
            self._knn_k = model["knn_k"]

        def _processed_image_prediction(self, processed_img):
            logits = self._mobilenet_model.predict(processed_img)
            logits = _process_logits(logits, self._model["model_mode"])
            sample_distance = np.dot(self._model["train_logits"], logits)
            sample_result = sorted(enumerate(sample_distance), key=lambda x: x[1])[-self._knn_k:]
            # Traning
            class_number = len(self._model["classes_label"])
            count = [0]*class_number
            if class_number > 2:
                for i in range(len(sample_result)):
                    if sample_result[i][0] < self._model["classes_group_len"][0]:
                        count[0] += 1
                    else:
                        j = 0
                        sum_len_af = self._model["classes_group_len"][0]
                        sum_len_be = sum_len_af
                        for j in range(1, class_number-1):
                            sum_len_af += self._model["classes_group_len"][j]
                            if sum_len_be <= sample_result[i][0] < sum_len_af:
                                count[j] += 1
                                break
                            sum_len_be = sum_len_af
                        else: 
                            count[j+1] += 1
            else:
                for i in range(len(sample_result)):
                    if sample_result[i][0] < self._model["classes_group_len"][0]:
                        count[0] += 1
                    else:
                        count[1] += 1
            score_dict = {}
            for i2 in range(class_number):
                score_dict[self._model["classes_label"][i2]] = count[i2]
            return score_dict

        def image_predict_and_accum(self, image):
            processed_img = _process_image(image)
            prediction_dict = self._processed_image_prediction(processed_img)
            now = datetime.datetime.now()
            if len(self._class_deque) > 0 and now - self._class_deque[0][0] > datetime.timedelta(seconds=self._timer_sec):
                self._class_deque.popleft()
            max_class = max(prediction_dict, key=prediction_dict.get)
            self._class_deque.append((now, max_class))
            return prediction_dict
        
        def accum_predict(self):
            if len(self._class_deque) == 0:
                return None
            elif datetime.datetime.now() - self._class_deque[0][0] < datetime.timedelta(seconds=self._timer_sec):
                return None
            else:
                winner_list = []
                for t, v in self._class_deque:
                    winner_list.append(v)
                sum = len(winner_list)
                class_counter = dict(collections.Counter(winner_list))
                for key in class_counter.keys():
                    class_counter[key] = class_counter[key]/sum
                return class_counter

        def set_knn_k(self, knn_k):
            self._model["knn_k"] = knn_k
            self._knn_k = knn_k

        def clear_accum(self):
            self._class_deque = collections.deque()

    class ImageClass():
        def __init__(self, label, image_folder_path):
            self.label = label
            image_folder_path = AiUtils.validate_folder_path(image_folder_path, False)
            self.image_folder_path = image_folder_path
            self.image_group_list = os.listdir(image_folder_path)
            self.image_arr = self._get_image_arr()

        def _get_image_arr(self): # (n, 224, 224, 3)
            image_arr = np.empty((0, 224, 224, 3), int)
            for i in range(len(self.image_group_list)):
                processed_image = _process_image_path(self.image_folder_path + self.image_group_list[i])
                image_arr = np.append(image_arr, processed_image, axis=0)
            return image_arr


