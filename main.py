from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from fastapi import Depends, FastAPI, HTTPException, status
from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep
import secrets

VIDEO_PATH = Path("videos/test.mp4")

app = FastAPI()
security = HTTPBasic()


class GpioStatusResponse(BaseModel):
    gpio: int
    on: bool


class SetGPIO(BaseModel):
    on: bool


@app.get("/")
async def root():
    return {"message": "Hello World"}


async def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "admin")
    correct_password = secrets.compare_digest(credentials.password, "20210555")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/video/{number}")
async def read_root(number: int, username: str = Depends(get_current_username)):
    player = OMXPlayer(VIDEO_PATH)
    sleep(5)
    player.quit()
