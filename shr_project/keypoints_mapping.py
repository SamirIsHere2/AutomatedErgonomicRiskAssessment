import os
import json
import subprocess 

import math

# COCO body keypoint names
COCO_KEYPOINT_LABELS = {
    "Nose": 0,
    "Neck": 1,
    "RShoulder": 2,
    "RElbow": 3,
    "RWrist": 4,
    "LShoulder": 5,
    "LElbow": 6,
    "LWrist": 7,
    "RHip": 8,
    "RKnee": 9,
    "RAnkle": 10,
    "LHip": 11,
    "LKnee": 12,
    "LAnkle": 13,
    "REye": 14,
    "LEye": 15,
    "REar": 16,
    "LEar": 17
}

# COCO hand keypoint names 
HAND_KEYPOINT_LABELS = {
    "Wrist": 0,
    "Thumb1": 1,
    "Thumb2": 2,
    "Thumb3": 3,
    "Thumb4": 4,
    "Index1": 5,
    "Index2": 6,
    "Index3": 7,
    "Index4": 8,
    "Middle1": 9,
    "Middle2": 10,
    "Middle3": 11,
    "Middle4": 12,
    "Ring1": 13,
    "Ring2": 14,
    "Ring3": 15,
    "Ring4": 16,
    "Pinky1": 17,
    "Pinky2": 18,
    "Pinky3": 19,
    "Pinky4": 20
}



    

# Function definitions...


# OpenPose command...

# Process JSON files...

# Process side JSON files...

