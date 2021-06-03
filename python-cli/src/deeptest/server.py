import shutil
from logging import getLogger
from pathlib import Path
from tempfile import NamedTemporaryFile

import uvicorn
from deeptest.backend.models import Base
from deeptest.db import Db, engine, get_db
from fastapi import Depends, FastAPI, File, UploadFile
from fastapi.datastructures import UploadFile

logger = getLogger("uvicorn")

app = FastAPI()

Base.metadata.create_all(bind=engine)


def save_upload_file_tmp(upload_file: UploadFile) -> Path:
    try:
        suffix = Path(upload_file.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(upload_file.file, tmp)
            tmp_path = Path(tmp.name)
    finally:
        upload_file.file.close()
    return tmp_path


@app.post("/upload/")
async def create_upload_file(
    file: UploadFile = File(...), submit: bool = False, db: Db = Depends(get_db)
):
    path = save_upload_file_tmp(file)
    logger.info(f"wrote {path}")
    branch = ""
    repo = ""
    sha = ""

    flaky_tests = db.check_store(path, branch, repo, sha)

    if submit:
        db.store(path, branch, repo, sha)

    return {"flaky_tests": flaky_tests}


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/report")
async def report(days: int = 7):
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")
