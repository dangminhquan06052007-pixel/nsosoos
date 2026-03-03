# main.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import shutil
import os

# --- PHẦN IMPORT ĐÚNG (KHÔNG CÒN SRC) ---
from database import FOOD_DATA
from models.detector import detector
from models.volume import estimator
# ----------------------------------------

app = FastAPI(title="Food Calorie Scanner Pro")

class NutritionInfo(BaseModel):
    food_name: str
    estimated_gram: float
    calories: float
    protein: float
    carbs: float
    fat: float

@app.post("/scan-food", response_model=NutritionInfo)
async def scan_food(file: UploadFile = File(...)):
    temp_file = f"temp_{file.filename}"
    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # 1. Nhận diện
        food_key = detector.predict(temp_file)
        print(f"-> Món ăn nhận diện: {food_key}")

        if food_key not in FOOD_DATA:
             raise HTTPException(status_code=404, detail=f"Nhận diện được '{food_key}' nhưng không có dữ liệu.")

        # 2. Tính gram
        gram = estimator.estimate(temp_file, food_key)
        
        # 3. Tính calo
        base_data = FOOD_DATA[food_key]
        ratio = gram / 100.0
        
        result = NutritionInfo(
            food_name=food_key.replace("_", " ").title(),
            estimated_gram=round(gram, 1),
            calories=round(base_data["calories"] * ratio, 1),
            protein=round(base_data["protein"] * ratio, 1),
            carbs=round(base_data["carbs"] * ratio, 1),
            fat=round(base_data["fat"] * ratio, 1)
        )
        return result
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)