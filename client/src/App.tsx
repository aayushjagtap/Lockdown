import { useMemo, useRef, useState } from "react";
import "./App.css";

type ServerMsg =
  | { type: "state"; payload: any }
  | { type: "error"; payload: { message: string } }
  | { type: "info"; payload: any };

export default function App() {
  const [roomId, setRoomId] = useState("test");
  const [playerId, setPlayerId] = useState("p1");
  const [connected, setConnected] = useState(false);
  const [lastMsg, setLastMsg] = useState<ServerMsg | null>(null);
  const [err, setErr] = useState<string | null>(null);

  const [selectedIndex, setSelectedIndex] = useState<number | null>(null);

  const wsRef = useRef<WebSocket | null>(null);

  // Server sends the per-player snapshot as payload
  const state = useMemo(() => {
    if (!lastMsg || lastMsg.type !== "state") return null;
    return lastMsg.payload;
  }, [lastMsg]);

  function connect() {
    setErr(null);
    setSelectedIndex(null);

    const url = `ws://127.0.0.1:8000/ws/${roomId}/${playerId}`;
    const ws = new WebSocket(url);

    ws.onopen = () => setConnected(true);
    ws.onclose = () => setConnected(false);
    ws.onerror = () => setErr("WebSocket error (check server + room)");
    ws.onmessage = (ev) => {
      const msg: ServerMsg = JSON.parse(ev.data);
      setLastMsg(msg);
      if (msg.type === "error") setErr(msg.payload.message);
    };

    wsRef.current = ws;
  }

  function send(action: any) {
    if (!wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) {
      setErr("Not connected");
      return;
    }
    wsRef.current.send(JSON.stringify(action));
  }

  return (
    <div
      style={{
        maxWidth: 900,
        margin: "40px auto",
        fontFamily: "Inter, system-ui, sans-serif",
      }}
    >
      <h1>Lockdown</h1>

      <div style={{ display: "flex", gap: 12, alignItems: "center", marginBottom: 16 }}>
        <label>
          Room:
          <input value={roomId} onChange={(e) => setRoomId(e.target.value)} />
        </label>
        <label>
          Player:
          <input value={playerId} onChange={(e) => setPlayerId(e.target.value)} />
        </label>
        <button onClick={connect} disabled={connected}>
          {connected ? "Connected" : "Connect"}
        </button>
      </div>

      {err && <div style={{ color: "crimson", marginBottom: 12 }}>Error: {err}</div>}

      {state ? (
        <>
          <h3>Game State</h3>
          <div>
            Current Player: <b>{state.turn.current_player}</b>
          </div>
          <div>
            Discard Top: <b>{state.discard_top ?? "(empty)"}</b>
          </div>

          <h3>Your Cards</h3>
          <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginBottom: 8 }}>
            {(state.you?.cards ?? []).map((c: string, i: number) => {
              const selected = selectedIndex === i;
              return (
                <button
                  key={i}
                  onClick={() => setSelectedIndex(i)}
                  style={{
                    padding: "10px 14px",
                    border: selected ? "2px solid #fff" : "1px solid #aaa",
                    borderRadius: 8,
                    background: selected ? "#222" : "#111",
                    color: "#fff",
                    cursor: "pointer",
                    minWidth: 54,
                    textAlign: "center",
                  }}
                  title={`Select card index ${i}`}
                >
                  {c}
                </button>
              );
            })}
          </div>

          <div style={{ opacity: 0.75, marginBottom: 12 }}>
            Selected index: <b>{selectedIndex ?? "(none)"}</b>
          </div>

          <h3>Players</h3>
          <ul>
            {Object.entries(state.players).map(([pid, p]: any) => (
              <li key={pid}>
                <b>{pid}</b>: {p.card_count} cards {p.called_lockdown ? "(lockdown)" : ""}
                {pid === state.you?.id ? " (you)" : ""}
              </li>
            ))}
          </ul>

          <h3>Actions</h3>
          <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
            <button onClick={() => send({ type: "draw_discard" })}>Draw → Discard</button>

            <button
              onClick={() => {
                if (selectedIndex === null) return setErr("Select one of your cards first");
                send({ type: "draw_swap", card_index: selectedIndex });
              }}
            >
              Draw → Swap (selected)
            </button>

            <button
              onClick={() => {
                if (selectedIndex === null) return setErr("Select one of your cards first");
                send({ type: "take_discard_swap", card_index: selectedIndex });
              }}
            >
              Take Discard → Swap (selected)
            </button>

            <button onClick={() => send({ type: "call_lockdown" })}>Call Lockdown</button>
          </div>

          <div style={{ marginTop: 10, opacity: 0.7 }}>
            Tip: Only the <b>current player</b> can use draw/swap actions. The server will return an error if it’s not
            your turn.
          </div>
        </>
      ) : (
        <div>Connect to see game state.</div>
      )}
    </div>
  );
}
