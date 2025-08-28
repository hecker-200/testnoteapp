from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

conn = MongoClient('mongodb+srv://b23es1003_db_user:achu2005@cluster0.qu8fgxf.mongodb.net/')


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request, id: str | None = None):
    """Render the index.html template on the root path."""

    docs = conn.notes.notes.find({})
    newDocs = []
    for doc in docs: 
        newDocs.append({
            'id': str(doc['_id']),   # convert ObjectId to string
            'note': doc.get('note', '')  # use get() to avoid KeyError
        })

    return templates.TemplateResponse(
        'index.html',
        {'request': request, 'newDocs': newDocs}  # ✅ correct format
    )


@app.get("/items/{item_id}")
def get_item(item_id: int, q: str | None = None):
    """Return item details given its ID and optional query parameter."""
    return {"item_id": item_id, "q": q}
