# Sustainable Resource Management System

A Smart City–oriented application that models and monitors the usage of urban resources
such as **water, energy, and waste** using **Object-Oriented Programming (OOP) principles in Python**.

This project is developed as a **3rd-year engineering mini project** and focuses on clean
system design, correctness, and clarity rather than unnecessary complexity.

---

## 🌐 Live Demo

🔗 https://sustainable-resource-management.up.railway.app

---

## Problem Statement

Urban areas require efficient tracking and management of natural resources to promote
sustainability and reduce environmental impact.

The objective of this project is to design and implement a **Sustainable Resource Management System**
that models resource availability, consumption, and sustainability metrics using
**Object-Oriented Programming (OOP)** concepts in Python.

---

## Key Features

- OOP-based system design with a common `Resource` base class
- Specialized resource types:
  - Water
  - Energy
  - Waste
- Consumer-based resource allocation and usage tracking
- Prevention of resource overuse through validation
- Sustainability reporting:
  - Total resource usage
  - Renewable vs non-renewable breakdown
- Threshold-based alerts and recommendations
- Interactive web dashboard for visualization
- Clean separation between system logic and presentation layer

---

## Object-Oriented Design

### Core Classes

- **Resource (Base Class)**
  - Attributes: `name`, `total_available`, `renewable`
  - Methods: `report_usage()`, `update_availability(amount)`

- **WaterResource, EnergyResource, WasteResource**
  - Derived from `Resource`
  - Demonstrate inheritance and polymorphism

- **Consumer**
  - Attributes: `consumer_id`, `name`, `assigned_resources`
  - Methods: `use_resource()`, `generate_usage_report()`

### OOP Principles Demonstrated

- **Abstraction** – Common resource behavior defined in a base class  
- **Inheritance** – Specialized resource types derived from `Resource`  
- **Encapsulation** – Controlled access to resource state via methods  
- **Polymorphism** – Uniform interfaces for reporting and updates  

---

## System Capabilities

- Supports multiple consumers and multiple resources
- Tracks consumption per resource and per consumer
- Enforces constraints to prevent overuse
- Generates sustainability insights and alerts
- Presents data through a structured monitoring dashboard

---

## 🛠 Technology Stack

- **Backend:** Python, FastAPI
- **Frontend:** HTML, CSS, JavaScript
- **Visualization:** Chart.js
- **Deployment:** Railway

---

## Running the Project Locally

```bash
# Clone the repository
git clone <repository-url>
cd sustainable-resource-management-system

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn api.app:app --reload
