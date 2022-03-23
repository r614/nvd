from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from backend.main import ARDUINO_INSTRUCTION_KEY, get_arduino_status, write_instruction_arduino, sync_arduino_state
from backend.utils import take_snapshot
import threading
import uvicorn 



class BackgroundSync(threading.Thread):
    def run(self, *args,**kwargs):
        sync_arduino_state()
  
app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
    max_age=3600,
)

@app.get("/")
async def status():
    return {"status": get_arduino_status()}

@app.get("/refresh_status")
async def refresh_status(): 
    status = write_instruction_arduino(ARDUINO_INSTRUCTION_KEY["request_status"])
    return {"status": status}

@app.get("/move")
async def move():
    if get_arduino_status() == "disabled": 
        raise HTTPException(504, "Arduino isn't connected yet")

    if get_arduino_status() == "ready" or get_arduino_status() == "moving" : 
        raise HTTPException(504, f"Cant trigger arduino rn, its {get_arduino_status()}")

    image_path = take_snapshot()
    write_instruction_arduino(ARDUINO_INSTRUCTION_KEY["trigger_move"])
    return FileResponse(image_path)

@app.get("/cancel")
async def cancel():
    if get_arduino_status() in ["disabled", "ready", "moving"]: 
        return
    write_instruction_arduino(ARDUINO_INSTRUCTION_KEY["cancel_move"])


if __name__ == "__main__": 
    sync_service = BackgroundSync()
    sync_service.start()
    uvicorn.run(app, host="0.0.0.0", port=8010)