from sre_parse import ANY
import time, jwt, httpx
from typing import Any, Dict, List
from .config import settings
import requests

GITLAB_API = "https://git.ringcentral.com/api/v4"


async def get_pr_diff(projectId: str, mrId: int) -> str:
    
    url =  f"{GITLAB_API}/projects/{projectId}/merge_request/{mrId}/changes"
    print("Ulr", url)
    headers={"PRIVATE-TOKEN": settings.gitlab_token}

    async with httpx.AsyncClient() as client:
        diffs = await client.get(url, headers=headers)
        diffs.raise_for_status
        diff_data = diffs.json()
        all_diffs = "\n".join([change["diff"] for change in diff_data["changes"]])
        print("Kundan-->", all_diffs)
        return all_diffs
    

async def create_review(projectId:str, mrId:str, comments:str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{GITLAB_API}/projects/{projectId}/merge_requests/{mrId}/notes",
            headers={"PRIVATE-TOKEN": settings.gitlab_token},
            data = {"body": comments}
        )

        response.raise_for_status
        if response.status_code != 201:
            print("Failed")
        else:
            print("Sucess")
