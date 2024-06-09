from fastapi import APIRouter, Cookie, status, HTTPException

from cvat.cvat import cvat_get_projects, cvat_delete_project
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


@router.delete("/{dataset_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dataset(
    dataset_id: int, 
    sessionid: str = Cookie(None), 
    csrftoken: str = Cookie(None)
):
    code = cvat_delete_project(dataset_id=dataset_id,
                        sessionid=sessionid,
                        csrftoken=csrftoken)
    if code != 204:
        raise HTTPException(status_code=code, detail='error')