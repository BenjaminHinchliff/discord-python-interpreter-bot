import os
import ast
import re

import dotenv
import discord
from discord.ext import commands
from RestrictedPython import compile_restricted, safe_builtins
from RestrictedPython.PrintCollector import PrintCollector

dotenv.load_dotenv()

def interpret(code):
    code += "\nresults = printed"
    byte_code = compile_restricted(
        code,
        filename="<string>",
        mode="exec",
    )
    data = { "_print_": PrintCollector, "__builtins__": safe_builtins }
    exec(byte_code, data, None)
    return data["results"]

class InterpreterBot(discord.Client):
    async def on_ready(self):
        print("logged in as {}".format(self.user))
    
    async def on_message(self, message):
        command_str = ">>"
        content = message.content
        if content.startswith(command_str):
            source = re.sub(r"{} ?".format(command_str), "", content, 1)
            source = re.sub(r"(?:^\"?`(?:`{2}(?:[a-zA-Z+]*)?)?\n?|\n?`(?:`{2})?\"?$)", "", source)
            print("Executed {}".format(repr(source)))
            await message.channel.send("```{}```".format(interpret(source) or "(no output to stdout)"))
    
    def run(self):
        token = os.getenv("TOKEN")
        if token:
            super().run(token)
        else:
            raise EnvironmentError("TOKEN environment variable doesn't exist")

if __name__ == "__main__":
    bot = InterpreterBot()
    bot.run()
