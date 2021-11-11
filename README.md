#Testing vertex prediction custom container

docker build -t myimage20 .
docker run -d -p 8080:8080 myimage20


docker tag myimage17 us-central1-docker.pkg.dev/kubeflow-demos/repo-models/container_model17

docker push us-central1-docker.pkg.dev/kubeflow-demos/repo-models/container_model17




gcloud beta ai models upload \
  --region=us-central1 \
  --display-name=fast-test4 \
  --container-image-uri=us-central1-docker.pkg.dev/kubeflow-demos/repo-models/container_model16 \
  --container-ports=8080 \
  --container-health-route=/health_check \
  --container-predict-route=/test


  curl -X 'POST' \
  'http://localhost:8080/test2' \
  -H 'Content-Type: application/json' \
  -d '{"instances":[["sfdsfasfsadf"]]}'
