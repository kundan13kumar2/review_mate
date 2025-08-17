from typing import List, Dict

from httpx import get
from . import github_client as gh
from .config import settings


def _lang_from_path(p: str) -> str | None:
    if p.endswith(".java"): return "Java"
    return None


def _hunk_start_line(patch: str | None) -> int | None:
    if not patch: return None

    import re
    m = re.search(r"@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@", patch)
    return int(m.group(1)) if m else None

async def review_pull_request(repo_full_name: str, pr_number: int):
    owner, repo = repo_full_name.split("/" , 1)
    pr = await gh.get_pr_metadata(owner, repo, pr_number)

    from .ai_client import review_file, summarize_pr
    #summary = await summarize_pr(pr['title'], pr['body'])
    #print(summary)
    summary=''

    files: List[Dict] = [
        f for f in await gh.list_pr_files(owner, repo, pr_number)
        if f['status'] != "removed"
    ][: settings.review_max_files]
    comments: list[dict] = []

    print(files)
    for f in files:
        patch = f.get('patch')
        print(patch)
        if not patch or len(patch) > settings.review_max_patch_chars:
            continue

        lang = _lang_from_path(f.get('filename'))
        
        review = await review_file(
            file_path = f["filename"],
            patch = patch,
            language_hint = lang,
            repo_ctx=f'{pr["base"]["repo"]["full_name"]}&{pr["base"]["ref"]} -> {pr["head"]["ref"]}' 
        )

        if not review:
            continue
        line = _hunk_start_line(patch) or 1
        comments.append({
            "path": f["filename"],
            "line": line,
            "body": f"**AI Review - {f['filename']}**\n{review}"
        })

    body = f"### AI Review Summary \n{summary}\n\n> Model: {settings.openai_model}\n Files reviewed: {len(comments)}/{len(files)}"
    if comments:
        await gh.create_review(owner, repo, pr_number, body, comments)