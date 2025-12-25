from fastapi import FastAPI
from app.api.ws import router, rooms

app = FastAPI(title="Lockdown Server")
app.include_router(router)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/rooms/{room_id}")
def create_room(room_id: str):
    # temporary: fixed 4 players for initial testing
    rooms.create_room(room_id, ["p1", "p2", "p3", "p4"], seed=1)
    return {"room_id": room_id, "players": ["p1", "p2", "p3", "p4"]}
