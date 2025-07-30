import random

GREETINGS = {
    "formal": [
        "Hello! How may I assist you today?",
        "Good day! I'm here to support you with anything you need",
        "Hi! Let me know how I can be of service",
        "Greetings! How can I help you move forward today?",
        "Welcome! I’m ready when you are"
    ],
    "informal": [
        "Hey! What’s cookin'?",
        "Hi! Need a hand?",
        "Hey hey! Ready when you are",
        "Yo! What can I do for you?",
        "Hi! Let’s dive in"
    ]
}

GOODBYES = {
    "formal": [
        "Goodbye! Don’t hesitate to reach out if you need anything else.",
        "Thank you for using our service! Wishing you a great rest of your day.",
        "Signing off now. All the best in your endeavors!",
        "It was a pleasure assisting you. Take care!",
        "Feel free to return anytime. Until then, goodbye!"
    ],
    "informal": [
        "Catch ya later!",
        "Bye! Hit me up if you need more help",
        "Talk soon — take it easy!",
        "See ya around! 😄",
    ]
}


def get_random_greeting(name: str = None, mode: str = "formal") -> str:
    messages = GREETINGS.get(mode, GREETINGS["formal"])
    greeting = random.choice(messages)

    if name:
        return greeting.replace("!", f" {name}!") if "!" in greeting else f"{greeting}, {name}."

    return greeting


def get_random_goodbye(name: str = None, mode: str = "formal") -> str:
    messages = GOODBYES.get(mode, GOODBYES["formal"])
    goodbye = random.choice(messages)

    if name:
        return goodbye.replace("!", f" {name}!") if "!" in goodbye else f"{goodbye}, {name}."
    return goodbye
