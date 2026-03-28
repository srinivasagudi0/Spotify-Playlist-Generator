"""
brain pipeline

FLow:
input -> ai -> keywords -> spotify -> results -> format output
"""


import json

from ai import convert_to_emotion

def process_input(user_input):
    emotion = convert_to_emotion(user_input)
    return emotion


# this below funtion converts the JSON into a more user friendly format, this is just for demonstration, we can directly use the JSON response from the ai and pass it to spotify to get the results, but for now we will just format the output in a more user friendly way.
def format_output(emotion):
    emotion_dict = json.loads(emotion)
    formatted_output = f"Emotion: {emotion_dict['emotion']} \nMood: {emotion_dict['mood']} \nKeywords: {', '.join(emotion_dict['keywords'])} \nEnergy: {emotion_dict['energy']}"
    return formatted_output



