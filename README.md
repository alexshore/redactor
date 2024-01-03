# Redactor Microservice

## General Usage

---

### Building

- Build docker image with `docker build -t redactor .`
- Tag image with repository username with `docker tag redactor <username>/redactor`
- Log-in to docker repository with `docker login -u <username>`
- Push image to repository with `docker push <username>/redactor`

### Deploying

- With `minikube`, start cluster with `minikube start`
- Using `kubectl`, deploy pods with `kubectl apply -f kubernetes/deployment.yml`
- Verify deployment is running with `kubectl get -f kubernetes/deployment.yml`
- Using `kubectl`, deploy service with `kubectl apply -f kubernetes/service.yml`
- Verify service is running with `kubectl get -f kubernetes/service.yml`

### Access

- Get URL with `minikube service redactor-service --url`
- Access by sending json data to `<URL>/redact` in a POST request

## CI Workflow

---

### Services

- For pipelines: GitHub Actions, Jenkins, CircleCI, etc.
- For testing: 
  - Coverage: SonarQube for reporting, coverage python module for testing.
  - Unit/Integration: Any python test framework e.g. pytest.
- For container registry: Google Container Registry, Harbor, Amazon ECR, etc.
- For servers: Amazon ECS, Google Kubernetes Engine, Azure Kubernetes Service, etc.

### Testing

#### For Coverage:
- Should run unit tests through coverage module.

#### For Unit-Testing:
- Design various unit tests for the redactor module.
- Tests should test each individual function with a large variety of input data checking for both expected successes and expected failures.
- Should be run before building.

#### For Integration-Testing:
- Design tests to be run on the app externally.
- Tests should pass a variety of data into the API endpoint and ensure they return either the expected fully redacted data or a json response containing error information. 
- Should be run after deploying to a staging server.

### Building

Should use a similar build process as written above to build the docker image but instead push it to a private enterprise container registry.

### Deployment

Should use the cli api of whichever server provider you're using combined with your CI pipelines service to deploy the service and deployment onto the available k8s cluster(s).

## Zero-Downtime Upgrades

---

Modern Kubernetes has a variety of ways to perform Zero-Downtime Upgrades and most kubernetes server providers will also have their own smoothed out processes to do the same thing within their APIs.

With GKE, an example Zero-Downtime Upgrade strategy could be the following:
- Create a separate node pool and deploy pods with the newer image version.
- Wait for new node pool to be up and running before pointing traffic at it.
- Cordon off the old node pool and drain each of its nodes.
- Delete the old node pool.
