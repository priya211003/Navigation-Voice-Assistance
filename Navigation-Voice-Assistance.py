import requests
import pyttsx3
import speech_recognition as sr
from geopy.geocoders import Nominatim

# Function to convert text to speech
def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Function to get voice input from user
def get_voice_input(prompt):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak_text(prompt)
        print(prompt)
        audio = recognizer.listen(source)

    try:
        location_text = recognizer.recognize_google(audio)
        print("You said:", location_text)
        a="You said"+location_text
        speak_text(a)
        return location_text
    except sr.UnknownValueError:
        error_message = "Sorry, I could not understand the audio."
        print(error_message)
        speak_text(error_message)
        return None
    except sr.RequestError as e:
        error_message = f"Could not request results from speech recognition service; {e}"
        print(error_message)
        speak_text(error_message)
        return None

# Function to get the latitude and longitude of a location
def get_location(location_text):
    if not location_text:
        error_message = "No location text provided."
        print(error_message)
        speak_text(error_message)
        return None

    geolocator = Nominatim(user_agent="your_app_name")
    try:
        location = geolocator.geocode(location_text)
        if location:
            success_message = f"Location coordinates are {location.latitude}, {location.longitude}."
            
            
            return location.latitude, location.longitude
        else:
            error_message = "Could not retrieve location coordinates."
            print(error_message)
            speak_text(error_message)
            return None
    except Exception as e:
        error_message = f"Error with geolocation service; {e}"
        print(error_message)
        speak_text(error_message)
        return None

# Function to fetch directions using OSRM
def fetch_directions(origin, destination):
    url = f"http://router.project-osrm.org/route/v1/driving/{origin[1]},{origin[0]};{destination[1]},{destination[0]}?overview=false&steps=true"
    speak_text("Have a nice journey with Zyto, your cycling partner")
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if 'routes' in data and data['routes']:
            route = data['routes'][0]
            directions = []
            for leg in route['legs']:
                for step in leg['steps']:
                    instruction = step.get('maneuver', {}).get('instruction', 'Continue')
                    maneuver_type = step.get('maneuver', {}).get('type', '')
                    modifier = step.get('maneuver', {}).get('modifier', '')
                    road_name = step.get('name', '')
                    distance = step.get('distance', 0)
                    
                    # Construct the direction string with turn instructions
                    if maneuver_type in ['turn', 'merge', 'on ramp', 'off ramp', 'fork']:
                        if modifier:
                            direction = f"Turn {modifier} onto {road_name}"
                        else:
                            direction = f"Continue onto {road_name}"
                    elif maneuver_type == 'roundabout':
                        exit_number = step.get('maneuver', {}).get('exit', 1)
                        direction = f"Take the {exit_number} exit at the roundabout onto {road_name}"
                    else:
                        direction = f"{instruction} on {road_name}"

                    directions.append(f"{direction}\t{distance:.1f}m")

            # Summarizing the entire route's distance and duration
            total_distance = route['distance']
            total_duration = route['duration']
            
            # Ascend and descend data may not be directly available in OSRM response
            # Here we are assuming ascend and descend might not be available
            ascend = 0  # Placeholder as OSRM does not provide ascend and descend data
            descend = 0  # Placeholder as OSRM does not provide ascend and descend data

            route_info = {
                'distance': total_distance,
                'duration': total_duration,
                'ascend': ascend,
                'descend': descend,
                'directions': directions
            }
            return route_info
        else:
            error_message = "Could not retrieve directions data."
            print(error_message)
            speak_text(error_message)
            return None
    except requests.exceptions.RequestException as e:
        error_message = f"HTTP Request failed: {e}"
        print(error_message)
        speak_text(error_message)
        return None
    except ValueError as e:
        error_message = f"Parsing Error: {e}"
        print(error_message)
        speak_text(error_message)
        return None

# Function to convert route information to speech
def speak_directions(route_info):
    if route_info:
        distance_km = route_info['distance'] / 1000
        duration_min = route_info['duration'] / 60
        print(f"Directions\n\nDistance: {distance_km:.1f}km. Time: {duration_min:.0f} min.")
        speak_text(f"Distance: {distance_km:.1f} kilometers. Time: {duration_min:.0f} minutes.")
        
        print(f"Ascend: {route_info['ascend']}m. Descend: {route_info['descend']}m.")
        speak_text(f"Ascend: {route_info['ascend']} meters. Descend: {route_info['descend']} meters.")
        
        print()
        
        for i, direction in enumerate(route_info['directions']):
            print(f"{i + 1}. {direction}")
            speak_text(direction)
    else:
        error_message = "Could not fetch directions."
        print(error_message)
        speak_text(error_message)

# Main function to run the script
def main():
    origin_text = get_voice_input("Please say your origin location:")
    destination_text = get_voice_input("Please say your destination location:")

    origin = get_location(origin_text)
    destination = get_location(destination_text)

    if origin and destination:
        route_info = fetch_directions(origin, destination)
        speak_directions(route_info)
    else:
        speak_text("Could not open directions due to invalid coordinates.")

if __name__ == "__main__":
    main()
