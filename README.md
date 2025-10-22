# Yolov5_football: Real-time Football Player Detection

## Description

This project implements a real-time football player detection application using YOLOv5. It identifies and tracks players on the field from video footage. The application utilizes existing video datasets with corresponding JSON annotations to train a YOLOv5 model for player detection. The `create_yolo_format_dataset.py` script is used to convert the dataset into the format required by YOLOv5.

## Features and Functionality

*   **Real-time Player Detection:** Employs YOLOv5 for fast and accurate player detection in video streams.
*   **Dataset Conversion:**  Includes a script (`create_yolo_format_dataset.py`) to convert existing football video datasets with JSON annotations into YOLOv5-compatible format. Specifically, it handles datasets where annotations are in a COCO-like JSON format.
*   **Training and Validation Data Preparation:**  The conversion script separates the data into training and validation sets.
*   **Bounding Box Generation:** Generates bounding box coordinates in the YOLOv5 format (center x, center y, width, height, normalized).
*   **Class Labeling:** Assigns class labels (0 or 1) to detected objects based on their category ID in the JSON annotations (category ID 3 becomes class 0, everything else becomes class 1).
*   **File Naming Convention:** The converted dataset uses a specific naming convention for images and label files: `{video_id}_{frame_number}.jpg` and `{video_id}_{frame_number}.txt`, respectively.

## Technology Stack

*   **YOLOv5:**  Object detection framework.
*   **Python:**  Programming language.
*   **OpenCV (cv2):**  For video processing and image handling.
*   **JSON:**  For reading annotation data.
*   **glob:** Used for locating files

## Prerequisites

Before you begin, ensure you have met the following requirements:

