FROM python:3.9-bullseye

RUN pip3 install requests

COPY evaluate.py /evaluate.py

ENTRYPOINT ["python3", "/evaluate.py"]
