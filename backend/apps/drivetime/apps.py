from django.apps import AppConfig
import html
from pathlib import Path
import os
from .tools.GoogleMapsTools import GoogleMapsTools
# from fast_bert.prediction import BertClassificationPredictor


class DrivetimeConfig(AppConfig):
    name = 'drivetime'
    gmt = GoogleMapsTools()
#     MODEL_PATH = Path("model")
#     BERT_PRETRAINED_PATH = Path("model/uncased_L-12_H-768_A-12/")
#     LABEL_PATH = Path("label/")
#     predictor = BertClassificationPredictor(model_path = MODEL_PATH/"multilabel-emotion-fastbert-basic.bin",
#                                             pretrained_path = BERT_PRETRAINED_PATH,
#                                             label_path = LABEL_PATH, multi_label=True)