*   **Python 3.6+:**  Install Python from [https://www.python.org/downloads/](https://www.python.org/downloads/).
*   **YOLOv5 Dependencies:** Install the necessary packages for YOLOv5.  A `requirements.txt` file (if one exists in the root of the repository after cloning) should be used to install these dependencies. Otherwise, install the dependencies manually. Common dependencies might include `torch`, `torchvision`, `opencv-python`, etc.

    ```bash
    pip install torch torchvision torchaudio
    pip install opencv-python
    ```

*   **CUDA (Optional):** If you have an NVIDIA GPU, install CUDA and cuDNN for accelerated training and inference. Refer to the NVIDIA documentation for installation instructions.
*   **Dataset:**  You will need a dataset of football videos with corresponding JSON annotations in a COCO-like format.  The JSON should contain `images` and `annotations` keys, with `image_id`, `category_id`, and `bbox` information for each annotation. The script expects the dataset to be organized in a directory structure like `data/football_{train/val}/{video_name}/{video.mp4, annotations.json}`.

## Installation Instructions

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/vanhdev-web/Yolov5_football.git
    cd Yolov5_football
    ```

2.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt # If a requirements.txt file exists, or manually install dependencies
    ```

## Usage Guide

### Dataset Preparation

1.  **Organize your dataset:** Ensure your football video dataset is structured as follows:

    ```
    Yolov5_football/
    └── data/
        └── football_train/
            └── video1/
                ├── video1.mp4
                └── annotations.json
            └── video2/
                ├── video2.mp4
                └── annotations.json
        └── football_val/
            └── video3/
                ├── video3.mp4
                └── annotations.json

    ```

    The `annotations.json` file should contain the bounding box information in the COCO format. Example format:

    ```json
    {
        "images": [
            {"id": 1, "width": 1920, "height": 1080, "file_name": "frame1.jpg"},
            {"id": 2, "width": 1920, "height": 1080, "file_name": "frame2.jpg"}
        ],
        "annotations": [
            {"id": 1, "image_id": 1, "category_id": 3, "bbox": [100, 200, 50, 80]},
            {"id": 2, "image_id": 1, "category_id": 2, "bbox": [300, 400, 60, 90]},
            {"id": 3, "image_id": 2, "category_id": 3, "bbox": [150, 250, 55, 85]}
        ]
    }
    ```
    `category_id` of 3 is mapped to class 0, while other categories greater than or equal to 2, such as category ID of 2, are mapped to class 1.

2.  **Run the dataset conversion script:**

    ```bash
    python create_yolo_format_dataset.py
    ```

    Before running, edit the script to change the `is_train` variable. Set `is_train = True` to process the training data and `is_train = False` to process the validation data. The `root` and `output_path` variables may also need adjusting.

    ```python
    is_train = False  # Set to True for training data, False for validation data
    mode = "train" if is_train else "val"
    root = "data/football_{}".format(mode) # Path to the folder containing the video and json files
    output_path = "../football/football_yolo" # Path to the folder that will contain the converted dataset
    ```

    This script will create the following directory structure under the `output_path`:

    ```
    football_yolo/
    ├── images/
    │   ├── train/
    │   │   ├── 1_1.jpg
    │   │   ├── 1_2.jpg
    │   │   └── ...
    │   └── val/
    │       ├── 2_1.jpg
    │       ├── 2_2.jpg
    │       └── ...
    └── labels/
        ├── train/
        │   ├── 1_1.txt
        │   ├── 1_2.txt
        │   └── ...
        └── val/
            ├── 2_1.txt
            ├── 2_2.txt
            └── ...
    ```

3.  **Configure YOLOv5:**

    *   Download or clone the YOLOv5 repository from [https://github.com/ultralytics/yolov5](https://github.com/ultralytics/yolov5).
    *   Copy the generated `football_yolo` directory (containing `images` and `labels` folders) into the `yolov5/data` directory (or wherever you prefer to keep your datasets).
    *   Create a YAML file (e.g., `football.yaml`) in the `yolov5/data` directory to define the dataset configuration. This file should specify the paths to the training and validation images and labels, as well as the number of classes and class names. Example `football.yaml`:

        ```yaml
        train: ../football/football_yolo/images/train/  # train images (relative to yolov5 directory)
        val: ../football/football_yolo/images/val/  # val images (relative to yolov5 directory)

        nc: 2  # number of classes
        names: ['player_type_1', 'player_type_2']  # class names
        ```

4.  **Train the YOLOv5 model:**

    Navigate to the YOLOv5 directory in your terminal and run the training script, specifying the dataset configuration file, model architecture, and other training parameters.

    ```bash
    cd yolov5
    python train.py --img 640 --batch 16 --epochs 100 --data data/football.yaml --weights yolov5s.pt --cache
    ```

    *   `--img`:  Image size for training.
    *   `--batch`:  Batch size.
    *   `--epochs`:  Number of training epochs.
    *   `--data`:  Path to the dataset configuration file (e.g., `data/football.yaml`).
    *   `--weights`:  Pre-trained weights to use (e.g., `yolov5s.pt`, `yolov5m.pt`). Download these from the YOLOv5 repository if you don't have them.
    *   `--cache`: Cache images for faster training.

5.  **Run Inference:**
    After training, use the `detect.py` script to run inference on video files or live camera feeds.

    ```bash
    python detect.py --weights runs/train/exp/weights/best.pt --source football_video.mp4
    ```

    * `--weights`: Path to the trained weights file (`best.pt` from the training run).
    * `--source`: Path to the video file or camera ID.

## API Documentation

This project primarily focuses on object detection using YOLOv5 and data conversion. There isn't a dedicated API in the traditional sense. The main interaction point is through the YOLOv5 framework and the dataset preparation script. Please refer to the YOLOv5 documentation for API details on model loading, inference, and other functionalities.

## Contributing Guidelines

Contributions are welcome!  To contribute to this project, follow these steps:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes and commit them with descriptive commit messages.
4.  Test your changes thoroughly.
5.  Submit a pull request to the `main` branch.

## License Information

License is unspecified.

## Contact/Support Information

For questions, bug reports, or general inquiries, please contact the repository owner through GitHub.