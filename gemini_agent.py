import os
import requests

def extract_project_summary(project_path):
    summary = ""

    # Include README content if present
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.lower().startswith("readme"):
                try:
                    with open(os.path.join(root, file), 'r', errors="ignore") as f:
                        readme = f.read()
                        summary += f"\n# {file}\n{readme[:3000]}"  # Truncate long READMEs
                except:
                    continue
                break  # Only include one README file

    # Include code/config files
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith((
                '.py', '.js', '.ts', '.java',
                'package.json', 'requirements.txt',
                'pom.xml', 'main.cpp'
            )):
                try:
                    with open(os.path.join(root, file), 'r', errors="ignore") as f:
                        content = f.read()
                        summary += f"\n# {file}\n" + content[:3000]
                except:
                    continue
    return summary


def generate_deployment_file(project_path, build_command=None, run_command=None, use_docker_compose=False):
    url = "http://chat.devscript.in/v1/chat/completions"

    project_summary = extract_project_summary(project_path)

    prompt = f"""
You are a DevOps assistant. Based on the following project code, generate a production-ready {"docker-compose.yml" if use_docker_compose else "Dockerfile"}.

Project Code Summary:
{project_summary}

{f"The user suggests this build command: {build_command}" if build_command else ""}
{f"The user suggests this run command: {run_command}" if run_command else ""}

Only return the complete deployment file. Do not include extra commentary.
"""

    body = {
        "model": "gpt-4o-mini",
        "stream": False,
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(url, json=body)
        response.raise_for_status()
        json_response = response.json().get('choices', [])
        return "\n".join([choice.get('message', {}).get('content', '') for choice in json_response])
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error calling GPT API: {e}")
