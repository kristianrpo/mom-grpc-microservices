# MOM-gRPC-Microservices Project for TET Course
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95%2B-green)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Swarm-orange)](https://docker.com)

A distributed system with failover capabilities developed for the Special Topics in Telematics course at EAFIT University.
## 📦 Introduction
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
