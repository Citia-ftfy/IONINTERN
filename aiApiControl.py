import subprocess
import zmq
import base64
import argparse
import time
import array
import json
import requests
import io
import base64
import sheetsCollector as sC
from PIL import Image, PngImagePlugin

parser = argparse.ArgumentParser()


parser.add_argument('-sip','--serverPort',type=str, default = "7860")
parser.add_argument('-steps','--steps',type=int, default = 20)
parser.add_argument('-styles','--styles',type=str, nargs='*', default=[""])
parser.add_argument('-prompt','--prompt', type=str, nargs='*',default=["Sunset"])
parser.add_argument('-gapi','--googleAPI',action="store_true")



args = parser.parse_args()


url = "http://127.0.0.1:"
url+=args.serverPort
pompyN = ""
if(args.googleAPI):
    pompy, pompyN = sC.grab()
else:
    pompy = args.prompt
prompt = ""

option_payload = {
    "sd_model_checkpoint": "v2-1_768-ema-pruned.safetensors [dcd690123c]",
    "CLIP_stop_at_last_layers": 2
}

response = requests.post(url=f'{url}/sdapi/v1/options', json=option_payload)

for s in pompy:
    prompt+=(s+" ")


payload = {
    "prompt": prompt,
    "steps": args.steps,
    "styles": args.styles,
    "sampler_index": "DDIM"
}

response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)

r = response.json()

for i in r['images']:
    image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))

    png_payload = {
        "image": "data:image/png;base64," + i
    }
    response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)

    pnginfo = PngImagePlugin.PngInfo()
    pnginfo.add_text("parameters", response2.json().get("info"))
    image.save('output.png', pnginfo=pnginfo)