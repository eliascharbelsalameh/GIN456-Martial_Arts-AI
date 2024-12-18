import numpy as np
import cv2  # type: ignore
from ultralytics import YOLO  # type: ignore

# Initialize the YOLOv8 model for pose estimation
model = YOLO('yolov8n-pose.pt')

# Function to calculate the angle between three points (A, B, C where B is the vertex)
def calculate_angle(A, B, C):
    AB = np.array(A) - np.array(B)
    BC = np.array(C) - np.array(B)
    
    cosine_angle = np.dot(AB, BC) / (np.linalg.norm(AB) * np.linalg.norm(BC))
    angle = np.arccos(cosine_angle)
    
    return np.degrees(angle)

# Compare the angles calculated with the expected ranges
def check_stance(angles, ideal_stance):
    for joint, angle in angles.items():
        if not (ideal_stance[joint][0] <= angle <= ideal_stance[joint][1]):
            return False, joint, angle
    return True, None, None

# Process a single image to extract keypoints, calculate angles, and annotate the result
def process_image(image_path, output_path):
    
    frame = cv2.imread(image_path) # Load the image

    results = model(frame) # Use YOLO to get the results

    keypoints = results[0].keypoints # Access the keypoints from the results object
    
    if keypoints is None or keypoints.shape[1] < 17:  # Ensure we have all 17 keypoints
        print("Not enough keypoints detected")
        cv2.imwrite(output_path, frame)  # Save the original image if there is an error
        return False

    # Extract keypoints (xy coordinates) for the person detected (assumed to be the first person)
    keypoints_xy = keypoints.xy[0].cpu().numpy()  # Move the keypoints to CPU and convert to NumPy array
    keypoint_confidence = keypoints.conf[0].cpu().numpy()  # Move the confidence values to CPU

    # Optionally, filter out keypoints with low confidence
    min_confidence = 0.7
    valid_keypoints = keypoints_xy[keypoint_confidence > min_confidence]

    # Ensure we have enough valid keypoints for meaningful angle calculation
    if len(valid_keypoints) < 6:  # You need at least 6 valid keypoints for elbow and knee calculations
        print(f"Not enough valid keypoints detected: {len(valid_keypoints)}")
        cv2.imwrite(output_path, frame)  # Save the original image
        return False

    # Extract keypoints for specific body parts, assuming typical order
    nose = keypoints_xy[0][:2]
    left_eye = keypoints_xy[1][:2]
    right_eye = keypoints_xy[2][:2]
    left_ear = keypoints_xy[3][:2]
    right_ear = keypoints_xy[4][:2]
    left_shoulder = keypoints_xy[5][:2]  # [x, y] for the left shoulder
    right_shoulder = keypoints_xy[6][:2]
    left_elbow = keypoints_xy[7][:2]     
    right_elbow = keypoints_xy[8][:2]     
    left_wrist = keypoints_xy[9][:2]
    right_wrist = keypoints_xy[10][:2]
    left_hip = keypoints_xy[11][:2]
    right_hip = keypoints_xy[12][:2]
    left_knee = keypoints_xy[13][:2]
    right_knee = keypoints_xy[14][:2]
    left_ankle = keypoints_xy[15][:2]
    right_ankle = keypoints_xy[16][:2]

    # Calculate angles based on keypoints (example for elbow and knee)
    angles = {
        'right_elbow': calculate_angle(right_shoulder, right_elbow, right_wrist),
        'left_elbow': calculate_angle(left_shoulder, left_elbow, left_wrist),
    }

    # Check if the person's stance is correct
    is_correct, incorrect_joint, actual_angle = check_stance(angles, ideal_stance)

    
        
    # Draw keypoints
    cv2.circle(frame, (int(left_shoulder[0]), int(left_shoulder[1])), 20, (0, 255, 0), -1)  # Green for shoulder
    cv2.circle(frame, (int(left_elbow[0]), int(left_elbow[1])), 20, (255, 0, 0), -1)  # Blue for elbow
    cv2.circle(frame, (int(left_wrist[0]), int(left_wrist[1])), 20, (0, 0, 255), -1)  # Red for wrist
    cv2.circle(frame, (int(right_shoulder[0]), int(right_shoulder[1])), 20, (0, 255, 0), -1)
    cv2.circle(frame, (int(right_elbow[0]), int(right_elbow[1])), 20, (255, 0, 0), -1)  
    cv2.circle(frame, (int(right_wrist[0]), int(right_wrist[1])), 20, (0, 0, 255), -1)  

    # Draw lines connecting shoulder -> elbow -> wrist
    cv2.line(frame, (int(left_shoulder[0]), int(left_shoulder[1])), (int(left_elbow[0]), int(left_elbow[1])), (255, 255, 255), 10)
    cv2.line(frame, (int(left_elbow[0]), int(left_elbow[1])), (int(left_wrist[0]), int(left_wrist[1])), (255, 255, 255), 10)
    cv2.line(frame, (int(right_shoulder[0]), int(right_shoulder[1])), (int(right_elbow[0]), int(right_elbow[1])), (255, 255, 255), 10)
    cv2.line(frame, (int(right_elbow[0]), int(right_elbow[1])), (int(right_wrist[0]), int(right_wrist[1])), (255, 255, 255), 10)

    # Save the annotated image
    cv2.imwrite(output_path, frame)
    # print(f"Processed image saved to {output_path}")
    if is_correct:
        # print("good")
        return True
    else:
        # print("bad")
        return False

# Define ideal stance angles (for each joint you want to analyze)
ideal_stance = {
    'left_elbow': (0, 45),
    'right_elbow': (45, 150),
    # Add other keypoint angles based on your stance
}
