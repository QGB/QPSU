import uasyncio,uaiowebrepl
loop=uasyncio.get_event_loop()
loop.create_task(uaiowebrepl.start(port=33))
loop.run_forever()
