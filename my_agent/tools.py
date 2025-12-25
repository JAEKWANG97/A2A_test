from typing import Dict


def get_current_time(city: str) -> Dict[str, str]:
    cities_time = {
        "Seoul": "10:30 AM",
        "New York": "6:30 PM",
        "London": "11:30 PM",
        "Tokyo": "4:30 AM",
    }
    time = cities_time.get(city, "Unknown")
    return {"status": "success", "city": city, "time": time}


def get_weather(city: str, units: str = "C") -> Dict[str, str]:
    data_c = {
        "Seoul": 5,
        "New York": 15,
        "London": 8,
        "Tokyo": 3,
    }
    desc = {
        "Seoul": "Cloudy",
        "New York": "Sunny",
        "London": "Rainy",
        "Tokyo": "Clear",
    }
    if city not in data_c:
        return {"status": "error", "error_message": f"No weather for '{city}'."}
    temp_c = data_c[city]
    if units.upper() == "F":
        temp = round((temp_c * 9 / 5) + 32)
        unit = "°F"
    else:
        temp = temp_c
        unit = "°C"
    return {"status": "success", "city": city, "weather": f"{desc[city]}, {temp}{unit}"}
