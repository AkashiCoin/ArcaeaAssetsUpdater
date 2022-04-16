"""
 - Author: DiheChen
 - Date: 2021-08-15 00:13:33
 - LastEditTime: 2021-09-01 21:39:36
 - LastEditors: DiheChen
 - Description: None
 - GitHub: https://github.com/Chendihe4975
"""
from os import listdir, path
from urllib.parse import urljoin
from urllib.request import pathname2url

from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import FileResponse
import ujson as json

from config import Config
from assets_updater import ArcaeaAssetsUpdater

app = FastAPI()
work_dir = path.abspath(
    path.join(path.dirname(__file__), "data"))
songs_dir = path.abspath(
    path.join(path.dirname(__file__), "data", "assets", "songs"))
char_dir = path.abspath(
    path.join(path.dirname(__file__), "data", "assets", "char"))
bg_dir = path.abspath(
    path.join(path.dirname(__file__), "data", "assets", "img", "bg"))

@app.get("/assets/songs/{song_id}/{file_name}")
async def _(song_id: str, file_name: str):
    if not path.exists(path.join(songs_dir, song_id)) and ("dl_" + song_id in listdir(songs_dir)):
        song_id = "".join(["dl_", song_id])
    return FileResponse(path.join(songs_dir, song_id, file_name))
    
@app.get("/assets/img/bg/{bg_name}")
async def _(bg_name: str):
    return FileResponse(path.join(bg_dir, bg_name))

@app.get("/api/version")
async def _(request: Request):
    with open(path.join(path.dirname(__file__), "data", "version.json"), "r") as file:
        return json.loads(file.read())

@app.get("/api/songlist")
async def _(request: Request):
    return FileResponse(path.join(work_dir, "songlist.json"))

@app.get("/api/slst")
async def _(request: Request):    
    return FileResponse(path.join(songs_dir, "songlist"))

@app.get("/api/songinfo")
async def _(request: Request):
    song_id = request.query_params.get("songid")
    if song_id is None:
        return {"code":"404"}
    song_info = ArcaeaAssetsUpdater.get_song_info(song_id)
    if song_info is None:
        return {"code":"404"}
    return song_info


@app.get("/api/song_list")
async def _(request: Request):
    song_dict = dict()
    for song in listdir(songs_dir):
        if path.isdir(path.join(songs_dir, song)):
            if path.exists(path.join(songs_dir, song, "base.jpg")):
                song_dict[song.replace("dl_", "")] = [urljoin(str(request.base_url), pathname2url(
                    path.join("assets", "songs", song.replace("dl_", ""), "base.jpg")))]
                if path.exists(path.join(songs_dir, song, "3.jpg")):
                    song_dict[song.replace("dl_", "")].append(urljoin(str(request.base_url), pathname2url(
                        path.join("assets", "songs", song.replace("dl_", ""), "3.jpg"))))
    return song_dict

@app.get("/api/bg_list")
async def _(request: Request):
    bg_dict = dict()
    for bg in listdir(bg_dir):
        if bg.endswith(".jpg"):
            bg_dict[bg.replace(".jpg", "")] = urljoin(str(request.base_url), pathname2url(
                path.join("assets", "img", "bg", bg)))
    return bg_dict

@app.get("/api/char_list")
async def _(request: Request):
    char_list = dict()
    for char in listdir(char_dir):
        char_list[char] = urljoin(str(request.base_url), pathname2url(
                        path.join("assets", "char", char)))
    return char_list


@app.get("/assets/char/{image_name}")
async def _(image_name: str):
    return FileResponse(path.join(char_dir, image_name))

@app.post("/api/update_songlist")
async def _(request: Request, background_tasks: BackgroundTasks):
    if "Authorization" in request.headers and request.headers["Authorization"] == Config.token:
        background_tasks.add_task(ArcaeaAssetsUpdater.update_songlist)
        return {"message": "Succeeded."}
    else:
        return {"message": "Access denied."}

@app.post("/api/force_update")
async def _(request: Request, background_tasks: BackgroundTasks):
    if "Authorization" in request.headers and request.headers["Authorization"] == Config.token:
        background_tasks.add_task(ArcaeaAssetsUpdater.force_update)
        return {"message": "Succeeded."}
    else:
        return {"message": "Access denied."}

@app.post("/api/unzip")
async def _(request: Request, background_tasks: BackgroundTasks):
    if "Authorization" in request.headers and request.headers["Authorization"] == Config.token:
        background_tasks.add_task(ArcaeaAssetsUpdater.unzip_file)
        return {"message": "Succeeded."}
    else:
        return {"message": "Access denied."}
