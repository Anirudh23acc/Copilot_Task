import hashlib

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class GenerateRequest(BaseModel):
	text: str


# FastAPI validates the JSON body against GenerateRequest and returns 422 if text is missing or not a string.
@app.post("/generate")
def generate(request: GenerateRequest) -> dict[str, str]:
	# hashlib works on bytes, so encode the text as UTF-8 before hashing.
	checksum = hashlib.sha256(request.text.encode("utf-8")).hexdigest()
	# FastAPI serializes the returned dict to a JSON response.
	return {"checksum": checksum}