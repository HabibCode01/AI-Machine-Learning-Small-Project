from ultralytics import YOLO

def train_custom_model():
    # Load pre-trained lightweight YOLO model weights
    model = YOLO("yolov8n.pt") 
    
    # Train the model (points to your dataset configuration file)
    model.train(
        data="path/to/dataset/data.yaml", 
        epochs=10, 
        imgsz=640, 
        device="cpu" # Change to '0' if you have an active NVIDIA GPU
    )

if __name__ == "__main__":
    # Uncomment to execute a local training job
    # train_custom_model()
    pass