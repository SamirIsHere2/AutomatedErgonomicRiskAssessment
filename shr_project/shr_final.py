import os
import json
import subprocess
import math
import keypoints_mapping as kp

def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def calculate_angle(point1, point2, point3):
    a = distance(point2, point3)
    b = distance(point1, point2)
    c = distance(point1, point3)
    angle = math.acos((b**2 + a**2 - c**2) / (2 * b * a))
    return math.degrees(angle)

def calculate_vertical_angle(point1, point2):
    vertical_point = (point2[0], point1[1])
    return calculate_angle(point1, point2, vertical_point)

def determine_orientation(keypoint_8, keypoint_11):
    if isinstance(keypoint_8, list) and isinstance(keypoint_11, list):
        if keypoint_11[1] > keypoint_8[1]:  # Compare Y values
            return "right"
        else:
            return "left"  # Assume left if they are at the same level or keypoint 8 is lower
    else:
        return "unknown"
'''


def process_json_file(json_file_path, keypoints, keypoints_hand, orientation):
    with open(json_file_path, "r") as file:
        data = json.load(file)
    
    if "people" in data and len(data["people"]) > 0 and "pose_keypoints_2d" in data["people"][0]:
        lbl_keypoints = {label: keypoints[kp.COCO_KEYPOINT_LABELS[label]*3: (kp.COCO_KEYPOINT_LABELS[label]*3)+3] for label in kp.COCO_KEYPOINT_LABELS}

        if orientation == "right":
            lbl_keypoints_hand = {label: keypoints_hand[kp.HAND_KEYPOINT_LABELS[label]*3: (kp.HAND_KEYPOINT_LABELS[label]*3)+3] for label in kp.HAND_KEYPOINT_LABELS}

            angles = {}
            angles["ANGLE_A"] = calculate_angle(lbl_keypoints["Nose"], lbl_keypoints["Neck"], lbl_keypoints["LHip"])
            angles["ANGLE_B"] = calculate_vertical_angle(lbl_keypoints["LElbow"], lbl_keypoints["LShoulder"])
            angles["ANGLE_C"] = calculate_angle(lbl_keypoints["Neck"], lbl_keypoints["LHip"], lbl_keypoints["LKnee"])
            angles["ANGLE_D"] = 180 - calculate_angle(lbl_keypoints["LElbow"], lbl_keypoints["LWrist"], lbl_keypoints_hand["Index1"])
            angles["ANGLE_E"] = calculate_angle(lbl_keypoints["LShoulder"], lbl_keypoints["LElbow"], lbl_keypoints["LWrist"])

            data.update(angles)

    with open(json_file_path, "w") as file:
        json.dump(data, file, indent=4)

def main():
    openpose_demo_exe = ".\\build\\x64\\Release\\OpenPoseDemo.exe"
    input_dir = "in_img"
    output_images_dir = "out_img"
    output_json_dir = "out_json"

    command = [
        openpose_demo_exe,
        "--image_dir", input_dir,
        "--write_images", output_images_dir,
        "--write_images_format", "jpg",
        "--model_pose", "COCO",
        "--hand",
        "--write_json", output_json_dir
    ]

    subprocess.run(command, check=True)

    for json_file in os.listdir(output_json_dir):
        json_file_path = os.path.join(output_json_dir, json_file)
        keypoints = data["people"][0]["pose_keypoints_2d"]
        keypoints_hand = data["people"][0]["hand_left_keypoints_2d"]
        orientation = determine_orientation(keypoints[8], keypoints[11])
        process_json_file(json_file_path, keypoints, keypoints_hand, orientation)

if __name__ == "__main__":
    main()


'''


# (Previous function definitions remain unchanged)

