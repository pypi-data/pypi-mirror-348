import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from greetron.greetings import get_random_greeting, get_random_goodbye

print(get_random_greeting())
print(get_random_greeting("Aryan"))
print(get_random_greeting("Aryan", mode="formal"))

print(get_random_goodbye())
print(get_random_goodbye("Aryan"))
print(get_random_goodbye("Aryan", mode="formal"))
