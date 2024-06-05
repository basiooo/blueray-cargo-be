def search_city_by_name(city_name, data):
    for city in data:
        if city["city_name"].lower() == city_name.lower():
            return [city]
    return []
