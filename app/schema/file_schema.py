from pydantic import BaseModel


class FileSchema(BaseModel):
    id: int
    file_url: str

    class Config:
        orm_mode = True
