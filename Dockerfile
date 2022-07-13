FROM ghcr.io/geode-solutions/vtk:3.9-cpu

WORKDIR /app

COPY . .
RUN pip3 install --user -r requirements.txt
ENV PYTHONPATH="/usr/local:$PYTHONPATH"

CMD python vtkw-server.py --port 443 --host 0.0.0.0 --content .

EXPOSE 443