'''
        keypoints = data["people"][0]["pose_keypoints_2d"]
        keypoints_hand = data["people"][0]["hand_left_keypoints_2d"]
        # Define keypoints (index * 3 to account for x, y, confidence values)
        keypoints = {i: (keypoints[i * 3], keypoints[i * 3 + 1]) for i in range(0, len(keypoints) // 3)}
        keypoints_hand = {i: (keypoints_hand[i * 3], keypoints_hand[i * 3 + 1]) for i in range(0, len(keypoints_hand) // 3)}

        angles["ANGLE_2A"] = calculate_angle(keypoints[0], keypoints[1], keypoints[11])
        angles["ANGLE_2B"] = calculate_vertical_angle(keypoints[6], keypoints[5])
        angles["ANGLE_2C"] = calculate_angle(keypoints[1], keypoints[11], keypoints[12])
        angles["ANGLE_2D"] = 180 - calculate_angle(keypoints[6], keypoints[7], keypoints_hand[5])
        angles["ANGLE_2E"] = calculate_angle(keypoints[5], keypoints[6], keypoints[7])

        print("DEBUG 2D:\n\n")

        # Accessing the x and y coordinates for "LElbow" from lbl_keypoints
        x_lelbow = lbl_keypoints["LElbow"][0]
        y_lelbow = lbl_keypoints["LElbow"][1]
        print("LElbow coordinates: ({}, {})".format(x_lelbow, y_lelbow))

        # Accessing the x and y coordinates for "LWrist" from lbl_keypoints
        x_lwrist = lbl_keypoints["LWrist"][0]
        y_lwrist = lbl_keypoints["LWrist"][1]
        print("LWrist coordinates: ({}, {})".format(x_lwrist, y_lwrist))

        # Accessing the x and y coordinates for "Index1" from lbl_keypoints_hand
        x_index1_hand = lbl_keypoints_hand["Index1"][0]
        y_index1_hand = lbl_keypoints_hand["Index1"][1]
        print("Index1 coordinates: ({}, {})".format(x_index1_hand, y_index1_hand))

      # Accessing the x and y coordinates for "LElbow" from keypoints
        x_lelbow = keypoints[6][0]
        y_lelbow = keypoints[6][1]
        print("K LElbow coordinates: ({}, {})".format(x_lelbow, y_lelbow))

        # Accessing the x and y coordinates for "LWrist" from keypoints
        x_lwrist = keypoints[7][0]
        y_lwrist = keypoints[7][1]
        print("K LWrist coordinates: ({}, {})".format(x_lwrist, y_lwrist))

        # Accessing the x and y coordinates for "Index1" from keypoints_hand
        x_index1_hand = keypoints_hand[5][0]
        y_index1_hand = keypoints_hand[5][1]
        print("K Index1 coordinates from hand keypoints: ({}, {})".format(x_index1_hand, y_index1_hand))

'''
'''
        keypoints2 = data["people"][0]["pose_keypoints_2d"]
        keypoints_hand2 = data["people"][0]["hand_right_keypoints_2d"]
        # Define keypoints (index * 3 to account for x, y, confidence values)
        keypoints2 = {i: (keypoints2[i * 3], keypoints2[i * 3 + 1]) for i in range(0, len(keypoints2) // 3)}
        keypoints_hand2 = {i: (keypoints_hand2[i * 3], keypoints_hand2[i * 3 + 1]) for i in range(0, len(keypoints_hand2) // 3)}

        angles["ANGLE_2A"] = calculate_angle(keypoints2[0], keypoints2[1], keypoints2[8])
        angles["ANGLE_2B"] = calculate_vertical_angle(keypoints2[3], keypoints2[2])
        angles["ANGLE_2C"] = calculate_angle(keypoints2[1], keypoints2[8], keypoints2[9])
        angles["ANGLE_2D"] = 180 - calculate_angle(keypoints2[3], keypoints2[4], keypoints_hand2[5])
        angles["ANGLE_2E"] = calculate_angle(keypoints2[2], keypoints2[3], keypoints2[4])
        
        # Update the JSON data with the angles
'''
'''
    if "orientation" in data and data["orientation"] == "right":
        keypoints = data["people"][0]["pose_keypoints_2d"]
        # Create a mapping from COCO keypoint labels to their respective indices
        lbl_keypoints = {label: keypoints[kp.COCO_KEYPOINT_LABELS[label]*3: (kp.COCO_KEYPOINT_LABELS[label]*3)
                        + 3] for label in kp.COCO_KEYPOINT_LABELS}
        
        keypoints_hand = data["people"][0]["hand_left_keypoints_2d"]
        # Create a mapping from COCO keypoint labels to their respective indices
        lbl_keypoints_hand = {label: keypoints_hand[kp.HAND_KEYPOINT_LABELS[label]*3: (kp.HAND_KEYPOINT_LABELS[label]*3)
                        + 3] for label in kp.HAND_KEYPOINT_LABELS}

        # Calculate the angles
        angles = {}
        # Assuming lbl_keypoints and lbl_keypoints_hand are dictionaries mapping keypoints to their indices
        # Calculate the angles using the updated keypoint labels
        sign = get_sign(lbl_keypoints["LElbow"][0], lbl_keypoints["LShoulder"][0])
        angles["ANGLE_B"] = sign * calculate_vertical_angle(lbl_keypoints["LElbow"], lbl_keypoints["LShoulder"])
        angles["ANGLE_C"] = calculate_angle(lbl_keypoints["Neck"], lbl_keypoints["LHip"], lbl_keypoints["LKnee"])
        angles["ANGLE_D"] = 180 - calculate_angle(lbl_keypoints["LElbow"], lbl_keypoints["LWrist"], lbl_keypoints_hand["Index1"])
        angles["ANGLE_E"] = calculate_angle(lbl_keypoints["LShoulder"], lbl_keypoints["LElbow"], lbl_keypoints["LWrist"])

    elif "orientation" in data and data["orientation"] == "left":
        keypoints = data["people"][0]["pose_keypoints_2d"]
        # Create a mapping from COCO keypoint labels to their respective indices
        lbl_keypoints = {label: keypoints[kp.COCO_KEYPOINT_LABELS[label]*3: (kp.COCO_KEYPOINT_LABELS[label]*3)
                        + 3] for label in kp.COCO_KEYPOINT_LABELS}
        
        
        # Calculate the angles
        angles = {}
        
        # Calculate the angles using the provided keypoint labels
        angles["ANGLE_A"] = 180 - calculate_angle(lbl_keypoints["REar"], lbl_keypoints["Neck"], lbl_keypoints["RHip"])
        sign = get_sign(lbl_keypoints["RElbow"][0], lbl_keypoints["RShoulder"][0])
        angles["ANGLE_B"] = sign * calculate_vertical_angle(lbl_keypoints["RElbow"], lbl_keypoints["RShoulder"])

        angles["ANGLE_C"] = calculate_angle(lbl_keypoints["Neck"], lbl_keypoints["RHip"], lbl_keypoints["RKnee"])
        angles["ANGLE_D"] = 180 - calculate_angle(lbl_keypoints["RElbow"], lbl_keypoints["RWrist"], lbl_keypoints_hand["Index1"])
        angles["ANGLE_E"] = calculate_angle(lbl_keypoints["RShoulder"], lbl_keypoints["RElbow"], lbl_keypoints["RWrist"])
        '''