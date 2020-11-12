This repository contains the code to capture image frames from either video ('.mp4', '.stream', .etc.) or image frame sources ('.jpg', '.png').

Please note that numerous adjustments have been made to make the code easy to run outside of the AWS cloud environment that it was originally written for. Anywhere where the 'LOCAL' variable is used throughout the `task.py` script is intended to make it easier; however, all of these `LOCAL` alternatives would be removed in a fully operational data pipeline. When run locally (artifically enforced using the 'LOCAL' variable in `task.py`), files will be saved to the directory the script is run from to demonstrate the output.


To download this repository to your local computer, run the following commands:

```
git clone https://github.com/danbernstein/sl-example.git
cd sl-example
```


To run the script as a python script in your local environment:

```
pip install -r requirements.txt
python task.py
```

To run the script as a docker container, confirm that you have Docker installed. Then run the following commands from the command line:

```
docker build -t capture_image .
docker run -d --name capture_container capture_image 
```

To see the container logs, run:

```
docker logs capture_container
```

To clean up the container, run:

```
docker stop capture_container && docker rm capture_container
```


