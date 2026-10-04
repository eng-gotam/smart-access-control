\# 🔐 Smart Access Control System



An AI-powered access control system that uses \*\*face detection, face recognition, and authorization logic\*\* to determine whether a person should be granted or denied access.



The system can detect multiple people at the same time and follows a strict security rule:



> \*\*The gate opens only when every detected person is authorized.\*\*



If even one unauthorized person is detected, access is denied.



\## 🚀 Live Demo



\*\*Streamlit App:\*\*

https://smart-access-control-gwvgdraw2crlzu3ndjqwmp.streamlit.app/



\*\*GitHub Repository:\*\*

https://github.com/eng-gotam/smart-access-control



\---



\## 📌 Project Overview



Traditional access control systems often rely on physical cards, passwords, or manual verification.



This project demonstrates how computer vision and face recognition can be used to build an automated access control system.



The system:



1\. Captures an image from the camera.

2\. Detects faces using \*\*OpenCV YuNet\*\*.

3\. Extracts face features using \*\*OpenCV SFace\*\*.

4\. Compares the detected face with registered face embeddings.

5\. Determines whether each person is authorized.

6\. Applies multi-person authorization logic.

7\. Logs the access attempt.

8\. Displays whether the gate should open or remain closed.



\---



\## 🧠 System Architecture



```text

&#x20;                   Camera

&#x20;                     │

&#x20;                     ▼

&#x20;             ┌───────────────┐

&#x20;             │ Face Detection│

&#x20;             │    YuNet      │

&#x20;             └───────┬───────┘

&#x20;                     │

&#x20;                     ▼

&#x20;             ┌───────────────┐

&#x20;             │ Face Alignment│

&#x20;             │   \& Feature   │

&#x20;             │   Extraction  │

&#x20;             │     SFace     │

&#x20;             └───────┬───────┘

&#x20;                     │

&#x20;                     ▼

&#x20;             ┌───────────────┐

&#x20;             │ Face Database  │

&#x20;             │  Embeddings    │

&#x20;             └───────┬───────┘

&#x20;                     │

&#x20;                     ▼

&#x20;             ┌───────────────┐

&#x20;             │ Authorization  │

&#x20;             │     Engine     │

&#x20;             └───────┬───────┘

&#x20;                     │

&#x20;             ┌───────┴────────┐

&#x20;             ▼                ▼

&#x20;       All Authorized?     Any Unknown?

&#x20;             │                │

&#x20;             ▼                ▼

&#x20;       🟢 ACCESS GRANTED   🔴 ACCESS DENIED

&#x20;             │                │

&#x20;             ▼                ▼

&#x20;        Gate Opens        Gate Closed

&#x20;                     │

&#x20;                     ▼

&#x20;               Access Logger

&#x20;                     │

&#x20;                     ▼

&#x20;                 SQLite DB

```



\---



\## 🔑 Multi-Person Security Logic



The system uses an \*\*all-authorized policy\*\*.



| Detected People   | Decision          |

| ----------------- | ----------------- |

| Gotam             | 🟢 Access Granted |

| Unknown           | 🔴 Access Denied  |

| Gotam + Gotam     | 🟢 Access Granted |

| Gotam + Unknown   | 🔴 Access Denied  |

| Unknown + Unknown | 🔴 Access Denied  |



This prevents an unauthorized person from entering by simply standing beside an authorized person.



\### Example



```text

Person 1 → Gotam → AUTHORIZED

Person 2 → Unknown → UNAUTHORIZED



&#x20;               ↓



&#x20;        ACCESS DENIED



&#x20;               ↓



&#x20;       Gate remains CLOSED

```



\---



\## 🛠️ Technologies Used



\### Programming



\* Python

\* SQLite



\### Computer Vision



\* OpenCV

\* YuNet

\* SFace



\### Machine Learning / AI



\* Face detection

\* Face recognition

\* Face embeddings

\* Cosine similarity



\### Web Application



\* Streamlit



\### Development Tools



\* Git

\* GitHub

\* PowerShell

\* VS Code



\---



\## 📂 Project Structure



```text

smart-access-control/

│

├── models/

│   ├── face\_detection\_yunet\_2023mar.onnx

│   └── face\_recognition\_sface\_2021dec.onnx

│

├── app.py

├── streamlit\_app.py

│

├── authorization.py

├── face\_detection.py

├── face\_recognation.py

├── face\_database.py

├── gate\_controller.py

├── database1.py

├── logger.py

│

├── requirements.txt

├── .gitignore

└── README.md

```



> Registered face images and face embeddings are intentionally excluded from the public repository.



\---



\## 🔍 Core Components



\### 1. Face Detection



`face\_detection.py`



Uses \*\*OpenCV YuNet\*\* to detect faces in an image.



The detector returns the bounding box and facial landmark information for each detected face.



\---



\### 2. Face Recognition



`face\_recognation.py`



Uses \*\*OpenCV SFace\*\* to:



\* Align detected faces

\* Generate face embeddings

\* Compare embeddings using cosine similarity



Example similarity values observed during testing:



```text

0.61

0.63

0.67

0.71

0.74

```



