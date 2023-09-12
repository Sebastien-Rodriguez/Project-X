FROM python:3.10-slim

COPY requierement.txt .
RUN apt update -y
RUN pip install -r requierement.txt

WORKDIR /Project_X
CMD [ "python3", "-m", "project_x" ]