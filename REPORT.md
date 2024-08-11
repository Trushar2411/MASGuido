Certainly! Here's a more detailed and structured project report suitable for a master's level submission in robotics:

---

## Project Report: Human-Centered Interaction in Robotics

### Title: Development of a Socially Interactive Pepper Robot for Academic Course Assistance

**Course:** Human-Centered Interaction in Robotics  
**Professor:** Prof. Dr. Teena Hassan  
**Teaching Assistant:** Ritwik Sinha  
**Duration:** 23rd May 2024 to 11th July 2024  
**Institution:** Hochschule Bonn-Rhein-Sieg (H-BRS)  
**Student:** [Your Name]

---

### 1. **Introduction**

In the context of advancing human-robot interaction, this project aimed to develop a socially interactive robotic assistant using the Pepper robot simulated in the qiBullet environment. The primary goal was to create a system that assists students in selecting suitable elective courses based on their preferences, leveraging a blend of face detection, natural language processing, and multi-modal interaction techniques.

### 2. **Project Objectives**

The project's objectives were outlined as follows:
1. **Face Detection and Verification**: Implement real-time face detection and optionally verify if the face belongs to an authorized user.
2. **Personalized Multi-Modal Greeting**: Develop a system for Pepper to initiate personalized greetings based on face detection.
3. **Robustness in Interaction**: Ensure that the robot can handle face detection errors and maintain a consistent interaction flow.
4. **Interactive Course Assistance**: Engage the user in a conversation to recommend elective courses.
5. **Course Recommendation Model**: Integrate a Bayesian network to rank and suggest elective courses based on user preferences.
6. **Gesture Integration**: Incorporate illustrative gestures that accompany verbal interactions to enhance engagement.
7. **Socially Appropriate Farewell**: Implement a polite and contextually appropriate farewell mechanism.
8. **Abusive Language Handling**: Ensure the system filters and handles abusive language appropriately.
9. **Speech Input Capability**: Optionally accept and process speech input from users.
10. **Branding and Marketing**: Develop a name and slogan for the robotic assistant.

### 3. **System Design and Implementation**

#### 3.1 **Face Detection and Verification**

**Technologies Used:**
- **OpenCV**: For face detection using the Haar Cascade classifier.
- **Webcam**: For capturing video feed.

**Description:**
The face detection module uses OpenCV's `haarcascade_frontalface_default.xml` to detect faces in the video stream from the webcam. Upon detection, the system calculates the face's center and adjusts Pepper’s head position to maintain visual engagement. 

**Verification (Optional):**
To verify authorized users, facial recognition algorithms can be integrated. For this, a database of authorized users' facial features could be maintained and matched against detected faces.

#### 3.2 **Greeting Interaction**

**Technologies Used:**
- **gTTS** (Google Text-to-Speech): For generating audio greetings.
- **PyDub**: For playing the generated audio.

**Description:**
Upon detecting a face, Pepper initiates a multi-modal greeting sequence involving both physical gestures (e.g., waving) and verbal communication. This sequence is designed to be welcoming and can be personalized if user verification is implemented.

**Implementation:**
- **Waving**: Pepper performs a waving motion using its arm.
- **Verbal Greeting**: A greeting message is synthesized and played using gTTS.

#### 3.3 **Robust Interaction Handling**

**Technologies Used:**
- **Error Handling**: Built-in checks to handle face detection failures.

**Description:**
The system includes mechanisms to handle temporary loss or misclassification of faces. If the detected face moves out of frame or if multiple faces are detected, Pepper pauses the interaction and waits until a stable face is detected again.

#### 3.4 **Interactive Course Assistance**

**Technologies Used:**
- **Rasa**: For natural language understanding and dialogue management.

**Description:**
The interaction involves a dialogue with the user to understand their course preferences. Pepper processes user input and provides course recommendations based on predefined criteria.

**Implementation:**
- **Dialogue Management**: Using Rasa to handle user queries and provide responses.
- **User Input Handling**: Collecting preferences and responding with appropriate course suggestions.

#### 3.5 **Course Recommendation Model**

**Technologies Used:**
- **Bayesian Network (Proposed)**: For ranking courses based on user preferences.

**Description:**
A Bayesian network model is proposed to rank courses according to various criteria such as difficulty, relevance to career goals, and personal interests. The model uses probabilistic inference to suggest the most suitable courses.

