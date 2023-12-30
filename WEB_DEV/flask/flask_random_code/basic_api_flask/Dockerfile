FROM python:3.11
EXPOSE 5000
WORKDIR /sample_marshamllow_api
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "--app", "/sample_marshamllow_api/app.py", "run", "--debug"]