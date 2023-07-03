# Import necessary modules
from flask import Flask, request, jsonify
import json
from modules.orchestrator import Orchestrator

# Create Flask app instance
app = Flask(__name__)
# Create Orchestrator instance
orchestrator = Orchestrator()

# Start the Orchestrator job status checker thread
orchestrator.start()

# Endpoint for creating a new job


@app.route("/api/v1/script", methods=["POST"])
def new_job():
    # Extract the job from the request
    job = request.json
    # Schedule the job through the orchestrator
    orchestrator.schedule_job(job)
    # Return a response with a success message
    return jsonify({"message": "Job scheduled"}), 201

# Endpoint for fetching script names


@app.route('/api/v1/script_names', methods=['GET'])
def get_script_names():
    # Load the info.json file containing script details
    with open("scripts/info.json", "r") as file:
        scripts_info = json.load(file)

    # Extract the script names and associated arguments
    scripts_data = [
        {
            "script_name": script_name,
            "arguments": script_info.get("arguments", [])
        }
        for script_name, script_info in scripts_info.items()
    ]

    # Return the script names and arguments as JSON
    return jsonify(scripts_data)

# Endpoint for getting all jobs


@app.route("/api/v1/script", methods=["GET"])
def get_jobs():
    # Get the job status from the orchestrator
    jobs_status = orchestrator.get_jobs_status()

    # Log the job status
    print("get_jobs: ")
    print(jobs_status)

    # Create a list of jobs with desired details
    jobs_list = [
        {
            "job_name": job_info["job_name"],
            "status": job_info["status"],
            "description": job_info["script_info"]["description"],
            "author": job_info["script_info"]["author"]
        }
        for _, job_info in jobs_status.items()
    ]

    # Return the list of jobs as JSON
    return jsonify(jobs_list), 200


# Run the app
if __name__ == '__main__':
    # Use debug mode during development
    app.run(debug=True)
