import json

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from ai.openai_integration import get_openai_analysis
from ingest.sources import (
    get_hn_stories,
    get_lobsters_stories,
    get_slashdot_stories,
    get_trending_github_repos,
)

load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
def get_design(request: Request):
    hn_data = get_hn_stories()
    lobsters_data = get_lobsters_stories()
    slashdot_data = get_slashdot_stories()
    gh_repos = get_trending_github_repos()
    all_data = hn_data + lobsters_data + slashdot_data + gh_repos

    analysis = get_openai_analysis(json.dumps([x.model_dump_json() for x in all_data]))

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"data": all_data, "analysis": analysis},
    )


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


@app.get("/gh")
def get_gh_repos():
    data = get_trending_github_repos()
    return {"data": data}


@app.get("/ai")
def get_ai_analysis():
    lobsters_data = [x.model_dump_json() for x in get_lobsters_stories()]
    hn_data = [x.model_dump_json() for x in get_hn_stories()]
    slashdot_data = [x.model_dump_json() for x in get_slashdot_stories()]
    gh_repos = [x.model_dump_json() for x in get_trending_github_repos()]
    all_data = hn_data + lobsters_data + slashdot_data + gh_repos
    ai_analysis = get_openai_analysis(json.dumps(all_data))
    return HTMLResponse(ai_analysis)
