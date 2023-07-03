# Import required libraries
import docker
import os
import time
import yaml
import json
import random
import string
from threading import Thread


class Orchestrator:
    def __init__(self):
        # Initialize Docker client
        self.client = docker.from_env()
        # Initialize job status dictionary
        self.jobs_status = {}

    # Function to generate a random ID for each job
    def generate_random_id(self):
        letters_and_digits = string.ascii_letters + string.digits
        return ''.join(random.choice(letters_and_digits) for i in range(5))

    # Function to retrieve script information from info.json file
    def get_script_info(self, script_name):
        # Read the info.json file
        with open("scripts/info.json", "r") as file:
            scripts_info = json.load(file)
        # Fetch the information for the script
        return scripts_info.get(script_name)

    # Function to run a specific job
    def run_job(self, job):
        script_name = job["script_name"]
        script_info = self.get_script_info(script_name)
        job_name = job["job_name"]

        # Scripts are assumed to be located in the scripts directory
        script_dir = os.path.join("scripts", script_name)
        requirements_path = os.path.join(script_dir, "requirements.txt")

        # Get the config file name from script_info
        config_filename = script_info.get('config_file_name', 'config.yaml')
        config_path = os.path.join(script_dir, "configs", config_filename)

        script_path = os.path.join(script_dir, "main.py")

        # Load and update the config file with job details
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)

        for key in config.keys():
            config[key] = job.get(key, config[key])

        with open(config_path, "w") as file:
            yaml.safe_dump(config, file)

        # Generate Dockerfile content
        dockerfile_content = f"""
        FROM jupyter/scipy-notebook:latest
        WORKDIR /app
        COPY . .
        RUN pip install -r requirements.txt
        CMD ["python", "main.py"]
        """

        # Write Dockerfile into script_dir
        with open(os.path.join(script_dir, 'Dockerfile'), 'w') as file:
            file.write(dockerfile_content)

        # Build Docker image using the script_dir as context
        image, build_logs = self.client.images.build(
            path=script_dir, tag=script_name.lower(), rm=True)

        # @TODO Handle error if the output folder is not created already
        volumes = {os.path.abspath(os.path.join(script_dir, 'OUTPUTS')): {
            'bind': '/app/OUTPUTS', 'mode': 'rw'}}

        # Run Docker container
        container = self.client.containers.run(
            image, detach=True, volumes=volumes)

        # Update job status in the jobs_status dictionary
        self.jobs_status[self.generate_random_id()] = {
            "job_name": job_name, "status": "running", "container_id": container.id, "script_info": script_info}

    # Function to schedule a job
    def schedule_job(self, job):
        # Start a new thread to run the job
        Thread(target=self.run_job, args=(job,)).start()

    # Function to check the status of all jobs
    def check_jobs_status(self):
        while True:
            for job_name, job_info in self.jobs_status.items():
                try:
                    container = self.client.containers.get(
                        job_info["container_id"])
                    if container.status == "exited":
                        self.jobs_status[job_name]["status"] = "finished"
                        self.jobs_status[job_name]["output"] = container.logs()
                        container.remove()
                except docker.errors.NotFound:
                    self.jobs_status[job_name]["status"] = "removed"

            # Log the status of all jobs
            print("check_job_status: ")
            print(self.jobs_status)
            # Wait for 10 seconds before checking the status again
            time.sleep(10)

    # Function to get the status of all jobs
    def get_jobs_status(self):
        return self.jobs_status

    # Function to start the Orchestrator
    def start(self):
        print("start being called ...")
        # Start a new thread to check the job status
        Thread(target=self.check_jobs_status).start()
