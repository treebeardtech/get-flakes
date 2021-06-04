import shutil
from datetime import datetime, timedelta
from logging import getLogger
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import List

import uvicorn
from get-flakes.backend.models import Base
from get-flakes.db import Db, FlakyTest, engine, get_db
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


@app.post("/repo/{provider}/{owner}/{repo}/{sha}/upload/")
async def create_upload_file(
    provider: str,
    owner: str,
    repo: str,
    sha: str,
    file: UploadFile = File(...),
    db: Db = Depends(get_db),
):
    path = save_upload_file_tmp(file)
    logger.info(f"wrote {path}")
    branch = ""
    flaky_tests = db.store(path, branch, f"{provider}/{owner}/{repo}", sha)

    return {"flaky_tests": flaky_tests}


@app.get("/")
async def root():
    return {"message": "Hello World"}


def make_report(days: int, flakes: List[FlakyTest]):
    report = f"""# Flaky Tests from the last {days} days

{len(flakes)} testcases logged both passing and failing statuses on a single commit.
"""

    for ft in flakes:
        report += f" * {ft.class_name}:{ft.test_name}\n"
        for ff in ft.runs:
            report += f"    * {ff.date} {ff.sha}\n"

    return report


@app.get("/repo/{provider}/{owner}/{repo}/report")
async def report(
    provider: str, owner: str, repo: str, days: int = 7, db: Db = Depends(get_db)
):
    start = datetime.now() - timedelta(days=days)
    flakes = db.get_flakes(f"{provider}/{owner}/{repo}", start)
    return make_report(days, flakes)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")
