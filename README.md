
# Multimodal Biometric System (Iris + Fingerprint Recognition)

This project implements a **Multimodal Biometric Authentication System** using Python. The system verifies users by analyzing **iris** and **fingerprint** images. It provides a graphical interface for enrolling and identifying users using both biometric modalities.

## 🧠 Features

- GUI built with **Tkinter**
- Iris and fingerprint image acquisition via file selection
- Matching and verification of users based on pre-enrolled images
- Data persistence using JSON for enrolled users
- Image display and status notifications in the GUI

## 📸 Modalities Used

1. **Iris Recognition**: Compares input iris image with enrolled data using feature matching (based on OpenCV image processing).
2. **Fingerprint Recognition**: Uses similar image matching logic for fingerprint analysis.

## 🛠️ Tech Stack

- Python 3.x
- [Tkinter](https://docs.python.org/3/library/tkinter.html) - GUI
- [OpenCV](https://opencv.org/) - Image processing
- [PIL / Pillow](https://pillow.readthedocs.io/) - Image manipulation
- JSON - Data storage

## 📂 Project Structure

```plaintext
.
├── biometric_gui.py          # Main application file
├── data/
│   ├── users.json            # Stores enrolled user data
│   └── enrolled_images/      # Directory for stored iris/fingerprint images
├── assets/
│   └── icons/                # Optional: icons used in GUI
└── README.md
````

## 🚀 How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/multimodal-biometrics.git
cd multimodal-biometrics
```

### 2. Install Dependencies

Ensure you have Python 3.x installed. Then, install the required packages:

```bash
pip install opencv-python Pillow numpy
```

### 3. Run the App

```bash
python biometric_gui.py
```

## ✅ Usage

### Enroll a New User

1. Click **Enroll**.
2. Select the user's iris and fingerprint images.
3. Provide a user ID or name.
4. Images are stored and data saved to `users.json`.

### Authenticate a User

1. Click **Authenticate**.
2. Select iris and fingerprint images.
3. The system will match them against the enrolled dataset.
4. If a match is found, the user is authenticated.

## 📌 Limitations

* Basic image matching (not using deep learning).
* Sensitive to image quality and lighting.
* Not designed for large-scale deployment.

## 🔒 Disclaimer

This project is a **proof of concept** and **not suitable for production** use where high security is required. It is intended for learning and research purposes.

## 📧 Contact

For questions or collaboration, contact: [youremail@example.com](mailto:youremail@example.com)

---

**License**: MIT

