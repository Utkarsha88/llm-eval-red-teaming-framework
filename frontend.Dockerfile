# Use a lightweight, official Python runtime image
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /workspace

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the client presentation code array 
COPY ./dashboard /workspace/dashboard
# Copy app folders if needed by the dynamic dataset scanner path (app/datasets)
COPY ./app/datasets /workspace/app/datasets

# Expose the presentation workspace interface port
EXPOSE 8501

# Run Streamlit with absolute mapping rules targeting host listeners
CMD ["streamlit", "run", "dashboard/app.py", "--server.port=8501", "--server.address=0.0.0.0"]