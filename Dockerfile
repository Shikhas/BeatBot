FROM python:3.6.2
RUN mkdir /src
COPY . /src
WORKDIR /src
RUN python -m pip install --upgrade pip setuptools wheel
RUN pip3 install -r requirements.txt
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]