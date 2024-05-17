from fastapi import APIRouter, Cookie

from cvat.cvat import cvat_get_projects, cvat_login_user
from schemas.dataset import ProjectsSchema

router = APIRouter()

@router.get("")
async def get_all(sessionid: str = Cookie(None), csrftoken: str = Cookie(None)):
    projects = cvat_get_projects(sessionid, csrftoken)
    response = []
    for project in projects.get("results"):
        response.append(
            ProjectsSchema(
                id=project.get("id"),
                name=project.get("name"),
                created_date=project.get("created_date"),
                status=project.get("status")
            )
        )
    return response
