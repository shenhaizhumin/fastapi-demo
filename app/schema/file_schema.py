from pydantic import BaseModel


class FileSchema(BaseModel):
    id: int
    file_url: str
