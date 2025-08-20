from openai import OpenAI
from .config import settings

client = OpenAI(api_key=settings.open_ai_key)

SYSTEM = ("You are a seasoned code reviewer. Focus on correctness, bugs,"
" performance, readability. You have to review only added or modified lines. If MR has deleted line, make sure it is not impacting other place."
" If any comments, please put comments below the line.")

async def review_file(prompt: list[str], file_path: str, patch: str, language_hint: str | None, repo_ctx: str | None) -> str:
    user = "\n".join([
        f"file:{file_path}",
        f"Language:{language_hint}" if language_hint else "",
        f"Repo context:{repo_ctx}" if repo_ctx else "",
        "Patch (unified diff):",
        patch
    ])

    # Use runtime prompt if provided, otherwise fall back to the default SYSTEM prompt
    if not prompt:
        system_content = SYSTEM
    else:
        system_content = "Developer Instructions\n"+"\n".join(f"- {p}" for p in prompt)

    resp = client.chat.completions.create(
        model=settings.openai_model,
        temperature=0.2,
        messages=[{"role":"system", "content": system_content},{"role":"user", "content":user}]
    )

    return (resp.choices[0].message.content or "").strip()

async def summarize_pr(title: str, body: str | None) -> str:
    resp = client.chat.completions.create(
        model=settings.openai_model,
        temperature=0.2,
        messages=[
            {"role":"system", "content":"Summarize the PR in ~5 bullets for a busy reviewer"},
            {"role":"user", "content":f"Title: {title}\nBody:\n{body or ''}"}
            ]
    )

    return (resp.choices[0].message.content or "").strip()
