import uasyncio as asyncio
# from pyb import UART
# uart = UART(4, 9600)
import M
uart=M.uart()

swriter = asyncio.StreamWriter(uart, {})
async def sender():
    while True:
        await swriter.awrite('Hello uart\n')
        await asyncio.sleep(2)

sreader = asyncio.StreamReader(uart)
async def receiver():
    while True:
        res = await sreader.read(1)
        print('Recieved', res)

loop = asyncio.get_event_loop()
rs=loop.create_task(sender())
print(rs)
loop.create_task(receiver())
loop.run_forever()