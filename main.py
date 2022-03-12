import os
import ast
import re
import multiprocess
from pathos.multiprocessing import ProcessPool

import dotenv
import discord
from discord.ext import commands
import RestrictedPython
from RestrictedPython import compile_restricted, limited_builtins, safe_builtins, utility_builtins
from RestrictedPython.PrintCollector import PrintCollector

dotenv.load_dotenv()

def interpret(code):
    """Interprets the given python code inside a safe execution environment"""
    code += "\nresults = printed"
    byte_code = compile_restricted(
        code,
        filename="<string>",
        mode="exec",
    )
    data = { 
        "_print_": PrintCollector,
        "__builtins__": {
            **limited_builtins,
            **safe_builtins,
            **utility_builtins,
            "all": all,
            "any": any,
            "_getiter_": RestrictedPython.Eval.default_guarded_getiter,
            "_iter_unpack_sequence_": RestrictedPython.Guards.guarded_iter_unpack_sequence
        },
        "_getattr_": RestrictedPython.Guards.safer_getattr
    }
    exec(byte_code, data, None)
    return data["results"]

class InterpreterBot(discord.Client):
    def __init__(self):
        super().__init__()
        self.pool = ProcessPool(nodes=4)

    async def on_ready(self):
        print("logged in as {}".format(self.user))
    
    async def on_message(self, message):
        command_str = ">>"
        content = message.content
        if content.startswith(command_str):
            # remove the command prefix itself and (maybe) a space
            source = re.sub(r"{} ?".format(command_str), "", content, 1)
            # remove code markers so code boxes work with this "beautiful" regex
            source = re.sub(r"(^`{1,3}(py(thon)?)?|`{1,3}$)", "", source)
            # log output to help debugging on failure
            print("Executed {}".format(repr(source)))
            sent = await message.channel.send("running code...")
            result = self.pool.apipe(interpret, source)
            output = None
            try:
                output = result.get(timeout=10)
            except multiprocess.context.TimeoutError:
                output = "Timeout error - do you have an infinite loop?"
            except Exception as e:
                output = "Runtime error: {}".format(e)
            await sent.edit(content="```\n{}```".format(output or "(no output to stdout)"))
    
    def run(self):
        token = os.getenv("TOKEN")
        if token:
            super().run(token)
        else:
            raise EnvironmentError("TOKEN environment variable doesn't exist")

if __name__ == "__main__":
    bot = InterpreterBot()
    bot.run()
