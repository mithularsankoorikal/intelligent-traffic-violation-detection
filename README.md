# Intelligent Traffic Violation Detection System 🚦

## Overview

The **Intelligent Traffic Violation Detection System** is a web-based application developed using Django and YOLOv8 to automate the detection and management of traffic violations from uploaded traffic videos. The system extracts video frames, detects objects using deep learning, and identifies violations such as triple riding and riding without a helmet.

The application stores violation details and supporting image evidence in a database. It also provides user registration and login, fine tracking, payment-status management, email notifications for detected violations, and PDF receipt generation.

## Features

- **Video Upload:** Upload recorded traffic videos for analysis.
- **Frame Extraction:** Extract frames from uploaded videos for object detection.
- **YOLOv8 Object Detection:** Detect relevant objects such as motorcycles, riders, and helmets.
- **Violation Identification:** Apply rule-based logic to identify supported violations, including triple riding and no-helmet riding.
- **Evidence Management:** Save detected violation frames and associated details.
- **Email Notifications:** Automatically send email notifications to registered users when a traffic violation is detected.
- **User Authentication:** Provide registration, login, and password-reset functionality.
- **Fine Management:** Allow users to view pending fines and fine history.
- **Payment Management:** Update fine payment status and generate PDF payment receipts.
- **Database Storage:** Store user and violation information using SQLite.

## Technologies Used

- **Programming Language:** Python
- **Web Framework:** Django
- **Deep Learning Model:** YOLOv8
- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Database:** SQLite
- **Development Environment:** PyCharm
- **Operating System:** Windows 11

## Quick Start Installation

Follow these steps to run the project locally.

### Prerequisites

- Python installed on your system.
- Git installed on your system.
- pip package manager.
- A compatible YOLOv8 model weights file (for example, `best.pt` or your project's trained weights).

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/intelligent-traffic-violation-detection.git
cd intelligent-traffic-violation-detection
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the environment on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install Dependencies

If the repository includes a `requirements.txt` file, run:

```bash
pip install -r requirements.txt
```

If it does not, create one containing the project's required packages, or install the dependencies specified by the project. Common packages may include:

```bash
pip install django ultralytics opencv-python reportlab
```

Install any additional packages your project imports.

### 4. Configure the Project

- Ensure the YOLOv8 model weights file is available in the expected model directory.
- Update the model path in the project settings or detection code if necessary.
- Configure Django email settings if you want violation notification emails to work.
- Keep passwords, email credentials, and other secrets out of public repositories.

### 5. Apply Database Migrations

```bash
python manage.py migrate
```

### 6. Start the Development Server

```bash
python manage.py runserver
```

Open the following address in your browser:

```text
http://127.0.0.1:8000/
```

### Troubleshooting

- **Missing module:** Install the missing dependency in your activated virtual environment.
- **Model file not found:** Verify the YOLOv8 weights file path.
- **Email not sending:** Check the Django email configuration and credentials.
- **Database errors:** Run the migrations and verify the database configuration.


## System Workflow

1. The administrator uploads a recorded traffic video.
2. The system extracts frames from the video.
3. YOLOv8 detects relevant objects in the extracted frames.
4. Rule-based logic identifies supported traffic violations.
5. The system saves violation evidence and related information.
6. An email notification is sent to the registered user when a traffic violation is detected.
7. Users log in to view their fine details and payment status.
8. Users can complete the project's payment workflow and download PDF receipts.

## Project Objective

The main objective is to demonstrate how deep learning and web technologies can be combined to automate traffic violation detection, maintain digital evidence, notify users about detected violations, and simplify fine management.

## Limitations

- The system processes uploaded videos rather than live CCTV feeds.
- Detection performance depends on video quality, lighting, and the trained model.
- Only the violation types implemented in the project are supported.
- The payment workflow should not be considered a real payment gateway unless integrated with a verified payment provider.

## Future Enhancements

- Automatic Number Plate Recognition (ANPR).
- Real-time traffic monitoring.
- Traffic violation analytics dashboard.
- Integration with a secure online payment gateway.
- Analytics dashboards for traffic violation trends.
- AI-powered chat assistant for explaining violations and traffic rules.

## Disclaimer

This project is developed for educational and demonstration purposes. Detection results should be reviewed before any real-world enforcement action.

