# Discord Python Interpreter Bot

In my continuing quest to think of things that are terrible security loophole ridden ideas - I've made a bot that can interpret python code on Discord. What could possibly go wrong aside from literally everything.

## Usage
Add the bot to your server via this [link](https://discord.com/api/oauth2/authorize?client_id=740798488563941399&permissions=2048&scope=bot)

### Command examples

All of these are valid
```
>> print("Hello world")
```

```
>> `print("Hello world")`
```

````
>> ```
print("Hello world")
```
````

````
>> ```python
print("Hello world")
```
````

## My Attempts to Not Get Hacked

So, I'm not naive, I know how dangerous this stuff is, so I haven't just plugged user input into an `eval` or something. I'm using the library `RestrictedPython` to provide a (hopefully) safe execution environment and set up a 10 second timeout to avoid hangups on infinite loops. I'm really hoping I didn't miss anything, but please email me if I did.
