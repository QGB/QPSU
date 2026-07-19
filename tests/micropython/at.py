import uasyncio
from ws_server import WSReader, WSWriter

async def echo(reader, writer):
    # Consume GET line
    await reader.readline()

    reader = await WSReader(reader, writer)
    writer = WSWriter(reader, writer)

    while 1:
        l = await reader.read(256)
        print(l)
        if l == b"\r":
            await writer.awrite(b"\r\n")
        else:
            await writer.awrite(l)


# import ulogging as logging
#logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.DEBUG) #ImportError: no module named 'ulogging'
loop = uasyncio.get_event_loop()
loop.create_task(uasyncio.start_server(echo, "0.0.0.0", 80))
loop.run_forever()
loop.close()