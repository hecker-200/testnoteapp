from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from config.db import collection

note = APIRouter()
templates = Jinja2Templates(directory="templates")


@note.get("/", response_class=HTMLResponse)
async def read_notes(request: Request):
    """Render all notes from MongoDB in index.html"""
    docs = collection.find({})
    new_docs = []
    for doc in docs:
        new_docs.append({
            "id": str(doc["_id"]),
            "note": f"{doc.get('title','')} - {doc.get('desc','')}"
        })

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "newDocs": new_docs}
    )


@note.post("/", response_class=HTMLResponse)
async def add_note(request: Request, title: str = Form(...), desc: str = Form(...)):
    """Handle POST request from form to add a new note"""
    new_note = {
        "title": title,
        "desc": desc,
        "important": False
    }
    collection.insert_one(new_note)
    # After inserting, render updated list
    docs = collection.find({})
    new_docs = []
    for doc in docs:
        new_docs.append({
            "id": str(doc["_id"]),
            "note": f"{doc.get('title','')} - {doc.get('desc','')}"
        })
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "newDocs": new_docs}
    )
