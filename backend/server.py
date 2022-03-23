from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from backend.main import ARDUINO_INSTRUCTION_KEY, ARDUINO_STATUS_KEY, ARDUINO_STATUS, write_instruction_arduino, sync_arduino_state
from backend.utils import take_snapshot
import threading

class BackgroundSync(threading.Thread):
    def run(self):
        sync_arduino_state()
  
app = FastAPI()

@app.get("/")
async def status():
    return {"status": ARDUINO_STATUS}

@app.get("/refresh_status")
async def refresh_status(): 
    status = write_instruction_arduino(ARDUINO_INSTRUCTION_KEY["request_status"])
    return {"status": status}

@app.get("/move")
async def move():
    if ARDUINO_STATUS == "disabled": 
        raise HTTPException(504, "Arduino isn't connected yet")

    if ARDUINO_STATUS == "ready" or ARDUINO_STATUS == "moving" : 
        raise HTTPException(504, f"Cant trigger arduino rn, its {ARDUINO_STATUS}")

    image_path = take_snapshot()
    write_instruction_arduino(ARDUINO_INSTRUCTION_KEY["trigger_move"])
    return FileResponse(image_path)

@app.get("/cancel")
async def cancel():
    if ARDUINO_STATUS in ["disabled", "ready", "moving"]: 
        return
    write_instruction_arduino(ARDUINO_INSTRUCTION_KEY["cancel_move"])
