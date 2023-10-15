import cv2
import operator
from PIL import Image, ImageTk
from string import ascii_uppercase

class CharacterRecognition:
    def __init__(self):
        self.current_symbol = None
        self.panel = None
        # Load your models here
        self.loaded_model = None
        self.loaded_model_dru = None
        self.loaded_model_tkdi = None
        self.loaded_model_smn = None

    def process_image(self, test_image):
        cv2image = cv2.cvtColor(test_image, cv2.COLOR_BGR2RGBA)
        self.current_image = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=self.current_image)
        self.panel.imgtk = imgtk
        self.panel.config(image=imgtk)
        cv2image = cv2image[y1:y2, x1:x2]
        gray = cv2.cvtColor(cv2image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 2)
        th3 = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
        ret, res = cv2.threshold(th3, 70, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    def predict_characters(self, test_image):
        test_image = cv2.resize(test_image, (128, 128))
        result = self.loaded_model.predict(test_image.reshape(1, 128, 128, 1))
        result_dru = self.loaded_model_dru.predict(test_image.reshape(1, 128, 128, 1))
        result_tkdi = self.loaded_model_tkdi.predict(test_image.reshape(1, 128, 128, 1))
        result_smn = self.loaded_model_smn.predict(test_image.reshape(1, 128, 128, 1))

        prediction = {}
        prediction['blank'] = result[0][0]
        inde = 1
        for i in ascii_uppercase:
            prediction[i] = result[0][inde]
            inde += 1

        # Layer 1
        prediction = sorted(prediction.items(), key=operator.itemgetter(1), reverse=True)
        self.current_symbol = prediction[0][0]

        # Layer 2
        if self.current_symbol in ['D', 'R', 'U']:
            prediction = {}
            prediction['D'] = result_dru[0][0]
            prediction['R'] = result_dru[0][1]
            prediction['U'] = result_dru[0][2]
            prediction = sorted(prediction.items(), key=operator.itemgetter(1), reverse=True)
            self.current_symbol = prediction[0][0]

        if self.current_symbol in ['D', 'I', 'K', 'T']:
            prediction = {}
            prediction['D'] = result_tkdi[0][0]
            prediction['I'] = result_tkdi[0][1]
            prediction['K'] = result_tkdi[0][2]
            prediction['T'] = result_tkdi[0][3]
            prediction = sorted(prediction.items(), key=operator.itemgetter(1), reverse=True)
            self.current_symbol = prediction[0][0]

        if self.current_symbol in ['M', 'N', 'S']:
            prediction1 = {}
            prediction1['M'] = result_smn[0][0]
            prediction1['N'] = result_smn[0][1]
            prediction1['S'] = result_smn[0][2]
            prediction1 = sorted(prediction1.items(), key=operator.itemgetter(1), reverse=True)
            if prediction1[0][0] == 'S':
                self.current_symbol = prediction1[0][0]
            else:
                self.current_symbol = prediction[0][0]

if __name__ == "__main__":
    # Initialize your CharacterRecognition class and perform image processing and prediction as needed
