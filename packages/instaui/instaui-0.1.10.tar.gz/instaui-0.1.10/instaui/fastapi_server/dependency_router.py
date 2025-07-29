from fastapi import FastAPI
from fastapi.responses import FileResponse

from instaui.fastapi_server import resource


URL = f"{resource.URL}/{{hash_part:path}}/{{file_name:path}}"


def create_router(app: FastAPI):
    _dependency_handler(app)


def _dependency_handler(app: FastAPI):
    @app.get(URL)
    def _(hash_part: str, file_name: str) -> FileResponse:
        folder = resource.get_folder_path(hash_part)
        local_file = folder / file_name

        return FileResponse(
            local_file, headers={"Cache-Control": "public, max-age=3600"}
        )
