# mindspace-ml-be

## How to Run

### Docker

#### Build

```bash
docker build -t mindspace-ml .
```

#### Run

```bash
docker run -p 80:8080 mindspace-ml
```

#### Builds

gcloud builds submit --tag gcr.io/mindspace-capstone-project/mindspace-ml .

#### Deploy to Cloud Run

gcloud beta run deploy mindspace-ml --image gcr.io/mindspace-capstone-project/mindspace-ml --region asia-southeast2 --platform managed --allow-unauthenticated --quiet

docker tag mindspace-ml:latest asia-southeast2.pkg.dev/mindspace-capstone-project/mindspace/mindspace-ml
