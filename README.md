# MOM-gRPC-Microservices Project for TET Course
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95%2B-green)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Swarm-orange)](https://docker.com)

## 📌 Introduction
This repository contains the first project for EAFIT University's Topics in Telematics course, implementing a fault-tolerant microservices system where an API Gateway (FastAPI) handles REST client requests and communicates with gRPC microservices (Sum/Subtraction/Multiplication), automatically failing over to a Redis-based MOM for request queuing during service outages, with Docker Swarm deployment on AWS ensuring high availability.

## 📦 Repository Structure
```bash
├── api_gateway/ # FastAPI gateway implementation
├── client/ # Sample client application
├── micro_services/ # gRPC microservices
│ ├── micro_service_multiplication/
│ ├── micro_service_subtraction/
│ └── micro_service_sum/
├── mom/ # Redis configuration and queue handlers
├── docker-compose.yml # Swarm deployment configuration
├── instances_script.txt # AWS instance setup
└── .gitignore
```
## 🚀 Usage & Deployment
### AWS Cluster Setup
1. Launch Instances (7x AWS EC2 from template): Load the [`instances_script.txt`](instances_script.txt) as **User Data** during template creation and configure inbound rules.
2. Initialize Swarm Manager:
   ```bash
   docker swarm init --advertise-addr <MANAGER_IP>
   ```
3. Join Workers:
   ```bash
   docker swarm join --token <TOKEN> <MANAGER_IP>:2377  # Run on all workers
   ```
5. Node Configuration
   ```bash
   # Label nodes for role assignment (run on manager)
   docker node update --label-add function=api-gateway manager-01
   docker node update --label-add function=redis worker-01
   docker node update --label-add function=microservice-sum worker-02
   docker node update --label-add function=mom worker-03
   # ... (add other microservices)
   ```
5. Deploy Stack
   ```bash
   # From manager node:
   docker stack deploy -c docker-compose.yml my_stack
   ```
   ```bash
   docker service ls  # Verify services
   ```
### Local Setup

1. Redis Setup with Docker (Recommended for Local Development)
    - 📌 Prerequisites: Docker Desktop installed and running
    - 🚀 Step-by-Step Running Redis in Docker:
      - Pull the Redis Image: If you don’t have Redis locally, Docker will download it automatically
      ```bash
      docker pull redis:alpine  # Lightweight Redis image
      ```
      - Start a Redis Container:
      ```bash
      docker run --name redis-mom -p 6379:6379 -d redis:alpine
      ```

2. Run Microservices
    - Sum Service:
    ```bash
    cd micro_services/micro_service_sum
    pip install -r requirements.txt
    python sum_service.py
    ```
    - Subtraction Service:
    ```bash
    cd micro_services/micro_service_subtraction
    pip install -r requirements.txt
    python subtraction_service.py
    ```
    - Multiplication Service:
    ```bash
    cd micro_services/micro_service_multiplication
    pip install -r requirements.txt
    python multiplication_service.py
    ```

3. Start MOM Handler
   ```bash
   cd mom
   pip install -r requirements.txt
   python main.py
   ```
4. Launch API Gateway
   ```bash
   cd api_gateway
   pip install -r requirements.txt
   uvicorn app:app --host 0.0.0.0 --port 80
   ```
5. Test the System using Client
   ```bash
   cd client
   pip install -r requirements.txt
   python main.py
   ```

It's important to note that you need to create a .env file in each component based on the .env.example file.

## 👥 Developers and Contact
For further inquiries, please contact:

- Sara Cortes: svcortesm@eafit.edu.co
- Kristian Restrepo: krestrepoo@eafit.edu.co
- Evelyn Zapata: eazapatat@eafit.edu.co
