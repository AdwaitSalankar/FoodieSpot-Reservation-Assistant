from dotenv import load_dotenv
import os
from typing import Dict, Any
import json

def load_env():
    load_dotenv()
    if not os.getenv("TOGETHER_API_KEY"):
        raise ValueError("TOGETHER_API_KEY not found in environment variables")

def validate_reservation_params(params: Dict[str, Any]) -> bool:
    required = ["restaurant_name", "name", "party_size", "date", "time"]
    return all(
        p in params and 
        (params[p] if isinstance(params[p], str) else str(params[p])) not in ["", "0"]
        for p in required
    )

def format_restaurant_details(restaurant: Dict) -> str:
    amenities = ", ".join(restaurant['amenities']) if restaurant['amenities'] else "None"
    return (
        f"**{restaurant['name']}**\n"
        f" Cuisine: {restaurant['cuisine']}\n"
        f" Location: {restaurant['location']}\n"
        f" Rating: {restaurant['rating']} | Price: {restaurant['price_range']}\n"
        f" Capacity: {restaurant['capacity']} | Amenities: {amenities}\n"
    )

def parse_date_time(input_str: str) -> Dict[str, str]:
    # Simplified date/time
    from datetime import datetime
    try:
        dt = datetime.strptime(input_str, "%Y-%m-%d %H:%M")
        return {"date": dt.strftime("%Y-%m-%d"), "time": dt.strftime("%H:%M")}
    except ValueError:
        return {}
    