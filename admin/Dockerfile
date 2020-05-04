# Use an official Python runtime as an image
FROM python:3.6

# The EXPOSE instruction indicates the ports on which a container # # will listen for connections
# Since Flask apps listen to port 5000  by default, we expose it
EXPOSE 5004
ADD . /admin

# Sets the working directory for following COPY and CMD instructions
# Notice we haven’t created a directory by this name - this
# instruction creates a directory with this name if it doesn’t exist
WORKDIR /admin

# Install any needed packages specified in requirements.txt
COPY requirements.txt /admin
COPY templates /admin
RUN pip install -r requirements.txt

# Run front-end_server.py when the container launches
COPY admin.py /admin
CMD python admin.py
