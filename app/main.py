import joblib
import re
from sklearn.neural_network import MLPClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from fastapi import FastAPI, status
import json

app = FastAPI()

model = joblib.load('spam_classifier.joblib')

def preprocessor(text):
    text = re.sub('<[^>]*>', '', text) # Effectively removes HTML markup tags
    emoticons = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)', text)
    text = re.sub('[\W]+', ' ', text.lower()) + ' '.join(emoticons).replace('-', '')
    return text

def classify_message(model, message):
    message = preprocessor(message)
    label = model.predict([message])[0]
    predictions = model.predict_proba([message]).tolist()
    print(predictions)
    response = json.dumps({'predictions': predictions})

    return response

@app.get('/')
def get_root():

    return {'message': 'Welcome to the spam detection API'}

@app.get('/health_check')
def health():
    return 200

@app.post('/predict')
async def detect_spam_query(message: str):
    print(message)
    return classify_message(model, message)

from pydantic import BaseModel
class Message(BaseModel):
    message: str

@app.post('/test')
async def test(m: Message):
    print(m.message)
    return classify_message(model, m.message)

from fastapi import Request, FastAPI
import pandas as pd

@app.post('/test2')
async def test2(request: Request):
    print("----------------- TESTING -----------------")
    print (type(request))
    body = await request.json()
    print (type(body))
    print (body)
    instances = body["instances"]
    column_headers = ['message']
    inputs = pd.DataFrame(instances, columns=column_headers)
    outputs = model.predict(inputs)
    print("outputs")
    print(outputs.tolist())

    return {"predictions": outputs.tolist()}

@app.post('/predict/{message}')
async def detect_spam_path(message: str):
    return classify_message(model, message)
