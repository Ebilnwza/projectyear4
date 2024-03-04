from ultralytics import YOLO
import cv2

class LICENSEPLATE_DETECTION:
    def __init__(self, model_path):
        # Load the YOLO model
        self.model = YOLO(model_path)
        
    def __call__(self, input_image, output_path):
        # Read the image to be detected
        img = cv2.imread(input_image)
        
        # Detect and store the results
        results = self.model(input_image)[0]

        # Variable to count the number of detected boxes
        count_boxes = 0

        # Confidence threshold for detection
        confidence_threshold = 0.5  # Adjust this value as needed

        # Loop through the detected boxes
        for i in range(len(results.boxes.data)):
            # Extract box information
            boxes = results.boxes.data[i].numpy().tolist()
            
            # Check if the confidence is above the threshold
            if boxes[4] > confidence_threshold:
                # Create bounding box 
                cv2.rectangle(img, (int(boxes[0]), int(boxes[1])),
                              (int(boxes[2]), int(boxes[3])), [0, 0, 255], 2)

                # Increment the count of detected boxes
                count_boxes += 1

                # Add text indicating class and confidence
                cv2.putText(img,
                            f'{results.names[int(boxes[5])]}:{int(boxes[4]*100)}%',
                            (int(boxes[0]), int(boxes[1] - 2)),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            [225, 0, 0],
                            thickness=2)

        # Add text indicating the total number of detected boxes
        cv2.putText(img,
                    f'Total Boxes: {count_boxes}',
                    (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    2,
                    [0, 0, 0],
                    thickness=3)

        # Save the processed image to the output_path
        cv2.imwrite(output_path, img)

        # Print the total number of detected boxes
        print(f"Total number of detected boxes: {count_boxes}")