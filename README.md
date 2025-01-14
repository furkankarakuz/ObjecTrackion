# ObjecTrackion 

ObjecTrackion is a versatile object recognition and tracking project that can analyze any video feed displayed on the main screen, including movies, TV shows, games, or city cameras. The project leverages state-of-the-art object detection techniques to provide seamless and customizable object recognition capabilities. 🔍

## Example Video 1
https://github.com/user-attachments/assets/2702eb68-c64b-4f2a-a036-af89cd026178

## Example Video 2
https://github.com/user-attachments/assets/5b1eeb6e-bb8f-4832-9c6d-d96bf6f706a6

## Features 🌟

- **Universal Object Recognition**: Perform object detection on any content displayed on the screen without restrictions. 📽
- **Logging & Notifications**: Automatically log detected objects and send notification messages based on recognition results. ✉️
- **Customizable Settings**: Adjust screen resolution, FPS, and other parameters for optimized performance. 🔄
- **Highlighted Object Detection**: Detected objects are displayed with bounding boxes on the screen for clear visibility. 🖥️
- **Automated Logging**: Recognized objects are logged and saved to a file automatically for future reference. 🗂️
- **Smart Notifications**: Send notifications based on specific object detection criteria to keep you informed in real time. 🔔

## Requirements 📦

Before running the project, make sure you have the following dependencies installed:

```bash
pip install -r requirements.txt
```

The `requirements.txt` includes:
- TensorFlow
- Keras
- OpenCV
- NumPy
- Matplotlib

## Setup 🛠️

1. Clone the repository:

```bash
git clone https://github.com/furkankarakuz/ObjecTrackion.git
```

2. Navigate to the project directory:

```bash
cd ObjecTrackion
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Desktop Interface (GUI) 🖥️
This project includes a Desktop GUI built with PyQt5 for an interactive and user-friendly experience.
To install the required dependency, run the following command:
```bash
pip install PyQt5
```
With PyQt5 installed, you can enjoy an intuitive desktop interface for running and interacting with the object detection and tracking system

## YOLO Configuration ⚙️

- ObjecTrackion uses the **YOLO (You Only Look Once)** algorithm for object detection.
- The objects recognized by the system are based on the **COCO dataset**.
- To customize the object names, you can modify the `coco.names` file found in the project directory.

## Supported Object Classes 🏷️
- person
- bicycle
- car
- motorcycle
- airplane
- bus
- train
- truck
- boat
- and more...

For a full list of object classes, refer to the COCO dataset class labels.


## Usage 🚀

Start the application:

```bash
python main.py
```



## Contributing 🤝

Contributions are welcome! Feel free to open an issue or submit a pull request to enhance ObjecTrackion.

## License 📄

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

✨ **ObjecTrackion**: Making object detection accessible and adaptable for any screen! ✨
