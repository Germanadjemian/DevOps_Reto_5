import uvicorn
import json
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API activa"}

@app.post("/add/{note}")
def add_note(note: str):
    try:
        with open("notes.json", "r") as f:
            notes = json.load(f)
    except:
        notes = []

    notes.append(note)

    with open("notes.json", "w") as f:
        json.dump(notes, f)

    return {"message": "Nota agregada", "total": len(notes)}

@app.get("/list")
def list_notes():
    try:
        with open("notes.json", "r") as f:
            notes = json.load(f)
    except:
        notes = []

    return {"notes": notes}