#def process_json_file(json_file_path, keypoints, keypoints_hand, orientation):
def process_json_file(data, json_file_path, keypoints, keypoints_hand, orientation):

    with open(json_file_path, "r") as file:
        data = json.load(file)
    
    if "people" in data and len(data["people"]) > 0 and "pose_keypoints_2d" in data["people"][0]:
        lbl_keypoints = {label: keypoints[kp.COCO_KEYPOINT_LABELS[label]*3: (kp.COCO_KEYPOINT_LABELS[label]*3)+3] for label in kp.COCO_KEYPOINT_LABELS}
        
        if orientation == "right":
            lbl_keypoints_hand = {label: keypoints_hand[kp.HAND_KEYPOINT_LABELS[label]*3: (kp.HAND_KEYPOINT_LABELS[label]*3)+3] for label in kp.HAND_KEYPOINT_LABELS}
            
            angles = {}
            # Calculate the angles using the provided keypoint labels
            angles["ANGLE_A"] = calculate_angle(lbl_keypoints["Nose"], lbl_keypoints["Neck"], lbl_keypoints["LHip"])
            angles["ANGLE_B"] = calculate_vertical_angle(lbl_keypoints["LElbow"], lbl_keypoints["LShoulder"])
            angles["ANGLE_C"] = calculate_angle(lbl_keypoints["Neck"], lbl_keypoints["LHip"], lbl_keypoints["LKnee"])
            angles["ANGLE_D"] = 180 - calculate_angle(lbl_keypoints["LElbow"], lbl_keypoints["LWrist"], lbl_keypoints_hand["Index1"])
            angles["ANGLE_E"] = calculate_angle(lbl_keypoints["LShoulder"], lbl_keypoints["LElbow"], lbl_keypoints["LWrist"])
            data.update(angles)
    else:
        lbl_keypoints = {label: keypoints[kp.COCO_KEYPOINT_LABELS[label]*3: (kp.COCO_KEYPOINT_LABELS[label]*3)+3] for label in kp.COCO_KEYPOINT_LABELS}
        lbl_keypoints_hand = {label: keypoints_hand[kp.HAND_KEYPOINT_LABELS[label]*3: (kp.HAND_KEYPOINT_LABELS[label]*3)+3] for label in kp.HAND_KEYPOINT_LABELS}

        angles = {}
        # Calculate the angles using the provided keypoint labels
        angles["ANGLE_A"] = calculate_angle(lbl_keypoints["Nose"], lbl_keypoints["Neck"], lbl_keypoints["RHip"])
        angles["ANGLE_B"] = calculate_vertical_angle(lbl_keypoints["RElbow"], lbl_keypoints["RShoulder"])
        angles["ANGLE_C"] = calculate_angle(lbl_keypoints["Neck"], lbl_keypoints["RHip"], lbl_keypoints["RKnee"])
        angles["ANGLE_D"] = 180 - calculate_angle(lbl_keypoints["RElbow"], lbl_keypoints["RWrist"], lbl_keypoints_hand["Index1"])
        angles["ANGLE_E"] = calculate_angle(lbl_keypoints["RShoulder"], lbl_keypoints["RElbow"], lbl_keypoints["RWrist"])
        data.update(angles)

    with open(json_file_path, "w") as file:
        json.dump(data, file, indent=4)

def main():
    openpose_demo_exe = ".\\build\\x64\\Release\\OpenPoseDemo.exe"
    input_dir = "in_img"
    output_images_dir = "out_img"
    output_json_dir = "out_json"

    command = [
        openpose_demo_exe,
        "--image_dir", input_dir,
        "--write_images", output_images_dir,
        "--write_images_format", "jpg",
        "--model_pose", "COCO",
        "--hand",
        "--write_json", output_json_dir
    ]

    subprocess.run(command, check=True)

    for json_file in os.listdir(output_json_dir):
        json_file_path = os.path.join(output_json_dir, json_file)
        
        with open(json_file_path, "r") as file:
       
            data = json.load(file)
            keypoints = data["people"][0]["pose_keypoints_2d"]
            keypoints_hand = data["people"][0]["hand_left_keypoints_2d"]
            orientation = determine_orientation(keypoints[8], keypoints[11])
            process_json_file(data, json_file_path, keypoints, keypoints_hand, orientation)

if __name__ == "__main__":
    main()