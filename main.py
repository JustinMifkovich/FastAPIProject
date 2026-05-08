from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

_next_id = 4
_favorites: dict[int, str] = {
    1: "google.com",
    2: "apple.com",
    3: "cnn.com",
}


class FavoriteIn(BaseModel):
    url: str


class Favorite(BaseModel):
    id: int
    url: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/favorites", response_model=list[Favorite])
async def list_favorites():
    return [Favorite(id=k, url=v) for k, v in _favorites.items()]


@app.get("/favorites/{favorite_id}", response_model=Favorite)
async def get_favorite(favorite_id: int):
    if favorite_id not in _favorites:
        raise HTTPException(status_code=404, detail="Favorite not found")
    return Favorite(id=favorite_id, url=_favorites[favorite_id])


@app.post("/favorites", response_model=Favorite, status_code=201)
async def create_favorite(body: FavoriteIn):
    global _next_id
    _favorites[_next_id] = body.url
    created = Favorite(id=_next_id, url=body.url)
    _next_id += 1
    return created


@app.put("/favorites/{favorite_id}", response_model=Favorite)
async def update_favorite(favorite_id: int, body: FavoriteIn):
    if favorite_id not in _favorites:
        raise HTTPException(status_code=404, detail="Favorite not found")
    _favorites[favorite_id] = body.url
    return Favorite(id=favorite_id, url=body.url)


@app.delete("/favorites/{favorite_id}", status_code=204)
async def delete_favorite(favorite_id: int):
    if favorite_id not in _favorites:
        raise HTTPException(status_code=404, detail="Favorite not found")
    del _favorites[favorite_id]
