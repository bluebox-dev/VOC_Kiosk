# Websocket
import asyncio
import websockets
import json

async def wss(orderIDReference,point):
    uri = "ws://localhost:9001"
    async with websockets.connect(uri) as websocket:
        event = {"action": "sendPrivate","companyID": orderIDReference,"amountScore": point}
        await websocket.send(json.dumps(event))

if __name__ == "__main__":
    asyncio.run(wss("orderIDReference",2))