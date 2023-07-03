# TL; DR

Hi! Omid here ;) It was fun working on this project. Formalities aside, several points worth mentioning:

## Focus points:

What I tried to focus more on my implementation and through the 3 hours time slot:

- Showcase the feasibility of the idea.
- Parallel threading for jobs.
- Dockerizing the jobs.
- Functional UI for the MVP.
- Pooling concept for better UX.
- Dynamic input adaption in UI; based on the config files in backend.
- Dynamic docker creation on backend.

The project is a MVP, which as you mentioned _proves the feasibility of the required functionality_ but indeed on the aesthetic aspects and testing all the functionalities and corner cases, there's room for improvement. I tried my best to deliver a product in a good shape within the estimated time provided by you: **3 hours**.

## Issue points:

- On my localhost (checked on two different laptops), the _requirements.txt_ provided by you beside the scripts couldn't get installed on **docker containers**. I had to remove the _versions_ of the dependencies.

## Out of scope points:

- To add a download button for the scripts output.
- To unify the format of config files for each script.
- To use websocket instead of pooling in the front-end.
- To add a DB / key-value storage for storing the jobs information.
- To add watches for different threads, so in case of failure in any of them, we can detect the failure.
- To add input validation for HTTP requests.

# Python Job Manager

This project is a Python job management system. It uses a Python-based backend and a React-based frontend to manage and monitor Python scripts that are running as Docker containers on the server.

## Setup

To set up and run the project, you will need to have Python, Docker, Node.js, and npm installed on your system.

### Backend

The backend of this project is a Python server which controls the execution of Python jobs in Docker containers.

First, navigate to the backend directory of the project:

```
cd backend
```

Then, install the required Python packages with:

```
pip install -r requirements.txt
```

After the required Python packages are installed, you can start the server with:

```
python main.py
```

The backend server will start and listen on http://localhost:5000.

### Frontend

The frontend of this project is a React application which provides a user interface for managing the Python jobs.

First, navigate to the frontend directory of the project:

```
cd . #root folder
```

Then, install the required npm packages with:

```
npm install
```

After the required npm packages are installed, you can start the server with:

```
npm run start
```

The frontend server will start and listen on http://localhost:3000.
