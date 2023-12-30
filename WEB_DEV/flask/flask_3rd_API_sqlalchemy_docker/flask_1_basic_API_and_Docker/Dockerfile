# write python version you will use. BASE IMAGE
FROM python:3.11
# what port Flask app will run
EXPOSE 5000
# copy your app to docker dir you choose
WORKDIR /app
# install flask, or any other framework. Starts terminal command when creating image
RUN pip install flask
# copy files to docker. first you have to write
# file you want to copy or folder, second you have to write
# docker image dir
COPY . .
# What command will be executed when you start your container.
# This command will start flask app
CMD ["flask", "--app", "/app/app.py", "run", "--debug"]