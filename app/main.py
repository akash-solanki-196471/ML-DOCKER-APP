from fastapi import FastAPI, Query, Form, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import tensorflow as tf
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy import create_engine, Column, Integer, DateTime, String, text
from sqlalchemy.orm import Session,sessionmaker
from sqlalchemy.ext.declarative import declarative_base 
import ast
import os
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
templates = Jinja2Templates(directory="app")
security = HTTPBasic()
DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You might want to restrict this to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictionLog(Base):
    __tablename__ = "prediction_logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow, server_default=text("CURRENT_TIMESTAMP"))
    image_string = Column(String)
    prediction_result = Column(String)

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

# Loading the model and cv
model_path = os.path.join(os.path.dirname(__file__), 'model', 'clothing_classification_model.h5')
model = tf.keras.models.load_model(model_path)

def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials is None and request.method == "OPTIONS":
        return None
    correct_username = os.environ.get("APP_USERNAME")  # replace with your desired username
    correct_password = os.environ.get("APP_PASSWORD")  # replace with your desired password

    if credentials.username != correct_username or credentials.password != correct_password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return credentials.username

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.options("/")
async def options():
    return {"msg": "OK"}

@app.get("/")
def read_root(request: Request, username: str = Depends(authenticate_user)):
    return templates.TemplateResponse("index.html", {"request": request, "username": username})

@app.post("/predict")
async def predict(image: str = Form(...),db: Session = Depends(get_db)):
    # Taking the input
    array_list = ast.literal_eval(image)
    # Convert the list to a NumPy array
    image_numpy_array = np.array(array_list)

    # Prediction
    my_pred = model.predict(image_numpy_array)
    # Log prediction
    log_prediction(image, class_names[np.argmax(my_pred[0])], db)

    # Returning JSON response
    return {"prediction": class_names[np.argmax(my_pred[0])]}

def log_prediction(image: str, prediction: str, db: Session):
    db_entry = PredictionLog(image_string=image, prediction_result=prediction)
    db.add(db_entry)
    db.commit()

