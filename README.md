# Navigation-Voice-Assistance

This project provides a voice-assisted navigation system in Python using the OpenStreetMap (OSM) API. It allows users to input origin and destination locations through voice commands, fetches route directions, and gives spoken instructions for a smoother navigation experience.

## Features

- Voice-based input for origin and destination locations.
- Fetches navigation directions and route details from OpenStreetMap via the OSRM API.
- Text-to-speech (TTS) for voice instructions on route directions.
- Summarizes the total distance, estimated duration, and directions to follow for the journey.

## Prerequisites

To run this project, you need:

- Python 3.x
- Required libraries:
  - `requests` for API requests
  - `pyttsx3` for text-to-speech
  - `speech_recognition` for capturing and recognizing voice input
  - `geopy` for geolocation (to convert place names to latitude and longitude)

Install the libraries with:
```bash
pip install requests pyttsx3 SpeechRecognition geopy
```

## Code Explanation

### Functions

- **speak_text**: Converts text to speech.
- **get_voice_input**: Captures user voice input for location names.
- **get_location**: Converts location name (text) to latitude and longitude using `geopy`.
- **fetch_directions**: Fetches route information between origin and destination using OSRM API.
- **speak_directions**: Reads out the step-by-step directions along with total route distance and estimated travel time.

### Main Code
1. **Voice Input**: Prompts for origin and destination locations through voice commands.
2. **Geolocation**: Translates place names into latitude and longitude.
3. **Fetch Directions**: Retrieves navigation directions from OSRM and structures them for use.
4. **Voice Output**: Summarizes and speaks the route details and step-by-step directions.

## Usage

1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/voice-navigation-osm.git
    ```
2. Run the script:
    ```bash
    python navigation_voice_assistant.py
    ```

3. Follow the prompts to speak your origin and destination locations.

