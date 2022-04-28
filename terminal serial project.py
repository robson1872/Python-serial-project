import asyncio
import aioserial
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import CompleteStyle, prompt
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.shortcuts import PromptSession
from pytest import Session

cmd_completer = WordCompleter(
    [
        "cmd send",
    ],
    meta_dict={
        "cmd send": "Is a command to send a message.",
    },
    ignore_case=True,
)

async def read_and_print(aioserial_instance: aioserial.AioSerial):
    while True:
        data: bytes = await aioserial_instance.read_async()
        print(data.decode(errors='ignore'), end='', flush=True)
        #if b'\n' in data:
        #    aioserial_instance.close()
        #    break

async def writee(aioserial_instance: aioserial.AioSerial):
    session = PromptSession("$- ", completer=cmd_completer, complete_style=CompleteStyle.MULTI_COLUMN, complete_in_thread=True)
    while True:
        curr = await session.prompt_async()
        line = str(curr)
        if(line == "exit"):
            break
        line += '\r\n'
        size = len(line)
        if(size != b'\x00'): 
            await aioserial_instance.write_async(line.encode())
            await asyncio.sleep(0.1);        
    aioserial_instance.close()
    
async def main():
    porta = input("Type the port: ")
    baudratee = input("Type the baudrate: ")
    aioserial_instance: aioserial.AioSerial = aioserial.AioSerial(port= porta, baudrate=baudratee)
    print("The conection is ready!\n")
    await asyncio.gather(read_and_print(aioserial_instance),writee(aioserial_instance))

asyncio.run(main())