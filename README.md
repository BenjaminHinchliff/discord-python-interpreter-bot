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

### Gotcha(s)

There are few things that you can't *really* do in this python interpreter. One thing is that printing is really weird. Printing is done to a local variable called `printed`, if you want to acess the output you'll have to do a top-level print. This is a side-effect of RestrictedPython.

For example:
```py
def print_num(num):
  print(num)
  return printed

print(print_num(num))
```

a bit awkward, I know, but there's not much I can do about  it.

## Libraries

It's on my mind, but I don't think it'll be possible without a much heaver layer of virtualization. Let me know if you have any ideas.

## My Attempts to Not Get Hacked

So, I'm not naive, I know how dangerous this stuff is, so I haven't just plugged user input into an `eval` or something. I'm using the library `RestrictedPython` to provide a (hopefully) safe execution environment and set up a 10 second timeout to avoid hangups on infinite loops. I'm really hoping I didn't miss anything, but please open and issue if I did.
