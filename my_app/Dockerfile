# Use an official Python runtime as an image
FROM python:3.6

# The EXPOSE instruction indicates the ports on which a container # # will listen for connections
# Since Flask apps listen to port 5000  by default, we expose it
EXPOSE 5005
ADD . /my_app

# Sets the working directory for following COPY and CMD instructions
# Notice we haven’t created a directory by this name - this
# instruction creates a directory with this name if it doesn’t exist
WORKDIR /my_app

# Install any needed packages specified in requirements.txt
COPY requirements.txt /my_app
COPY templates /my_app
RUN pip install -r requirements.txt

# Run front-end_server.py when the container launches
COPY front-end_server.py /my_app
CMD python front-end_server.py
