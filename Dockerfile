FROM ghcr.io/geode-solutions/vtk:3.9-cpu

WORKDIR /app

COPY . .
RUN python3 --version
RUN pip3 install --user -r requirements.txt
ENV PYTHONPATH="/usr/local:$PYTHONPATH"

CMD ["python3", "vtkw-server.py", "--port", "1234", "--host", "0.0.0.0", "--content", "".""]

EXPOSE 1234