from fastapi import FastAPI
from pydantic import BaseModel, root_validator


class Package(BaseModel):
    name: str
    version: str

    @root_validator
    def name_and_version_must_differ(cls, values: dict[str, str]) -> dict[str, str]:
        if values.get("name") == values.get("version"):
            raise ValueError("name and version must differ")
        return values

    class Config:
        anystr_strip_whitespace = True


app = FastAPI(title="Agentic Dependabot Repair")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/packages")
def create_package(package: Package) -> dict[str, str]:
    return package.dict()
