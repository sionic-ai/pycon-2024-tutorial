import os

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from code_search.config import ROOT_DIR
from code_search.llm.xionic import XIONIC_CLIENT
from code_search.searcher import CombinedSearcher
from code_search.get_file import FileGet

app = FastAPI()

searcher = CombinedSearcher()
get_file = FileGet()


@app.get("/api/search")
async def search(query: str):
    return {"result": searcher.search(query, limit=5)}


@app.get("/api/file")
async def file(path: str):
    return {"result": get_file.get(path)}


def create_chat_messages(question: str, contexts: list[dict]) -> list[dict[str, str]]:
    system_message = {
        "role": "system",
        "content": "You are a helpful assistant that answers questions about code based on the provided context in Korean(한국어).",
    }
    user_message = {
        "role": "user",
        "content": f"""Please answer the following question based on the provided code context:

Question: {question}

Code Context:
{contexts}""",
    }
    return [system_message, user_message]


@app.post("/api/answer")
async def answer(query: str):
    contexts: list[dict] = searcher.search(query, limit=5)
    messages: list[dict[str, str]] = create_chat_messages(query, contexts)
    response: str = await XIONIC_CLIENT.get_completion_chat(messages=messages)
    return {"result": response}


app.mount(
    "/", StaticFiles(directory=os.path.join(ROOT_DIR, "frontend", "dist"), html=True)
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
