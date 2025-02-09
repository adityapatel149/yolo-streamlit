# YOLO11 Streamlit App

Object Detection, segmentation, and pose estimation for Images and Videos

This repository contains a Streamlit web application for performing object detection, segmentation, and pose estimation on images and videos using the YOLO11 model.

## Demo

The application is deployed at: [YOLO11 Streamlit App](https://yolo-aditya-patel.streamlit.app)

## Features
- **Object Detection**: Detects objects in images and videos.
- **Segmentation**: Performs instance segmentation.
- **Pose Estimation**: Estimates human poses.
- **Supports Images and Videos**: Users can upload their own images or select from preloaded videos.

## Installation

### Prerequisites
Make sure you have Python installed (>=3.8).

### Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/yolo11-streamlit-app.git
   cd yolo11-streamlit-app
   ```

2. Create a virtual environment (optional but recommended):
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Run the application:
   ```sh
   streamlit run main.py
   ```

## Usage
1. Open the app in your browser.
2. Select the model type (Detection, Segmentation, or Pose Estimation) from the sidebar.
3. Adjust the confidence threshold.
4. Upload an image or select a video.
5. Click submit to process the input and display results.

## File Structure
```
📦 yolo11-streamlit-app
├── images/              # Default test images
├── videos/              # Default test videos
├── weights/             # YOLO11 model weights
├── main.py              # Streamlit app script
├── requirements.txt     # Dependencies
└── README.md            # Documentation
```

## Requirements
Below is the `requirements.txt` file for setting up the necessary dependencies:
```
streamlit
opencv-python
ultralytics
Pillow
```

## Acknowledgments
- Built using [Streamlit](https://streamlit.io/)
- YOLO model provided by [Ultralytics](https://ultralytics.com/)

## License
This project is open-source and available under the [MIT License](LICENSE).

