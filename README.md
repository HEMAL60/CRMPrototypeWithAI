Prototype ERP/CRM Module with AI Support for Reliant Windows
This project is a full-stack prototype of a modern, containerized ERP/CRM module designed to meet the specifications of the technical task for the KTP Associate position. It demonstrates a complete development workflow, from database design to a functional web interface, including a machine learning feature.

The entire application is orchestrated with Docker Compose, ensuring a simple and reliable setup process.

Features Implemented
This prototype successfully delivers on all core requirements outlined in the task brief:

Database & Data Model: A robust PostgreSQL database schema models customers, products, quotations, and users with role-based access control.

Full Customer Management (CRM):

Add new customers with mandatory field validation.

Update existing customer details.

View a complete list of all customers.

Search for specific customers by ID or name.

Quotation History (ERP): View a detailed quotation history for any customer, including all line-item details.

Role-Based Access Control (RBAC):

A secure endpoint allows authorized administrators ('Human Resources Head') to manage the roles of other users.

A separate secure endpoint allows administrators to view the full list of company users.

AI-Powered Quotation Predictor:

An AI model trained on historical data provides instant, data-driven price estimates for new quotation items.

Architecture & Tech Stack
The application is built using a modern, decoupled three-tier architecture, with each component running in its own Docker container.

Frontend (Streamlit): A clean and interactive web interface built entirely in Python. It acts as the client, making API calls to the backend.

Backend (FastAPI): A high-performance REST API that handles all business logic, database interactions, and AI predictions.

Database (PostgreSQL): A powerful and reliable relational database for data persistence.

Tools, Libraries, and Platforms
Category

Technology

Reason for Choice

Backend

FastAPI, Uvicorn

For its high performance, modern asynchronous capabilities, and automatic generation of interactive API docs.



SQLAlchemy

The industry-standard ORM for Python, providing a robust and secure way to interact with the database.



Pydantic

For strict data validation and settings management, ensuring a reliable API data contract.

Frontend

Streamlit

Enables rapid development of a clean, data-focused web UI entirely in Python, perfect for a prototype.



Requests, Pandas

For communicating with the backend API and for efficient data manipulation and display.

Database

PostgreSQL

A production-grade, open-source relational database known for its reliability and feature set.

AI/ML

Scikit-learn, Pandas

The go-to libraries for machine learning in Python, providing powerful tools for data processing and modeling.

Platform

Docker, Docker Compose

For containerizing the application, ensuring a consistent, portable, and easy-to-run development environment.

How to Run the Solution Locally
Prerequisites
Git

Docker Desktop (ensure the Docker engine is running)

Step-by-Step Instructions
Clone the Repository:
Open a terminal and clone your GitHub repository.

git clone [https://github.com/HEMAL60/CRMPrototypeWithAI.git](https://github.com/HEMAL60/CRMPrototypeWithAI.git)
cd CRMPrototypeWithAI

Build and Start the Services:
This single command will build the images for the frontend and backend, start all three containers, and connect them to a shared network.

docker-compose up --build

Keep this terminal running to view live logs from all services.

Access the Application:
Once all containers are running, the application is ready to use.

Frontend Web App: Open your browser and navigate to http://localhost:8501

Backend API Docs: To explore the API, navigate to http://localhost:8000/docs

Note: The AI Price Predictor feature will work immediately, as a pre-trained model (ml_model.joblib) is already included in this repository. Training the model is optional.

Optional: Retraining the AI Model
If you wish to retrain the model (for example, after adding more data), follow these steps while the main application is running:

Run the Training Script:
Open a new, second terminal and run the following command. This executes the training script inside the running backend container.

docker-compose exec backend python train_model.py

This will overwrite the existing ml_model.joblib file with a newly trained version.

Restart the Backend:
Go back to your first terminal, press Ctrl+C to stop the services, and then start them again. This is necessary for the backend to load the new model file into memory.

docker-compose up

Future Scope & Cloud Deployment
The containerized architecture of this project serves as a strong foundation for a scalable, production-ready cloud deployment. The use of Docker ensures that the application is portable and can run consistently across different environments.

General Cloud Deployment Strategy
Managed Database: The local PostgreSQL container would be replaced with a managed database service like Amazon RDS or Google Cloud SQL. This provides automated backups, scaling, and security patching, which are essential for production.

Container Registry: The frontend and backend Docker images would be pushed to a private container registry, such as Amazon ECR, Google Container Registry, or Docker Hub.

Container Orchestration: The images would be deployed to a container hosting service like AWS Elastic Beanstalk, Google Cloud Run, or Azure App Service, which manage networking, scaling, and load balancing.

Environment Configuration: The DATABASE_URL would be updated in the backend's environment variables to point to the managed database.

Deployment with Kubernetes
For more advanced scaling and management, the application is well-suited for deployment on a Kubernetes cluster (e.g., using Amazon EKS, Google GKE, or Azure AKS).

Translation to Kubernetes Objects: The docker-compose.yml file provides a clear blueprint that can be translated into Kubernetes manifest files:

Each service (frontend, backend) would become a Deployment (to manage Pods) and a Service (for networking).

The postgres_data volume would become a PersistentVolumeClaim, ensuring database storage is stable and independent of the database Pod's lifecycle.

Environment variables would be managed using ConfigMaps and Secrets.

Benefits of Kubernetes: Deploying on Kubernetes would unlock powerful features like:

Auto-scaling: Automatically increase or decrease the number of backend pods based on CPU load.

Self-healing: If a container crashes, Kubernetes will automatically restart it.

Rolling Updates: Update the application to a new version with zero downtime.

Centralized Logging and Monitoring: Integrate with tools like Prometheus and Grafana for deep insights into application performance.