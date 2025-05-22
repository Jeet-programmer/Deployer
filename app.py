from fastapi import FastAPI
from pydantic import BaseModel
import tempfile, subprocess, shutil
from gemini_agent import generate_deployment_file

app = FastAPI()

class RepoRequest(BaseModel):
    git_url: str
    build_command: str | None = None
    run_command: str | None = None
    use_docker_compose: bool = False

@app.post("/generate")
def generate_file(req: RepoRequest):
    tmp_dir = tempfile.mkdtemp()
    try:
        subprocess.run(["git", "clone", req.git_url, tmp_dir], check=True)
        deployment_file = generate_deployment_file(
            tmp_dir,
            build_command=req.build_command,
            run_command=req.run_command,
            use_docker_compose=req.use_docker_compose
        )
        return {"deployment_file": deployment_file}
    except Exception as e:
        return {"error": str(e)}
    finally:
        shutil.rmtree(tmp_dir)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
