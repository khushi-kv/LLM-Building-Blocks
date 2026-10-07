# main.py
from models import Message

history:list[Message]=[
    Message(role="system",content="You are a helpful assistant.")
]

while True:
     user_input=input("You: ")
     if user_input=="quit":
          break
           
     history.append(Message(role="user",content=user_input))
     reply=f"you said:{user_input}"
     history.append(Message(role="assistant",content=reply))
     print(f"Bot: {reply}")

print(f"{len(history)} messages in history")