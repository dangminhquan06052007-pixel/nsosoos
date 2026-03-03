import pandas as pd
import random
import os

# --- SỬA ĐỔI TẠI ĐÂY ---
# Đường dẫn giờ trỏ đến file .txt
DB_PATH = "data/nutrition_db.txt"

def get_nutrition_from_db(food_name):
    # Kiểm tra xem file có tồn tại không để tránh crash server
    if not os.path.exists(DB_PATH):
        print(f"LỖI: Không tìm thấy file tại đường dẫn: {DB_PATH}")
        return None

    try:
        # Đọc file .txt (nội dung vẫn phải có dấu phẩy ngăn cách)
        df = pd.read_csv(DB_PATH, sep=',', encoding='utf-8') 
    except Exception as e:
        print(f"LỖI: Không đọc được nội dung file. Chi tiết: {e}")
        return None
    
    # Kiểm tra xem có cột 'food_name' không
    if 'food_name' not in df.columns:
        print("LỖI: File dữ liệu không có cột 'food_name'. Kiểm tra lại nội dung file!")
        return None

    df['food_name'] = df['food_name'].astype(str)
    
    result = df[df['food_name'].str.lower() == food_name.lower()]
    
    if not result.empty:
        return result.iloc[0].to_dict()
    return None

def predict_food_info(image):
    """
    Hàm này sau này sẽ nhận ảnh và chạy model AI.
    Hiện tại trả về kết quả giả lập.
    """
    # 1. Giả lập AI nhận diện được món (Sau này thay bằng YOLO)
    list_foods = ["Pho bo tai", "Com tam suon", "Banh mi thit"]
    detected_food = random.choice(list_foods)
    
    # 2. Giả lập khối lượng (gram)
    estimated_weight = random.randint(200, 500) # Random 200-500g
    
    # 3. Lấy thông tin dinh dưỡng từ DB
    nutrition_info = get_nutrition_from_db(detected_food)
    
    if nutrition_info:
        # Tính toán lại dựa trên khối lượng thực tế
        multiplier = estimated_weight / 100
        
        return {
            "food_name": detected_food,
            "weight_grams": estimated_weight,
            "calories": round(nutrition_info['calories_per_100g'] * multiplier, 1),
            "protein": round(nutrition_info['protein'] * multiplier, 1),
            "carbs": round(nutrition_info['carbs'] * multiplier, 1),
            "fat": round(nutrition_info['fat'] * multiplier, 1)
        }
    
    return {"error": "Food not found in database"}