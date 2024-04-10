import requests
import time

#Fareed
# Function to format duration in minutes to "hours h minutes m" format
def format_duration(minutes):
    hours, minutes = divmod(minutes, 60)
    return f"{hours}h {minutes}m"

#Fareed
# Function to search flights using entity IDs
def search_flights_with_entity_ids(fromEntityId, toEntityId, departDate):
    url = "https://sky-scanner3.p.rapidapi.com/flights/search-one-way"
    querystring = {
        "fromEntityId": fromEntityId,
        "toEntityId": toEntityId,
        "departDate": departDate
    }
    headers = {
        "X-RapidAPI-Key": "ddfeaaf6e7mshf8f352856a366e4p115b58jsn9005b19e9de4",
        "X-RapidAPI-Host": "sky-scanner3.p.rapidapi.com"
    }
    
    # Send GET request to the API endpoint
    response = requests.get(url, headers=headers, params=querystring)
    
    if response.status_code == 200:
        data = response.json()
        itineraries = data.get('data', {}).get('itineraries', [])
        processed_data = []
        
        # Process each itinerary and extract relevant flight information
        for itinerary in itineraries:
            price = itinerary.get('price', {}).get('formatted', '')
            legs = itinerary.get('legs', [])
            
            if legs:
                first_leg = legs[0]
                departure_time = first_leg.get('departure')
                arrival_time = first_leg.get('arrival')
                duration_minutes = first_leg.get('durationInMinutes', 0)
                duration_formatted = format_duration(duration_minutes)
                stop_count = first_leg.get('stopCount')
                
                first_segment = first_leg.get('segments', [])[0]
                flight_number = first_segment.get('flightNumber')
                carrier = first_segment.get('marketingCarrier', {}).get('name')
                
                # Build the processed flight dictionary
                flight_data = {
                    'flightNumber': flight_number,
                    'carrier': carrier,
                    'departureTime': departure_time,
                    'arrivalTime': arrival_time,
                    'duration': duration_formatted,
                    'stopCount': stop_count,
                    'price': price,
                }
                processed_data.append(flight_data)
        
        return processed_data
    else:
        print(f"API request failed with status code: {response.status_code}")
        return []
#Fareed
# Function to perform auto-complete for flight search queries
def auto_complete(query):
    url = "https://sky-scanner3.p.rapidapi.com/flights/auto-complete"
    querystring = {"query": query}
    headers = {
        "X-RapidAPI-Key": "ddfeaaf6e7mshf8f352856a366e4p115b58jsn9005b19e9de4",
        "X-RapidAPI-Host": "sky-scanner3.p.rapidapi.com"
    }
    
    # Send GET request to the API endpoint
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    
    print(f"API response for query '{query}':")
    print(data)
    print("---")
    
    if response.status_code == 200 and data.get('status'):
        suggestions = data.get('data', [])
        if suggestions:
            return suggestions[0]['presentation']['id']
        else:
            print(f"No suggestions found for query: {query}")
    else:
        print(f"API request failed with status code: {response.status_code}")
        return None