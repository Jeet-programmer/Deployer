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

    # Continue with project files
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith((
                '.py', '.js', '.ts', '.java', '.cpp',
                'package.json', 'requirements.txt', 'pom.xml'
            )):
                try:
                    with open(os.path.join(root, file), 'r', errors="ignore") as f:
                        content = f.read()
                        summary += f"\n# {file}\n" + content[:3000]
                except:
                    continue
    return summary


def generate_dockerfile_with_gemini(project_path):
    url = "https://chat.devscript.in/v1/chat/completions"

    project_summary = extract_project_summary(project_path)

    prompt = f"""
You are a DevOps assistant. A user has submitted a project with the following file contents:

{project_summary}

Based on the contents above (including README if available), generate a production-ready Dockerfile that can run this application. 
Only output the Dockerfile.
"""

    body = {
        "model": "gpt-4o-mini",
        "stream": False,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, json=body)
        response.raise_for_status()
        json_response = response.json().get('choices', [])
        return "\n".join([choice.get('message', {}).get('content', '') for choice in json_response])
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error calling GPT API: {e}")