Higher similarity indicates a stronger match.



\---



\### 3. Authorization



`authorization.py`



The authorization module compares the detected face embedding against registered users.



The system identifies:



```text

Known person

&#x20;    ↓

Similarity threshold

&#x20;    ↓

Authorized / Unauthorized

```



Unknown faces are rejected.



\---



\### 4. Gate Controller



`gate\_controller.py`



The gate controller represents the physical gate logic.



Current implementation simulates:



```text

ACCESS AUTHORIZED

&#x20;       ↓

GATE OPENED

&#x20;       ↓

Timeout

&#x20;       ↓

GATE CLOSED

```



For unauthorized access:



```text

ACCESS DENIED

&#x20;       ↓

GATE REMAINS CLOSED

```



The project can later be connected to real hardware such as a relay, servo motor, or electronic door lock.



\---



\### 5. Database



`database1.py`



Uses SQLite to store system data and access records.



The database supports:



\* User authorization

\* Access logs

\* Timestamps

\* Similarity scores



\---



\### 6. Logger



`logger.py`



Records access attempts such as:



```text

Gotam | AUTHORIZED | 0.67

Unknown | UNAUTHORIZED | 0.34

```



Example access history:



```text

ID | Name    | Status       | Score | Timestamp

\--------------------------------------------------

36 | gotam   | AUTHORIZED   | 0.65  | 2026-10-04

35 | gotam   | AUTHORIZED   | 0.68  | 2026-10-04

34 | gotam   | AUTHORIZED   | 0.63  | 2026-10-04

30 | Unknown | UNAUTHORIZED | 0.58  | 2026-10-04

```



\---



\## 🌐 Streamlit Deployment



The project includes a separate Streamlit application:



```text

streamlit\_app.py

```



The deployed application uses the browser camera instead of directly accessing the server's webcam.



The deployed pipeline is:



```text

Browser Camera

&#x20;     ↓

Image Capture

&#x20;     ↓

YuNet

&#x20;     ↓

SFace

&#x20;     ↓

Authorization

&#x20;     ↓

Access Decision

&#x20;     ↓

SQLite Logging

```



\### Run Locally



Install dependencies:



```bash

pip install -r requirements.txt

```



Start the Streamlit application:



```bash

streamlit run streamlit\_app.py

```



Then open the local Streamlit URL shown in the terminal.



\---



\## 📦 Dependencies



The project uses:



```text

streamlit

opencv-contrib-python-headless

numpy

```



See `requirements.txt` for the exact versions.



\---



\## 🔒 Security \& Privacy



Face images and face embeddings are \*\*not included in the public GitHub repository\*\*.



The following files are intentionally excluded:



```text

data/users/

face\_database.pkl

access\_control.db

```



The deployed application uses protected configuration for the face database rather than exposing biometric data publicly.



\---



\## 🧪 Testing



The project includes separate testing scripts:



```text

test\_face.py

test\_recognition.py

test\_authorization.py

```



These were used to validate:



\* Face detection

\* Face feature extraction

\* Face recognition

\* Authorization decisions



\---



\## 📊 Example Results



\### Authorized Person



```text

Detected: Gotam

Similarity: 0.71



ACCESS GRANTED

Gate would OPEN

```



\### Unknown Person



```text

Detected: Unknown

Similarity: below authorization threshold



ACCESS DENIED

Gate would remain CLOSED

```



\### Authorized + Unknown



```text

Gotam      → AUTHORIZED

Unknown    → UNAUTHORIZED



ACCESS DENIED

Gate would remain CLOSED

```



This demonstrates the system's multi-person security policy.



\---



\## 🎯 Current Features



\* \[x] Face detection

\* \[x] Face recognition

\* \[x] Face embeddings

\* \[x] Multiple face detection

\* \[x] User authorization

\* \[x] Multi-person access control

\* \[x] Gate simulation

\* \[x] Access logging

\* \[x] SQLite database

\* \[x] Streamlit web interface

\* \[x] Streamlit Cloud deployment

\* \[x] Protected face database

\* \[x] GitHub repository



\---



\## 🚧 Future Improvements



Possible future upgrades include:



\* Real electronic gate/door hardware integration

\* Real-time browser video stream

\* User registration interface

\* Admin dashboard

\* Access statistics and analytics

\* Email/SMS security alerts

\* Anti-spoofing / liveness detection

\* Better face database management

\* Role-based access control

\* Multiple access zones

\* Cloud database integration



\---



\## 💡 Learning Outcomes



This project provided practical experience with:



\* Computer vision

\* Face detection

\* Face recognition

\* Feature embeddings

\* Similarity matching

\* Authorization systems

\* Multi-person security logic

\* SQLite

\* Python modular architecture

\* Streamlit

\* Git and GitHub

\* Cloud deployment



\---



\## 👨‍💻 Author



\*\*Gotam Kumar\*\*



BS Artificial Intelligence Student



GitHub:

https://github.com/eng-gotam



\---



\## ⭐ Project Status



\*\*Completed — Portfolio MVP\*\*



The system has been tested locally and deployed successfully using Streamlit Community Cloud.



