from __future__ import annotations

import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.api.models import ActionRequest
from app.api.rooms import RoomManager
from app.game.actions import TurnActions

router = APIRouter()
rooms = RoomManager()


@router.websocket("/ws/{room_id}/{player_id}")
async def ws_room(websocket: WebSocket, room_id: str, player_id: str):
    await websocket.accept()

    try:
        room = rooms.get_room(room_id)
    except RuntimeError:
        await websocket.send_json({"type": "error", "payload": {"message": "Room not found"}})
        await websocket.close()
        return

    room.sockets.add(websocket)

    async def broadcast_state():
        msg = {
            "type": "state",
            "payload": {
                "state": room.snapshot_public(),
                "result": room.maybe_result(),
            },
        }
        dead = []
        for ws in list(room.sockets):
            try:
                await ws.send_json(msg)
            except Exception:
                dead.append(ws)
        for ws in dead:
            room.sockets.discard(ws)

    await broadcast_state()

    try:
        while True:
            raw = await websocket.receive_text()
            data = json.loads(raw)
            action = ActionRequest(**data)

            async with room.lock:
                actions = TurnActions(room.state)
                try:
                    if action.type == "draw_discard":
                        actions.draw_and_discard(player_id)
                    elif action.type == "draw_swap":
                        if action.card_index is None:
                            raise RuntimeError("card_index required")
                        actions.draw_and_swap(player_id, action.card_index)
                    elif action.type == "take_discard_swap":
                        if action.card_index is None:
                            raise RuntimeError("card_index required")
                        actions.take_discard_and_swap(player_id, action.card_index)
                    elif action.type == "call_lockdown":
                        room.state.call_lockdown(player_id)
                    else:
                        raise RuntimeError("Unknown action type")

                    await broadcast_state()

                except Exception as e:
                    await websocket.send_json({"type": "error", "payload": {"message": str(e)}})

    except WebSocketDisconnect:
        room.sockets.discard(websocket)
