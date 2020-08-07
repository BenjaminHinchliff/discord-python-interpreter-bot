# Discord Python Interpreter Bot

In my continuing quest to think of things that are terrible security loophole ridden ideas - I've made a bot that can interpret python code on Discord. What could possibly go wrong aside from literally everything.

## My Attempts to Not Get Hacked

So, I'm not naive, I know how dangerous this stuff is, so I haven't just plugged user input into an `eval` or something. I'm using the library `RestrictedPython` to provide a (hopefully) safe execution environment and set up a 10 second timeout to avoid hangups on infinite loops. I'm really hoping I didn't miss anything, but please email me if I did.
