import asyncio
import json
import websockets

ROOM = "test"
BASE = f"ws://127.0.0.1:8000/ws/{ROOM}"


async def listen(name: str, ws):
    try:
        async for msg in ws:
            data = json.loads(msg)
            print(f"\n[{name}] RECV {data['type']}:")
            print(json.dumps(data, indent=2))
    except Exception as e:
        print(f"[{name}] connection closed: {e}")



async def main():
    # Connect two players
    ws1 = await websockets.connect(f"{BASE}/p1")
    ws2 = await websockets.connect(f"{BASE}/p2")

    t1 = asyncio.create_task(listen("p1", ws1))
    t2 = asyncio.create_task(listen("p2", ws2))

    # Give time for initial state broadcast
    await asyncio.sleep(0.5)

    # p1 action (must be p1's turn first in your room)
    await ws1.send(json.dumps({"type": "draw_discard"}))
    await asyncio.sleep(0.5)

    # p2 action
    await ws2.send(json.dumps({"type": "draw_discard"}))
    await asyncio.sleep(0.5)

    # cleanup
    t1.cancel()
    t2.cancel()
    await ws1.close()
    await ws2.close()


if __name__ == "__main__":
    asyncio.run(main())
