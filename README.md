# Prototype ERP/CRM Module with AI Support for Reliant Windows

[![Python](https://img.shields.io/badge/Python-3.9-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95.2-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.22.0-red.svg)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/Docker-24.0-blue.svg)](https://www.docker.com/)

This repository contains a full-stack prototype of a modern, containerized ERP/CRM module designed for Reliant Windows. It demonstrates a complete development workflow, from database design to a functional web interface, incorporating a practical machine learning feature for price prediction.

The entire application is orchestrated with **Docker Compose**, ensuring a simple, one-command setup process.

---

## 🎯 Core Features

This prototype successfully delivers on all key requirements outlined in the project brief.

* **🗃️ Database & Data Model**: A robust PostgreSQL schema models customers, products, quotations, and users with role-based access control (RBAC).
* **👥 Full Customer Management (CRM)**:
    * Add new customers with mandatory field validation.
    * Update existing customer details seamlessly.
    * View a comprehensive list of all customers.
    * Search for customers by ID or name.
* **🧾 Quotation History (ERP)**: View a detailed quotation history for any customer, including all line-item details.
* **🔐 Role-Based Access Control (RBAC)**:
    * A secure endpoint for `Human Resources Head` to manage user roles.
    * A secure endpoint for administrators to view all company users.
* **🤖 AI-Powered Quotation Predictor**: An AI model trained on historical data provides instant, data-driven price estimates for new quotation items, streamlining the sales process.

---

## 🏗️ Architecture & Tech Stack

The application is built using a modern, decoupled three-tier architecture. Each component is isolated in its own Docker container for maximum portability and scalability.

* **Frontend (Streamlit)**: A clean and interactive web interface built entirely in Python. It acts as the client, making API calls to the backend.
* **Backend (FastAPI)**: A high-performance REST API that handles all business logic, database interactions, and serves AI model predictions.
* **Database (PostgreSQL)**: A powerful, open-source relational database for all data persistence.

### Tools, Libraries, and Platforms

| Category      | Technology                   | Reason for Choice                                                                                   |
| :------------ | :--------------------------- | :-------------------------------------------------------------------------------------------------- |
| **Backend** | `FastAPI`, `Uvicorn`         | High performance, modern asynchronous capabilities, and automatic interactive API documentation.    |
|               | `SQLAlchemy`                 | The industry-standard ORM for Python, providing a robust and secure way to interact with the database. |
|               | `Pydantic`                   | Enforces strict data validation and settings management, ensuring a reliable API data contract.       |
| **Frontend** | `Streamlit`                  | Enables rapid development of a clean, data-focused UI entirely in Python, perfect for a prototype.    |
|               | `Requests`, `Pandas`         | For seamless communication with the backend API and efficient data manipulation for display.        |
| **Database** | `PostgreSQL`                 | A production-grade, open-source relational database known for its reliability and rich feature set.   |
| **AI/ML** | `Scikit-learn`, `Pandas`     | The go-to libraries for machine learning in Python, providing powerful tools for data processing and modeling. |
| **Platform** | `Docker`, `Docker Compose`   | For containerizing the application, ensuring a consistent, portable, and easy-to-run environment.   |

---

## 🚀 How to Run the Solution Locally

### Prerequisites

* [**Git**](https://git-scm.com/)
* [**Docker Desktop**](https://www.docker.com/products/docker-desktop/) (ensure the Docker engine is running)

### Step-by-Step Instructions

1.  **Clone the Repository**:
    Open your terminal and run the following commands:
    ```bash
    git clone [https://github.com/HEMAL60/CRMPrototypeWithAI.git](https://github.com/HEMAL60/CRMPrototypeWithAI.git)
    cd CRMPrototypeWithAI
    ```

2.  **Build and Start the Services**:
    This single command builds the Docker images, starts all three containers (frontend, backend, database), and connects them.
    ```bash
    docker-compose up --build
    ```
    Keep this terminal running to view live logs from all services.

3.  **Access the Application**:
    Once the containers are running, the application is ready!
    * **🌐 Frontend Web App**: Open your browser to **[http://localhost:8501](http://localhost:8501)**
    * **⚙️ Backend API Docs**: Explore the API endpoints at **[http://localhost:8000/docs](http://localhost:8000/docs)**

> **Note**: The AI Price Predictor feature works out-of-the-box, as a pre-trained model (`ml_model.joblib`) is included in the repository.

### Default User Credentials

To test the Role-Based Access Control features, use the following pre-seeded users:

* **Admin Role**:
    * **Username**: `admin@reliant.com`
    * **Password**: `adminpassword`
* **Standard User Role**:
    * **Username**: `user@reliant.com`
    * **Password**: `userpassword`

---

## 🧠 Optional: Retraining the AI Model

If you add more data and wish to retrain the model, follow these steps while the main application is running.

1.  **Run the Training Script**:
    Open a **new, second terminal** and execute the training script inside the running backend container.
    ```bash
    docker-compose exec backend python train_model.py
    ```
    This will overwrite the existing `ml_model.joblib` file with a newly trained version.

2.  **Restart the Backend**:
    Return to your **first terminal**, press `Ctrl+C` to stop the services, and then start them again. This is necessary for the FastAPI backend to load the new model into memory.
    ```bash
    docker-compose up
    ```

---

## ☁️ Future Scope & Cloud Deployment

The containerized architecture of this project serves as a strong foundation for a scalable, production-ready cloud deployment.

### General Cloud Strategy

1.  **Managed Database**: Replace the local PostgreSQL container with a managed service like **Amazon RDS** or **Google Cloud SQL** for automated backups, scaling, and security.
2.  **Container Registry**: Push the `frontend` and `backend` Docker images to a private registry like **Amazon ECR**, **Google Container Registry**, or **Docker Hub**.
3.  **Container Orchestration**: Deploy the images to a container hosting service like **AWS Elastic Beanstalk**, **Google Cloud Run**, or **Azure App Service** to manage networking, scaling, and load balancing.
4.  **Environment Configuration**: Update the `DATABASE_URL` in the backend's environment variables to point to the new managed database.

### Deployment with Kubernetes

For advanced scaling and management, the application is well-suited for deployment on a Kubernetes cluster (e.g., **Amazon EKS**, **Google GKE**, or **Azure AKS**).

* **Translation**: The `docker-compose.yml` file provides a clear blueprint that can be translated into Kubernetes manifest files (`Deployment`, `Service`, `PersistentVolumeClaim`).
* **Benefits**: Deploying on Kubernetes would unlock powerful features like **auto-scaling**, **self-healing** pods, **zero-downtime rolling updates**, and integration with monitoring tools like **Prometheus** and **Grafana**.