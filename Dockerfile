# Extend the official Airflow image and install required Python dependencies
FROM apache/airflow:2.8.3

# Switch to the airflow user to install packages
USER airflow
RUN pip install --no-cache-dir pandas scikit-learn joblib requests
