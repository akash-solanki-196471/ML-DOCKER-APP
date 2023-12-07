# AI Image Classification Web Application

## Overview

This repository contains a Python-based web application that serves an AI model for image classification. The application is containerized using Docker and can be deployed in a Kubernetes environment.

## Prerequisites

- Docker installed: [Get Docker](https://docs.docker.com/get-docker/)
- Kubernetes installed: [Install Kubernetes](https://kubernetes.io/docs/setup/)
- kubectl configured: [Install kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)

## Setup Instructions

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/akash-solanki-196471/ML-DOCKER-APP.git
    cd ML-DOCKER-APP
    ```

2. **Build the Docker Image:**

    ```bash
    docker build -t ml-docker-app .
    ```


3. **Update Kubernetes Deployment Configuration:**

    Open `kube.yaml` and update the `image` field under `containers` with your Docker image name:

    ```yaml
    spec:
      containers:
      - name: your-container-name
        image: your-image-name:tag
        ports:
        - containerPort: 80
    ```


5. **Deploy to Kubernetes:**

    ```bash
    kubectl apply -f kube.yaml
    ```

6. **Expose the Service:**

    If needed, expose the service to access it externally:

    ```bash
    kubectl expose deployment your-deployment-name --type=LoadBalancer --port=80 --target-port=80
    ```


## Accessing the Application

Once the deployment is successful, you can access the application using the external IP provided by the LoadBalancer service or by using the NodePort, depending on your Kubernetes environment.

```bash
kubectl get services
