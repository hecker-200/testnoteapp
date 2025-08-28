from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# MongoDB connection
conn = MongoClient('mongodb+srv://b23es1003_db_user:achu2005@cluster0.qu8fgxf.mongodb.net/')
collection = conn.notes.notes  # DB: notes, Collection: notes

@app.get("/", response_class=HTMLResponse)
async def read_notes(request: Request):
    """Render index.html with all notes"""
    docs = collection.find({})
    newDocs = []
    for doc in docs:
        newDocs.append({
            "id": str(doc["_id"]),
            "title": doc.get("title", ""),
            "desc": doc.get("desc", ""),
            "important": doc.get("important", False)
        })
    return templates.TemplateResponse("index.html", {"request": request, "newDocs": newDocs})


@app.post("/", response_class=HTMLResponse)
async def add_note(
    request: Request,
    title: str = Form(...),
    desc: str = Form(...),
    important: str | None = Form(None)
):
    """Insert a new note into MongoDB"""
    new_note = {
        "title": title,
        "desc": desc,
        "important": True if important == "on" else False
    }
    collection.insert_one(new_note)

    # Redirect back to GET "/" so the page reloads with the new note
    return RedirectResponse(url="/", status_code=303)
