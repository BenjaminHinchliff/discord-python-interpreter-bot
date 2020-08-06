import os
import ast

import dotenv
import discord
from discord.ext import commands
from RestrictedPython import compile_restricted, safe_builtins
from RestrictedPython.PrintCollector import PrintCollector

dotenv.load_dotenv()

@commands.command()
async def interpret(ctx, code):
    code = code.replace("`", "")
    code += "\nresults = printed"
    try:
        print(code)
        byte_code = compile_restricted(
            code,
            filename="<string>",
            mode="exec",
        )
        data = { "_print_": PrintCollector, "__builtins__": safe_builtins }
        exec(byte_code, data, None)
        await ctx.send("```{}```".format(data["results"]))
    except SyntaxError as e:
        await ctx.send("syntax error: {}".format(e))

class InterpreterBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="~")
        self.add_command(interpret)
    
    def run(self):
        super().run(os.getenv("TOKEN"))

if __name__ == "__main__":
    bot = InterpreterBot()
    bot.run()
