import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import os
from dataclasses import dataclass

@dataclass
class Restaurant:
    id: int
    name: str
    cuisine: str
    location: str
    capacity: int
    amenities: List[str]
    rating: float
    price_range: str
    opening_hours: Dict[str, str]

@dataclass
class Reservation:
    id: str
    restaurant_id: int
    name: str
    party_size: int
    date: str
    time: str
    special_requests: str

class RestaurantDB:
    def __init__(self):
        self.restaurants = self._load_fixed_restaurants()
        self.reservations = []
        self.reservation_file = "reservations.json"
        self._load_reservations_from_file()
    
    def _load_fixed_restaurants(self) -> List[Restaurant]:
        fixed_restaurants = [
            Restaurant(
                id=1,
                name="Taj Mahal Bistro",
                cuisine="North Indian",
                location="Downtown",
                capacity=50,
                amenities=["private dining", "valet parking", "wheelchair accessible"],
                rating=4.6,
                price_range="₹400-₹8000",
                opening_hours={
                    "Monday": "11:00-23:00",
                    "Tuesday": "11:00-23:00",
                    "Wednesday": "11:00-23:00",
                    "Thursday": "11:00-23:00",
                    "Friday": "11:00-24:00",
                    "Saturday": "10:00-24:00",
                    "Sunday": "10:00-23:00"
                }
            ),
            Restaurant(
                id=2,
                name="Coastal Spice",
                cuisine="South Indian",
                location="Midtown",
                capacity=45,
                amenities=["live music", "outdoor seating"],
                rating=4.5,
                price_range="₹300-₹5000",
                opening_hours={
                    "Monday": "11:00-22:30",
                    "Tuesday": "11:00-22:30",
                    "Wednesday": "11:00-23:00",
                    "Thursday": "11:00-23:00",
                    "Friday": "11:00-23:30",
                    "Saturday": "10:00-23:30",
                    "Sunday": "10:00-22:30"
                }
            ),
            Restaurant(
                id=3,
                name="Punjab Grill House",
                cuisine="North Indian",
                location="Uptown",
                capacity=60,
                amenities=["bar", "live tandoor counter"],
                rating=4.7,
                price_range="₹350-₹7000",
                opening_hours={
                    "Monday": "11:00-23:00",
                    "Tuesday": "11:00-23:00",
                    "Wednesday": "11:00-23:30",
                    "Thursday": "11:00-23:30",
                    "Friday": "11:00-24:00",
                    "Saturday": "10:00-24:00",
                    "Sunday": "10:00-23:00"
                }
            ),
            Restaurant(
                id=4,
                name="South Palace",
                cuisine="South Indian",
                location="Outskirts",
                capacity=55,
                amenities=["banquet hall", "outdoor seating"],
                rating=4.4,
                price_range="₹250-₹4500",
                opening_hours={
                    "Monday": "11:00-22:00",
                    "Tuesday": "11:00-22:00",
                    "Wednesday": "11:00-22:30",
                    "Thursday": "11:00-22:30",
                    "Friday": "11:00-23:00",
                    "Saturday": "10:00-23:00",
                    "Sunday": "10:00-22:00"
                }
            ),
            Restaurant(
                id=5,
                name="Classic Dhaba",
                cuisine="North Indian",
                location="Downtown",
                capacity=40,
                amenities=["river view", "cultural performances"],
                rating=4.8,
                price_range="₹500-₹9000",
                opening_hours={
                    "Monday": "11:00-22:30",
                    "Tuesday": "11:00-22:30",
                    "Wednesday": "11:00-23:00",
                    "Thursday": "11:00-23:00",
                    "Friday": "11:00-23:30",
                    "Saturday": "10:00-23:30",
                    "Sunday": "10:00-22:30"
                }
            ),
            Restaurant(
                id=6,
                name="Rajasthani Darbar",
                cuisine="North Indian",
                location="Midtown",
                capacity=65,
                amenities=["traditional seating", "folk dance shows"],
                rating=4.3,
                price_range="₹300-₹6000",
                opening_hours={
                    "Monday": "11:00-23:00",
                    "Tuesday": "11:00-23:00",
                    "Wednesday": "11:00-23:30",
                    "Thursday": "11:00-23:30",
                    "Friday": "11:00-24:00",
                    "Saturday": "10:00-24:00",
                    "Sunday": "10:00-23:00"
                }
            ),
            Restaurant(
                id=7,
                name="Goan Shack",
                cuisine="Multicuisine",
                location="Uptown",
                capacity=5,
                amenities=["beach theme", "bar"],
                rating=4.6,
                price_range="₹400-₹7500",
                opening_hours={
                    "Monday": "11:00-23:00",
                    "Tuesday": "11:00-23:00",
                    "Wednesday": "11:00-23:30",
                    "Thursday": "11:00-23:30",
                    "Friday": "11:00-24:00",
                    "Saturday": "10:00-24:00",
                    "Sunday": "10:00-23:00"
                }
            ),
            Restaurant(
                id=8,
                name="Hyderabad House",
                cuisine="Multicuisine",
                location="Outskirts",
                capacity=70,
                amenities=["banquet hall", "sheesha lounge"],
                rating=4.9,
                price_range="₹450-₹10000",
                opening_hours={
                    "Monday": "11:00-23:00",
                    "Tuesday": "11:00-23:00",
                    "Wednesday": "11:00-23:30",
                    "Thursday": "11:00-23:30",
                    "Friday": "11:00-24:00",
                    "Saturday": "10:00-24:00",
                    "Sunday": "10:00-23:00"
                }
            ),
            Restaurant(
                id=9,
                name="Gujarati Bhavan",
                cuisine="North Indian",
                location="Downtown",
                capacity=50,
                amenities=["thali service", "vegetarian only"],
                rating=4.2,
                price_range="₹200-₹4000",
                opening_hours={
                    "Monday": "11:00-22:00",
                    "Tuesday": "11:00-22:00",
                    "Wednesday": "11:00-22:30",
                    "Thursday": "11:00-22:30",
                    "Friday": "11:00-23:00",
                    "Saturday": "10:00-23:00",
                    "Sunday": "10:00-22:00"
                }
            ),
            Restaurant(
                id=10,
                name="Kashmiri Kitchen",
                cuisine="North Indian",
                location="Midtown",
                capacity=30,
                amenities=["mountain view", "hookah"],
                rating=4.7,
                price_range="₹500-₹8500",
                opening_hours={
                    "Monday": "11:00-22:30",
                    "Tuesday": "11:00-22:30",
                    "Wednesday": "11:00-23:00",
                    "Thursday": "11:00-23:00",
                    "Friday": "11:00-23:30",
                    "Saturday": "10:00-23:30",
                    "Sunday": "10:00-22:30"
                }
            ),
            Restaurant(
                id=11,
                name="Awadhi Lounge",
                cuisine="Multicuisine",
                location="Uptown",
                capacity=45,
                amenities=["live ghazals", "royal decor"],
                rating=4.8,
                price_range="₹600-₹12000",
                opening_hours={
                    "Monday": "11:00-23:00",
                    "Tuesday": "11:00-23:00",
                    "Wednesday": "11:00-23:30",
                    "Thursday": "11:00-23:30",
                    "Friday": "11:00-24:00",
                    "Saturday": "10:00-24:00",
                    "Sunday": "10:00-23:00"
                }
            ),
            Restaurant(
                id=12,
                name="Konkan Express",
                cuisine="Multicuisine",
                location="Outskirts",
                capacity=40,
                amenities=["fishing pond", "boat seating"],
                rating=4.5,
                price_range="₹350-₹6500",
                opening_hours={
                    "Monday": "11:00-22:00",
                    "Tuesday": "11:00-22:00",
                    "Wednesday": "11:00-22:30",
                    "Thursday": "11:00-22:30",
                    "Friday": "11:00-23:00",
                    "Saturday": "10:00-23:00",
                    "Sunday": "10:00-22:00"
                }
            ),
            Restaurant(
                id=13,
                name="Retro Dhaba",
                cuisine="Multicuisine",
                location="Downtown",
                capacity=55,
                amenities=["retro decor", "bar"],
                rating=4.4,
                price_range="₹400-₹7000",
                opening_hours={
                    "Monday": "11:00-23:00",
                    "Tuesday": "11:00-23:00",
                    "Wednesday": "11:00-23:30",
                    "Thursday": "11:00-23:30",
                    "Friday": "11:00-24:00",
                    "Saturday": "10:00-24:00",
                    "Sunday": "10:00-23:00"
                }
            ),
            Restaurant(
                id=14,
                name="Rasoi Khana",
                cuisine="North Indian",
                location="Midtown",
                capacity=60,
                amenities=["live litti chokha counter", "cultural shows"],
                rating=4.3,
                price_range="₹250-₹4500",
                opening_hours={
                    "Monday": "11:00-22:30",
                    "Tuesday": "11:00-22:30",
                    "Wednesday": "11:00-23:00",
                    "Thursday": "11:00-23:00",
                    "Friday": "11:00-23:30",
                    "Saturday": "10:00-23:30",
                    "Sunday": "10:00-22:30"
                }
            ),
            Restaurant(
                id=15,
                name="Andhra Spice",
                cuisine="South Indian",
                location="Uptown",
                capacity=50,
                amenities=["chilli challenge", "bar"],
                rating=4.7,
                price_range="₹300-₹6000",
                opening_hours={
                    "Monday": "11:00-23:00",
                    "Tuesday": "11:00-23:00",
                    "Wednesday": "11:00-23:30",
                    "Thursday": "11:00-23:30",
                    "Friday": "11:00-24:00",
                    "Saturday": "10:00-24:00",
                    "Sunday": "10:00-23:00"
                }
            ),
            Restaurant(
                id=16,
                name="Flavours",
                cuisine="North Indian",
                location="Outskirts",
                capacity=35,
                amenities=["bamboo decor", "live music"],
                rating=4.6,
                price_range="₹350-₹5500",
                opening_hours={
                    "Monday": "11:00-22:00",
                    "Tuesday": "11:00-22:00",
                    "Wednesday": "11:00-22:30",
                    "Thursday": "11:00-22:30",
                    "Friday": "11:00-23:00",
                    "Saturday": "10:00-23:00",
                    "Sunday": "10:00-22:00"
                }
            ),
            Restaurant(
                id=17,
                name="Tadka Tandoor",
                cuisine="Multicuisine",
                location="Downtown",
                capacity=45,
                amenities=["street food counter", "theater shows"],
                rating=4.5,
                price_range="₹200-₹4000",
                opening_hours={
                    "Monday": "11:00-22:30",
                    "Tuesday": "11:00-22:30",
                    "Wednesday": "11:00-23:00",
                    "Thursday": "11:00-23:00",
                    "Friday": "11:00-23:30",
                    "Saturday": "10:00-23:30",
                    "Sunday": "10:00-22:30"
                }
            ),
            Restaurant(
                id=18,
                name="Fuel Blend",
                cuisine="Multicuisine",
                location="Midtown",
                capacity=40,
                amenities=["Western", "live cooking"],
                rating=4.4,
                price_range="₹300-₹5000",
                opening_hours={
                    "Monday": "11:00-23:00",
                    "Tuesday": "11:00-23:00",
                    "Wednesday": "11:00-23:30",
                    "Thursday": "11:00-23:30",
                    "Friday": "11:00-24:00",
                    "Saturday": "10:00-24:00",
                    "Sunday": "10:00-23:00"
                }
            ),
            Restaurant(
                id=19,
                name="Grand Garden",
                cuisine="North Indian",
                location="Uptown",
                capacity=50,
                amenities=["temple style seating", "vegetarian only"],
                rating=4.3,
                price_range="₹150-₹3000",
                opening_hours={
                    "Monday": "07:00-22:00",
                    "Tuesday": "07:00-22:00",
                    "Wednesday": "07:00-22:30",
                    "Thursday": "07:00-22:30",
                    "Friday": "07:00-23:00",
                    "Saturday": "07:00-23:00",
                    "Sunday": "07:00-22:00"
                }
            ),
            Restaurant(
                id=20,
                name="Malabari Coast",
                cuisine="South Indian",
                location="Outskirts",
                capacity=60,
                amenities=["beach view", "spice market"],
                rating=4.7,
                price_range="₹400-₹7000",
                opening_hours={
                    "Monday": "11:00-23:00",
                    "Tuesday": "11:00-23:00",
                    "Wednesday": "11:00-23:30",
                    "Thursday": "11:00-23:30",
                    "Friday": "11:00-24:00",
                    "Saturday": "10:00-24:00",
                    "Sunday": "10:00-23:00"
                }
            ),
            Restaurant(
                id=21,
                name="Pahadi Dhaba",
                cuisine="North Indian",
                location="Downtown",
                capacity=30,
                amenities=["mountain decor", "fireplace"],
                rating=4.5,
                price_range="₹350-₹6000",
                opening_hours={
                    "Monday": "11:00-22:00",
                    "Tuesday": "11:00-22:00",
                    "Wednesday": "11:00-22:30",
                    "Thursday": "11:00-22:30",
                    "Friday": "11:00-23:00",
                    "Saturday": "10:00-23:00",
                    "Sunday": "10:00-22:00"
                }
            ),
            Restaurant(
                id=22,
                name="Mewari Mahal",
                cuisine="North Indian",
                location="Midtown",
                capacity=55,
                amenities=["royal palace theme", "folk performances"],
                rating=4.8,
                price_range="₹500-₹9000",
                opening_hours={
                    "Monday": "11:00-23:00",
                    "Tuesday": "11:00-23:00",
                    "Wednesday": "11:00-23:30",
                    "Thursday": "11:00-23:30",
                    "Friday": "11:00-24:00",
                    "Saturday": "10:00-24:00",
                    "Sunday": "10:00-23:00"
                }
            ),
            Restaurant(
                id=23,
                name="Chaat Corner",
                cuisine="Multicuisine",
                location="Uptown",
                capacity=65,
                amenities=["live counters", "outdoor seating"],
                rating=4.2,
                price_range="₹100-₹2000",
                opening_hours={
                    "Monday": "10:00-22:00",
                    "Tuesday": "10:00-22:00",
                    "Wednesday": "10:00-22:30",
                    "Thursday": "10:00-22:30",
                    "Friday": "10:00-23:00",
                    "Saturday": "09:00-23:00",
                    "Sunday": "09:00-22:00"
                }
            ),
            Restaurant(
                id=24,
                name="Boat House",
                cuisine="South Indian",
                location="Outskirts",
                capacity=40,
                amenities=["backwater view", "boat dining"],
                rating=4.6,
                price_range="₹400-₹7500",
                opening_hours={
                    "Monday": "11:00-22:30",
                    "Tuesday": "11:00-22:30",
                    "Wednesday": "11:00-23:00",
                    "Thursday": "11:00-23:00",
                    "Friday": "11:00-23:30",
                    "Saturday": "10:00-23:30",
                    "Sunday": "10:00-22:30"
                }
            ),
            Restaurant(
                id=25,
                name="Dilli 6",
                cuisine="North Indian",
                location="Downtown",
                capacity=70,
                amenities=["street theme", "live chaat counter"],
                rating=4.9,
                price_range="₹200-₹5000",
                opening_hours={
                    "Monday": "11:00-23:00",
                    "Tuesday": "11:00-23:00",
                    "Wednesday": "11:00-23:30",
                    "Thursday": "11:00-23:30",
                    "Friday": "11:00-24:00",
                    "Saturday": "10:00-24:00",
                    "Sunday": "10:00-23:00"
                }
            )
        ]
        return fixed_restaurants
    
    def find_restaurants(self, cuisine: str = None, location: str = None, 
                        party_size: int = None, date: str = None, 
                        time: str = None, amenities: List[str] = None) -> List[Dict]:
        results = []
        for restaurant in self.restaurants:
            # Filter by criteria
            if cuisine and restaurant.cuisine.lower() != cuisine.lower():
                continue
            if location and restaurant.location.lower() != location.lower():
                continue
            if amenities and not all(a.lower() in [am.lower() for am in restaurant.amenities] for a in amenities):
                continue
            
            if party_size and restaurant.capacity < party_size:
                continue
                
            if date and time:
                # availability check
                reservation_count = sum(
                    1 for r in self.reservations 
                    if r.restaurant_id == restaurant.id 
                    and r.date == date 
                    and abs((datetime.strptime(r.time, "%H:%M") - datetime.strptime(time, "%H:%M")).total_seconds()) < 3600
                )
                if reservation_count >= restaurant.capacity / 4:
                    continue
            
            results.append({
                "id": restaurant.id,
                "name": restaurant.name,
                "cuisine": restaurant.cuisine,
                "location": restaurant.location,
                "capacity": restaurant.capacity,
                "amenities": restaurant.amenities,
                "rating": restaurant.rating,
                "price_range": restaurant.price_range,
                "available": True
            })
        
        return results
    
    def make_reservation(self, restaurant_id: int, name: str, party_size: int, 
                       date: str, time: str, special_requests: str = "") -> Dict:
        
        # Validate all required parameters
        if not name or name.strip() == "":
            return {"success": False, "error": "Please provide a name for the reservation"}
        
        if party_size <= 0:
            return {"success": False, "error": "Party size must be at least 1"}
        
        if not date or date.strip() == "":
            return {"success": False, "error": "Please provide a reservation date"}
        
        if not time or time.strip() == "":
            return {"success": False, "error": "Please provide a reservation time"}
        
        restaurant = next((r for r in self.restaurants if r.id == restaurant_id), None)
        if not restaurant:
            return {"success": False, "error": "Restaurant not found"}
        
        if party_size > restaurant.capacity:
            return {"success": False, "error": f"Party size exceeds restaurant capacity of {restaurant.capacity}, Book another restaurant."}
     
        overbooked = sum(
            1 for r in self.reservations
            if r.restaurant_id == restaurant_id and r.date == date
            and abs((datetime.strptime(r.time, "%H:%M") - datetime.strptime(time, "%H:%M")).total_seconds()) < 3600
        )

        if overbooked >= restaurant.capacity // 4:
            return {
                "success": False,
                "error": f"The time slot {time} is currently full. Please try a different time.",
                "suggestions": [f"{hour:02d}:{minute:02d}" for hour in range(18, 22) for minute in [0, 30]]
            }

        # Generate reservation ID
        reservation_id = f"RES-{random.randint(10000, 99999)}"
        
        # Create reservation
        reservation = Reservation(
            id=reservation_id,
            restaurant_id=restaurant_id,
            name=name,
            party_size=party_size,
            date=date,
            time=time,
            special_requests=special_requests
        )
        self.reservations.append(reservation)
        self._save_reservations_to_file()
        
        return {
            "success": True,
            "reservation_id": reservation_id,
            "restaurant_name": restaurant.name,
            "date": date,
            "time": time,
            "party_size": party_size
        }
    
    def _load_reservations_from_file(self):
        if os.path.exists(self.reservation_file):
            try:
                with open(self.reservation_file, "r") as f:
                    content = f.read().strip()
                    if not content:
                        self.reservations = []
                        return
                    data = json.loads(content)
                    self.reservations = [Reservation(**r) for r in data]
            except Exception as e:
                self.reservations = []
        else:
            self._save_reservations_to_file()


    def _save_reservations_to_file(self):
        with open(self.reservation_file, "w") as f:
            json.dump([r.__dict__ for r in self.reservations], f, indent=2)
    
    def modify_reservation(self, reservation_id: str, updates: dict) -> dict:
        reservation = next((r for r in self.reservations if r.id == reservation_id), None)
        if not reservation:
            return {"success": False, "error": "Reservation not found"}
        
        for key, value in updates.items():
            if hasattr(reservation, key):
                setattr(reservation, key, value)
        
        self._save_reservations_to_file()

        return {
            "success": True,
            "message": "Reservation updated",
            "updated": reservation.__dict__
        }

    def cancel_reservation(self, reservation_id: str) -> Dict:
        original_len = len(self.reservations)
        self.reservations = [r for r in self.reservations if r.id != reservation_id]
        if len(self.reservations) == original_len:
            return {"success": False, "error": "Reservation not found"}

        self._save_reservations_to_file()
        return {"success": True, "message": "Reservation canceled"}
