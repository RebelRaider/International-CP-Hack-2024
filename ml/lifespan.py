import pickle

import torch
import whisper
import imagebind
from loguru import logger
from transformers import GPT2Tokenizer, GPT2LMHeadModel

from ml.constants import RUGPT, CLASSIFIER_PATH

device = "cuda" if torch.cuda.is_available() else "cpu"

logger.debug("loading wisper")
whisper_model = whisper.load_model("tiny")
whisper_model.eval()
whisper_model.to(device)

logger.debug("loading imagebind")
imagebind_model = imagebind.model.imagebind_huge(True)
imagebind_model.eval()
imagebind_model.to(device)

logger.debug("loading bert")
bert_tokenizer = GPT2Tokenizer.from_pretrained(RUGPT)
bert_model = GPT2LMHeadModel.from_pretrained(RUGPT)
bert_model.to(device)

with open(CLASSIFIER_PATH, "rb") as f:
    catboost_models = pickle.load(f)
