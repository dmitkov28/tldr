import json

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from ai.openai_integration import get_openai_analysis
from ingest.sources import get_hn_stories, get_lobsters_stories, get_slashdot_stories

load_dotenv()

app = FastAPI()


@app.get("/")
def main():
    return {"Hello": "world"}


@app.get("/hn")
def get_hn():
    data = get_hn_stories()
    return {"data": data}


@app.get("/lobsters")
def get_lobsters():
    data = get_lobsters_stories()
    return {"data": data}


@app.get("/slashdot")
def get_slashdot():
    data = get_slashdot_stories()
    return {"data": data}


@app.get("/ai")
def get_ai_analysis():
    lobsters_data = [x.model_dump_json() for x in get_lobsters_stories()]
    hn_data = [x.model_dump_json() for x in get_hn_stories()]
    slashdot_data = [x.model_dump_json() for x in get_slashdot_stories()]
    all_data = hn_data + lobsters_data + slashdot_data
    ai_analysis = get_openai_analysis(json.dumps(all_data))
    return HTMLResponse(ai_analysis)
