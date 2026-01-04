FROM python:3.10
RUN mkdir -p /app
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT [ "./entrypoint.sh" ]
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
