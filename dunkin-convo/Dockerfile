FROM 140427343267.dkr.ecr.us-east-2.amazonaws.com/base:latest
COPY . /app
WORKDIR /app
COPY . /tmp/
EXPOSE 8080
ENTRYPOINT ["python"]
CMD ["app.py"]