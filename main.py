import cv2
import math
import io
import json
from googletrans import Translator
import requests
from yandex_translate import YandexTranslate


imagesFolder = "images"
cap = cv2.VideoCapture(0)#Open web cam
frameRate = cap.get(40) #frame rate
frame =cap.read()


while(cap.isOpened()):
    frameId = cap.get(4) #current frame number
    ret, frame = cap.read()
    if (ret != True):
        break
    if (frameId % math.floor(frameRate) == 0):
        filename = imagesFolder + "/image_" +  str(int(frameId)) + ".jpg"
        cv2.imwrite(filename, frame) #Save Images
    #OCR (Extract Text from Image)
        img = cv2.imread(filename)
        roi = img
        url_api = "https://api.ocr.space/parse/image"
        _, compressedimage = cv2.imencode(".jpg", roi, [1, 90])
        file_bytes = io.BytesIO(compressedimage)
        
        result = requests.post(url_api,
                      files = {"image_480.jpg": file_bytes},
                      data = {"apikey": "ea285139df88957",
                              "language": "eng"})
        
        result = result.content.decode()
        result = json.loads(result)
        
        parsed_results = result.get("ParsedResults")[0]
        text_detected = parsed_results.get("ParsedText")
        # Text Translation
        trans = Translator()
        t = trans.translate(text_detected)
        ogt=(f'{t.origin}')
        trt=(f'{t.text}')
        print("\nOriginal Text: " + ogt)
        print("Translated Text: " + trt)
