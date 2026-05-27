import os
import json
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from analyzer import (
    analyze_profile,
    analyze_jd,
    generate_resume,
    generate_cover_letter,
    generate_interview_questions,
    generate_dashboard,
    save_all_files,
)
from notion_integration import add_tasks_to_notion

load_dotenv()

app = FastAPI(title="CareerCraft API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── REQUEST MODELS ───────────────────────────────────────────

class JDRequest(BaseModel):
    jd: str
    company: str
    company_org: str = ""


# ── MAIN ANALYZE ENDPOINT ────────────────────────────────────

@app.post("/analyze")
async def analyze(req: JDRequest):
    """
    Stream real-time progress logs to frontend.
    Each line is a JSON object: {type, msg/files/analysis}
    """

    async def stream():
        def log(msg: str):
            return json.dumps({"type": "log", "msg": msg}) + "\n"

        try:
            # ── Step 1: Coral queries ──
            yield log("🔍 Querying GitHub via Coral SQL...")
            await asyncio.sleep(0.1)

            profile = await asyncio.get_event_loop().run_in_executor(
                None, analyze_profile
            )

            yield log(f"✅ Found {len(profile['repos'])} repos, {len(profile['languages'])} languages")
            yield log(f"💻 Top language: {profile['languages'][0]['language'] if profile['languages'] else 'N/A'}")

            if profile['notion']:
                yield log(f"📋 Connected to Notion — {len(profile['notion'])} pages found")
            else:
                yield log("📋 Notion connected (no pages found — add pages to workspace)")

            await asyncio.sleep(0.2)

            # ── Step 2: Claude analysis ──
            yield log("🧠 Analyzing JD vs your profile with Claude...")
            await asyncio.sleep(0.1)

            analysis = await asyncio.get_event_loop().run_in_executor(
                None, analyze_jd, req.jd, profile, req.company_org
            )
            yield log("✅ Analysis complete — match score calculated")
            await asyncio.sleep(0.1)

            # ── Step 3: Generate resume ──
            yield log("📄 Generating tailored resume...")
            resume = await asyncio.get_event_loop().run_in_executor(
                None, generate_resume, req.jd, profile, analysis
            )
            yield log("✅ Resume generated")

            # ── Step 4: Cover letter ──
            yield log("✉️  Writing personalized cover letter...")
            cover = await asyncio.get_event_loop().run_in_executor(
                None, generate_cover_letter, req.jd, profile, analysis
            )
            yield log("✅ Cover letter written")

            # ── Step 5: Interview questions ──
            yield log("❓ Generating 15 interview questions...")
            questions = await asyncio.get_event_loop().run_in_executor(
                None, generate_interview_questions, req.jd, analysis
            )
            yield log("✅ Interview prep ready")

            # ── Step 6: Dashboard ──
            yield log("🎯 Building interactive career dashboard...")
            dashboard = await asyncio.get_event_loop().run_in_executor(
                None, generate_dashboard,
                req.company, req.jd, analysis, cover, questions, profile
            )
            yield log("✅ Dashboard generated")

            # ── Step 7: Save files ──
            yield log("💾 Saving all files...")
            files = save_all_files(
                req.company.lower().replace(" ", "_"),
                resume, cover, questions, dashboard
            )
            yield log(f"✅ {len(files)} files saved to output/")

            # ── Step 8: Notion integration ──
            yield log("📌 Posting 30-day plan to Notion...")
            notion_ok = await asyncio.get_event_loop().run_in_executor(
                None, add_tasks_to_notion, req.company, analysis
            )
            if notion_ok:
                yield log("✅ Tasks added to Notion database!")
            else:
                yield log("⚠️  Notion: Could not add tasks (check token + page access)")

            # ── Done ──
            yield log("🎉 Career pack complete!")
            yield json.dumps({
                "type": "done",
                "files": files,
                "analysis": analysis,
            }) + "\n"

        except Exception as e:
            yield json.dumps({"type": "error", "msg": str(e)}) + "\n"

    return StreamingResponse(stream(), media_type="text/event-stream")


# ── FILE ENDPOINTS ───────────────────────────────────────────

@app.get("/files")
async def list_files():
    """List all files in output directory"""
    output_dir = "../output"
    if not os.path.exists(output_dir):
        return {"files": []}

    files = []
    for f in sorted(os.listdir(output_dir)):
        if f.startswith("."):
            continue
        path = os.path.join(output_dir, f)
        files.append({
            "name": f,
            "size": os.path.getsize(path),
            "type": f.split(".")[-1],
        })
    return {"files": files}


@app.get("/files/{filename}")
async def get_file_content(filename: str):
    """Get text content of a file"""
    path = f"../output/{filename}"
    if not os.path.exists(path):
        return {"error": "File not found"}
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    return {"content": content, "filename": filename}


@app.get("/preview/{filename}")
async def preview_file(filename: str):
    """Serve HTML file directly in browser"""
    path = f"../output/{filename}"
    if not os.path.exists(path):
        return {"error": "File not found"}
    return FileResponse(path, media_type="text/html")


@app.get("/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}


# ── RUN ──────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)