FROM python:3

LABEL maintainer = "danbernstein94@gmail.com"

COPY ./requirements.txt /app/requirements.txt

# Set the working directory to /app
WORKDIR /app

RUN pip install -r requirements.txt
RUN pip install git+https://github.com/timothymugayi/boto3-sqs-extended-client-lib.git

# Copy the current directory contents into the container at /app
COPY . /app

# install the package contained in the container
RUN pip install -e .

CMD ["python", "/app/task.py"]
