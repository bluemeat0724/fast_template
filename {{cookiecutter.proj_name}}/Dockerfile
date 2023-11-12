ARG python_version=3.10-slim-buster
FROM python:$python_version
MAINTAINER G
LABEL version="1.0"
LABEL description="{{cookiecutter.proj_name}}"
# Set the working directory in the container to /app
WORKDIR /app

COPY ./ ./

RUN pip install -i https://mirrors.ustc.edu.cn/pypi/web/simple pip -U && \
    pip config set global.index-url https://mirrors.ustc.edu.cn/pypi/web/simple

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
#EXPOSE 8007

ENV MODE=dev

#ENTRYPOINT ["python", "-m", "init_db.py"]

# Run the command to start Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8007"]

