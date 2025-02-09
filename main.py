from email.policy import default
from pyexpat import model
from unittest.mock import DEFAULT
import cv2
import streamlit as st
from pathlib import Path
import sys
from ultralytics import YOLO
from PIL import Image



# Get absolute path of current file
FILE = Path(__file__).resolve()

# Get parent directory of current file
ROOT = FILE.parent

# Add root path to sys.path list
if ROOT not in sys.path:
    sys.path.append(str(ROOT))

# Get relative path of root directory wrt current working directory
ROOT = ROOT.relative_to(Path.cwd())

# Sources
IMAGE = 'Image'
VIDEO = 'Video'
SOURCE_LIST = [IMAGE, VIDEO]

# Image Config
IMAGES_DIR = ROOT/'images'
DEFAULT_IMAGE = IMAGES_DIR/'test_image_1.jpg'
DEFAULT_DETECTED_IMAGE = IMAGES_DIR/'test_image_1_results.jpg'

# VIdeo Config
VIDEOS_DIR = ROOT/'videos'
VIDEOS_DICT = {
    'Video 1': VIDEOS_DIR/'test_video_1.mp4',
    'Video 2': VIDEOS_DIR/'test_video_2.mp4',
    'Video 3': VIDEOS_DIR/'test_video_3.mp4',
}

# Model Configuration
MODEL_DIR = ROOT/'weights'
# DETECTION_MODEL = MODEL_DIR/'yolo11l.pt'
# SEGMENTATION_MODEL = MODEL_DIR/'yolo11l-seg.pt'
# POSE_MODEL = MODEL_DIR/'yolo11l-pose.pt'
DETECTION_MODEL = 'yolo11l.pt'
SEGMENTATION_MODEL = 'yolo11l-seg.pt'
POSE_MODEL = 'yolo11l-pose.pt'

# Page Layout in Streamlit
st.set_page_config(
    page_title = "YOLO11",
)

# Header
st.header("Object Detection using YOLO11")

# Sidebar
st.sidebar.header("Model Configurations")
model_type = st.sidebar.radio("Task", ["Detection", "Segmentation", "Pose Estimation"])
confidence_value = float(st.sidebar.slider("Select Model Confidence Value", 25, 100, 40))/100

# Select model
if model_type == 'Detection':
    model_path = DETECTION_MODEL
elif model_type == 'Segmentation':
    model_path = SEGMENTATION_MODEL
elif model_type == 'Pose Estimation':
    model_path = POSE_MODEL

# Load YOLO model
model = YOLO(model_path)

# Image/Video Configuration
st.sidebar.header("Image/Video Config")
source_radio = st.sidebar.radio("Select Source", SOURCE_LIST)

source_image = None
if source_radio == IMAGE:
    source_image = st.sidebar.file_uploader("Choose an Image...", type = ('jpg','png','webp','jpeg','bep'))

    col1, col2 = st.columns(2)
    with col1:
        try:
            if source_image is None:
                default_image_path = str(DEFAULT_IMAGE)
                default_image = Image.open(default_image_path)
                st.image(default_image, caption="Default Image", use_container_width=True)
            else:
                uploaded_image = Image.open(source_image)
                st.image(source_image, caption="Uploaded Image", use_container_width=True)
        except Exception as e:
            st.error("Error occured while opening the image")
            st.error(e)

    with col2:
        try:
            if source_image is None:
                default_detected_image_path = str(DEFAULT_DETECTED_IMAGE)
                default_detected_image = Image.open(default_detected_image_path)
                st.image(default_detected_image, caption="Detected Image", use_container_width=True)
            else:
                if st.sidebar.button('Submit', use_container_width=True):
                    result = model.predict(uploaded_image, conf=confidence_value)
                    boxes = result[0].boxes
                    result_plotted = result[0].plot()[:,:,::-1]
                    st.image(result_plotted, caption="Detected Image", use_container_width=True)

                    try:
                        with st.expander("Detection Results"):
                            for box in boxes:
                                st.write(box.data)
                    except Exception as e:
                        st.error(e)
        except Exception as e:
            st.error("Error occured while opening the image")
            st.error(e)

elif source_radio == VIDEO:
    #source_video = st.sidebar.file_uploader("Choose a Video...", type = ('mp4'))
    source_video = st.sidebar.selectbox("Choose a Video...", VIDEOS_DICT.keys())
    with open(VIDEOS_DICT.get(source_video), 'rb') as video_file:
        video_bytes = video_file.read()
        if video_bytes:
            st.video(video_bytes)
        if st.sidebar.button('Submit',use_container_width=True):
            try:
                video_cap = cv2.VideoCapture(str(VIDEOS_DICT.get(source_video)))
                st_frame = st.empty()
                while (video_cap.isOpened()):
                    success, image = video_cap.read()
                    if success:
                        image = cv2.resize(image, (720, int(720*(9/16))))
                        # Predict objects using YOLO11
                        result = model.predict(image, conf=confidence_value)
                        # Plot detected objects on videoframe
                        result_plotted = result[0].plot()
                        st_frame.image(result_plotted, caption = "Detected Video", channels="BGR", use_container_width=True) 
                    else:
                        video_cap.release()
                        break;
            except Exception as e:
                st.sidebar.error("Error Loading Video"+str(e))

