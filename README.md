# Face Expression Detection API

This project is a Flask application that detects facial expressions using a pre-trained model. It provides an online interface as well as a Docker setup for local deployment.

## Live Demo

You can access the live demo of this application at: [Face Expression Detection](https://scornful-millicent-universityofwaterloo-dd7f76b3.koyeb.app/)

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Prerequisites

- Python 3.7 or higher
- Docker (for running with Docker)
- Git

### Clone the Repository

```bash
git clone https://github.com/chitwan-waterloo/face_expression_detection_api.git
cd face_expression_detection_api

### Install Dependencies

```bash
pip install -r requirements.txt

### Run the Flask App

```bash
python app.py

#### 
The application will be available at http://127.0.0.1:5000

### Using Docker
To build and run the application using Docker:

```bash
docker build -t face_expression_detection_api .
docker run -p 5000:5000 face_expression_detection_api