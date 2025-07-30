fruit_data = {
    "Apple": {"color": "Red", "taste": "Sweet", "nutrients": ["fiber", "vitamin C"]},
    "Banana": {"color": "Yellow", "taste": "Sweet", "nutrients": ["potassium", "vitamin B6"]},
    # Add more fruits...
}

def get_fruit_info(name):
    return fruit_data.get(name.title(), "Fruit not found.")
