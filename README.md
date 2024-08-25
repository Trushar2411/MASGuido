# MASGuido
# Personalized Elective Finder with Pepper Robot

**Project Duration:** 23rd May 2024 to 11th July 2024

**Course:** Human-Centered Interaction in Robotics

**Instructors:**
- Prof. Dr. Teena Hassan (teena.hassan@h-brs.de)
- Ritwik Sinha (ritwik.sinha@smail.inf.h-brs.de)

---

## Project Overview

Welcome to the Personalized Elective Finder project! This project aims to develop a socially interactive assistant using Pepper, the humanoid robot. The assistant will help students find a list of suitable elective courses based on their preferences.

---

## Features

1. **Face Detection and Verification:**
   - Pepper detects faces using the webcam.
   - Optional: Verify if the face belongs to an authorized user.

2. **Multi-modal Greeting Behavior:**
   - Initiates a greeting when a face is detected.
   - Optional: Personalize the greeting based on the person's identity.

3. **Error Handling in Face Detection:**
   - Handles noise and errors in face detection to avoid misclassification.

4. **Conversation to Assist in Finding Electives:**
   - Engages in a conversation to understand user preferences.
   - Uses an internal model to infer and recommend suitable courses.
   - Optional: Provides a ranking of courses using a Bayesian network.

5. **Illustrative Gestures:**
   - Displays gestures to accompany speech during the conversation.

6. **Socially Appropriate Farewell:**
   - Bids farewell in a polite and socially appropriate manner.

7. **Filtering Abusive Language:**
   - Detects and refrains from engaging in abusive language exchanges.

8. **Speech Input:**
   - Optional: Accepts speech input from the user.

---

## Installation and Setup

### Prerequisites

- Python 3.7+
- qiBullet Simulation Environment
- OpenCV
- NLTK
- Other dependencies listed in `requirements.txt`

### Steps to Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Trushar2411/MASGuido.git
   ```
## Usage

### Running the Simulation

1. Ensure your webcam is connected and working.
2. Run `main.py` to start the simulation.
3. Follow the on-screen instructions to interact with Pepper.

### Features Demonstration

- Pepper will detect your face and initiate a greeting.
- Engage in a conversation with Pepper to find suitable elective courses.
- Observe the gestures and interactions provided by Pepper.
- Conclude the session with a farewell from Pepper.

---

## Internal Model for Course Recommendation

Pepper uses a Bayesian network to infer and recommend elective courses based on user preferences. This model considers various criteria such as:

- User's academic background
- Interests
- Previous coursework

---

## Marketing Slogan

**Meet MASGuido: Your Personal Course Navigator!**

---

## Contributing

We welcome contributions! Please fork the repository and create a pull request with your changes. Ensure your code follows the project's coding standards and includes relevant tests.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

## Contact

For any queries or support, please contact:

- Trushar Ghanekar(trushar.ghanekar2411@gmail.com)
- Shrikar Nakhye(nakhyeshrikar@icloud.com)

---

Thank you for using the Personalized Elective Finder! We hope it helps you navigate your elective choices with ease.

