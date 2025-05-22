import streamlit as st
import requests

st.title("🛠️ Universal Deployment File Generator")

git_url = st.text_input("🔗 GitHub Repository URL")
build_command = st.text_input("⚙️ Optional: Build Command")
run_command = st.text_input("🚀 Optional: Run Command")
use_docker_compose = st.checkbox("Generate docker-compose.yml instead of Dockerfile")

if st.button("Generate"):
    if git_url:
        with st.spinner("Generating..."):
            response = requests.post("http://localhost:8001/generate", json={
                "git_url": git_url,
                "build_command": build_command,
                "run_command": run_command,
                "use_docker_compose": use_docker_compose
            })
            if response.ok and "deployment_file" in response.json():
                st.success("✅ Deployment File Generated!")
                extension = "yaml" if use_docker_compose else "docker"
                st.code(response.json()["deployment_file"], language=extension)
            else:
                st.error("❌ Failed to generate file.")
                st.json(response.json())
