FROM python:3.9
ENV DATABASE_URL=mysql+mysqlconnector://root:password@192.168.1.3/ML_DOCKER_APP
ENV APP_USERNAME=akash_solanki
ENV APP_PASSWORD=akki@1928
WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
