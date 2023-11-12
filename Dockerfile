# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory to /app
WORKDIR /app
COPY requirements.txt ./
# Install Gradio and other dependencies
RUN pip install -r requirements.txt

# Copy the contents of the Gradio app into the container
COPY app.py ./

# Expose the port on which Gradio will run
EXPOSE 7860

# Command to run the Gradio app
CMD ["python", "app.py"]
