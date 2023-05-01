from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time
import json
from PIL import ImageDraw
from PIL import ImageFont

with open('secret.json') as f:
    secret = json.load(f)
KEY = secret['KEY']
ENDPOINT = secret['ENDPOINT']

computervision_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(KEY))

def get_tags(filepath):
    local_image = open(filepath,"rb")
    tags_result = computervision_client.tag_image_in_stream(local_image)
    tags = tags_result.tags
    # Print results with confidence score
#     else:
#         for tag in tags:
#             print(tag.name)
#             print("{:.2f}%".format(tag.confidence * 100))
    return tags
  
  
  
def detect_objects(filepath):
    local_image = open(filepath,"rb")

    detect_objects_results_local = computervision_client.detect_objects_in_stream(local_image)
    objects = detect_objects_results_local.objects
    return objects
  
  
import streamlit as st

st.title('物体検出アプリ')

uploaded_file = st.file_uploader('Choose an image...',type=['jpg','png'])

if uploaded_file is not None:
  img = Image.open(uploaded_file) 
  img_path = f'img/{uploaded_file.name}'
  img.save(img_path)
  objects = detect_objects(img_path)
  
  #描画
  draw = ImageDraw.Draw(img)
  for object in objects:
    x = object.rectangle.x
    y = object.rectangle.y
    w = object.rectangle.w
    h = object.rectangle.h
    caption = object.object_property
    
    font = ImageFont.truetype(font = './ipaexg.ttf',size=20)
    text_w,text_h = draw.textsize(caption,font = font)
    
    draw.rectangle([(x,y),(x+w,y+h)],fill=None,outline='blue',width=5)
    draw.rectangle([(x,y),(x+text_w,y+text_h)],fill='blue',outline='blue',width=5)
    draw.text((x,y),caption,fill='white',font=font)
  
  st.image(img)
  
  tags = get_tags(img_path)
  all_tags=""
  for tag in tags:
    all_tags = all_tags + '[{}:{:.2f}%] '.format(tag.name, tag.confidence*100)
  
  st.markdown('**認識されたコンテンツタグとその信頼性**')
  st.markdown(f'>{all_tags}')