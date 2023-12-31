import gradio as gr
import os
import requests

from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse
from modules import script_callbacks

extensions_path = __file__.split("/extensions",1)[0]
self_folder = os.path.join(extensions_path,"extensions/sd_t2icall")
with open(os.path.join(self_folder,"easy_ui.html"),"r") as f:
    t2icall_html = f.read()

def on_ui_tabs():
    with gr.Blocks(analytics_enabled=False) as ui_component:
        with gr.Column():
            pass
        return [(ui_component, "t2icall", "t2icall")]
    
def on_app_started(_: gr.Blocks, app: FastAPI) -> None:
    @app.get("/t2icall/easy_ui.html",response_class=HTMLResponse)
    def welcome():
        return t2icall_html

    @app.post("/t2icall/api/generate")
    def t2icall(data:dict,request: Request):
        tgt_url = request.headers.get("Tgt-Url").strip()
    #    tgt_url = request.headers.get("Tgt_Url")
    #    if tgt_url : 
    #        tgt_url = tgt_url.strip()
        if "init_images" in data:
            response = requests.post(f"{tgt_url}sdapi/v1/img2img",json=data)
        else:
            response = requests.post(f"{tgt_url}sdapi/v1/txt2img",json=data)
        if response.status_code == 200:
            return response.json()["images"][0]
        raise ConnectionError
    @app.get("/t2icall/api/easyGetOptions")
    def getUpscaler(request: Request):
        tgt_url = request.headers.get("Tgt-Url").strip()
  #      tgt_url = request.headers.get("Tgt_Url")
   #     if tgt_url is not None:
 #           tgt_url = Tgt_Url.strip()
        response = requests.get(tgt_url)
        if response.status_code == 200 and tgt_url.endswith("upscalers"):
            return ",".join([upscaler["name"] for upscaler in response.json() if upscaler["name"] !="None"])
        elif response.status_code == 200 and tgt_url.endswith("sd-vae"):
            return ",".join(["default"] + [model["model_name"] for model in response.json() if model] + ["None","Automatic"])
            
    @app.get("/t2icall/api/getForwarding")
    def getForwarding(request: Request):
        tgt_url = request.headers.get("Tgt-Url").strip()
        response = requests.get(tgt_url)
        return response.json()     
script_callbacks.on_ui_tabs(on_ui_tabs)
script_callbacks.on_app_started(on_app_started)
