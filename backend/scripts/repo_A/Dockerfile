
        FROM jupyter/scipy-notebook:latest
        WORKDIR /app
        COPY . .
        RUN pip install -r requirements.txt
        CMD ["python", "main.py"]
        