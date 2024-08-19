import json

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from youtube_transcript_api._errors import TranscriptsDisabled
from ai import prompts
from ai.openai_integration import analyze_with_openai
from ingest import sources

load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
def get_design(request: Request):
    hn_data = sources.sources.get_hn_stories()
    lobsters_data = sources.sources.get_lobsters_stories()
    slashdot_data = sources.get_slashdot_stories()
    gh_repos = sources.get_trending_github_repos()
    all_data = hn_data + lobsters_data + slashdot_data + gh_repos

    analysis = analyze_with_openai(
        system_prompt=prompts.news_summarizer,
        prompt=json.dumps([x.model_dump_json() for x in all_data]),
    )

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"data": all_data, "analysis": analysis},
    )


@app.get("/hn")
def get_hn():
    data = sources.get_hn_stories()
    return {"data": data}


@app.get("/lobsters")
def get_lobsters():
    data = sources.get_lobsters_stories()
    return {"data": data}


@app.get("/slashdot")
def get_slashdot():
    data = sources.get_slashdot_stories()
    return {"data": data}


@app.get("/gh")
def get_gh_repos():
    data = sources.get_trending_github_repos()
    return {"data": data}


@app.get("/yt/{video_id}")
def get_yt_transcript(video_id: str):
    data = sources.get_yt_video_transcript(video_id)
    return {"data": data}


@app.get("/yt-ai/{video_id}")
def get_yt_transcript_ai_analysis(video_id: str):
    data = sources.get_yt_video_transcript(video_id)
    ai_analysis = analyze_with_openai(
        system_prompt=prompts.yt_transcripts_summarizer, prompt=json.dumps(data)
    )
    return HTMLResponse(ai_analysis)


@app.get("/yt-comments/{video_id}")
def get_yt_comments_data(video_id: str):
    data = sources.get_yt_comments(video_id)
    return {"data": data}


@app.get("/yt-ai-comments/{video_id}")
def get_yt_transcript_and_comments_ai_analysis(video_id: str):
    try:
        data = sources.get_yt_video_transcript(video_id)
    except TranscriptsDisabled:
        return {"Error": "Could not retrieve YouTube transcript"}
    comments = " ".join(item for item in sources.get_yt_comments(video_id))
    all_data = data + "\n" + "Comments:" + " " + comments
    ai_analysis = analyze_with_openai(
        system_prompt=prompts.yt_transcripts_and_comments_summarizer,
        prompt=json.dumps(all_data),
    )
    return HTMLResponse(ai_analysis)


@app.get("/ai")
def get_ai_analysis():
    lobsters_data = [x.model_dump_json() for x in sources.get_lobsters_stories()]
    hn_data = [x.model_dump_json() for x in sources.get_hn_stories()]
    slashdot_data = [x.model_dump_json() for x in sources.get_slashdot_stories()]
    gh_repos = [x.model_dump_json() for x in sources.get_trending_github_repos()]
    all_data = hn_data + lobsters_data + slashdot_data + gh_repos
    ai_analysis = analyze_with_openai(
        system_prompt=prompts.news_summarizer, prompt=json.dumps(all_data)
    )
    return HTMLResponse(ai_analysis)
