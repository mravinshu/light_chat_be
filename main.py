import asyncio
import websockets


async def hello(websocket, path):
    print("Connected", websocket, path)
    name = await websocket.recv()
    print(f"< {name}")

    await sendReply(websocket, path)


async def sendReply(websocket, path):
    reply = input("Reply: ")
    await websocket.send(reply)

start_server = websockets.serve(hello, "192.168.31.206", 8765)
print("Server started with url " + "ws://192.168.31.206:8765")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
