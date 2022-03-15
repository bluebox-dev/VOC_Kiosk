import asyncio
import websockets

async def hello(websocket):
 name = await websocket.recv()
 print(name)

start_server = websockets.serve(hello, 'localhost', 9001)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