**Implementation (Proposed):**
- **Data Collection**: Gathering data on courses and user preferences.
- **Model Training**: Training the Bayesian network to predict course suitability.
- **Integration**: Connecting the model to Pepper's dialogue system for dynamic recommendations.

#### 3.6 **Gesture Integration**

**Technologies Used:**
- **Pepper SDK**: For controlling Pepper’s physical movements.

**Description:**
Pepper uses gestures such as head nodding and hand movements to accompany verbal communication, making interactions more engaging and natural.

**Implementation:**
- **Head Nodding**: Implemented to signify agreement or attentiveness.
- **Hand Gestures**: Used during greetings or explanations.

#### 3.7 **Socially Appropriate Farewell**

**Technologies Used:**
- **gTTS** and **PyDub**: For generating and playing farewell messages.

**Description:**
Pepper concludes interactions with a polite and contextually appropriate farewell, ensuring a positive end to the user experience.

**Implementation:**
- **Farewell Message**: Synthesized and played using gTTS.
- **Gesture**: Accompanying gesture to reinforce the farewell.

#### 3.8 **Abusive Language Handling**

**Technologies Used:**
- **Text Filtering Algorithms**: For detecting and handling abusive language.

**Description:**
The system filters out abusive language and responds politely to maintain a professional interaction environment.

**Implementation:**
- **Abusive Language Detection**: Implemented using text analysis and predefined lists of offensive terms.
- **Polite Response**: A default response when abusive language is detected.

#### 3.9 **Speech Input Capability**

**Technologies Used:**
- **Speech Recognition Libraries**: For processing spoken input (optional).

**Description:**
Pepper can optionally accept speech input, making interactions more versatile and accessible.

**Implementation:**
- **Speech Recognition**: Using libraries like SpeechRecognition to process and understand user speech.

### 4. **User Interaction Flow**

1. **Face Detection**: Detect and verify the user.
2. **Greeting**: Perform a greeting sequence including gestures and speech.
3. **Conversation**: Engage in dialogue to assist with course selection.
4. **Course Recommendation**: Provide course recommendations based on user input.
5. **Farewell**: End the interaction with a polite farewell.
6. **Handle Abusive Language**: Detect and address inappropriate language.

### 5. **Testing and Evaluation**

#### 5.1 **Face Detection Accuracy**
- **Objective**: Ensure reliable face detection and tracking.
- **Method**: Tested under various lighting conditions and distances.
- **Results**: Achieved high accuracy in face detection with occasional errors in low light.

#### 5.2 **User Engagement**
- **Objective**: Evaluate user satisfaction with interactions.
- **Method**: User feedback collected during testing.
- **Results**: Positive feedback on multi-modal greetings and gesture integration.

#### 5.3 **Course Recommendation Effectiveness**
- **Objective**: Assess the relevance and accuracy of course recommendations.
- **Method**: Simulated user inputs and evaluated recommendations.
- **Results**: Recommendations aligned well with user preferences; Bayesian model performance was promising.

#### 5.4 **System Robustness**
- **Objective**: Ensure the system handles errors gracefully.
- **Method**: Simulated errors and interruptions.
- **Results**: System demonstrated resilience and effective error handling.

### 6. **Challenges and Future Work**

#### 6.1 **Challenges**
- **Face Detection Noise**: Occasionally affected by environmental conditions.
- **Speech Recognition Limitations**: Background noise impacted speech processing.

#### 6.2 **Future Work**
- **Enhanced Face Recognition**: Integrate advanced facial recognition for improved user verification.
- **Advanced NLP Models**: Utilize more sophisticated models for dialogue management.
- **Real-World Deployment**: Test the system in real-world environments for further evaluation.

### 7. **Marketing and Branding**

**Robot Name**: Pepper Assistant  
**Slogan**: "Your Academic Companion – Navigate Your Course Choices with Pepper!"

### 8. **Conclusion**

The development of the Pepper Assistant robot successfully integrated various human-centered interaction techniques to provide an engaging and helpful academic assistant. The project demonstrated the potential of combining robotics with social interaction and advanced algorithms to create a useful tool for students. The Pepper Assistant stands as a prototype for future developments in socially assistive robotics, offering a foundation for continued research and application.

---

**Submitted by:** [Your Name]  
**Date:** [Submission Date]  

---

This detailed report outlines the project’s scope, system design, implementation details, testing procedures, and future work, suitable for a master's level submission in robotics. Adjust the specifics based on actual implementations and findings.