# MOM-gRPC-Microservices Project for TET Course
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95%2B-green)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Swarm-orange)](https://docker.com)

A distributed system with failover capabilities developed for the Special Topics in Telematics course at EAFIT University.

## 📦 Repository Structure
├── api_gateway/ # FastAPI gateway implementation
├── client/ # Sample client application
├── micro_services/ # gRPC microservices
│ ├── sum/
│ ├── subtraction/
│ └── multiplication/
├── mom/ # Redis configuration and queue handlers
├── docs/ # Documentation and diagrams
├── docker-compose.yml # Swarm deployment configuration
├── instances_script.txt # AWS instance setup
└── .gitignore
