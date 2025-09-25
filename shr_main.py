import os
import json
import subprocess
import cv2


import math
import keypoints_mapping as kp

from directory_utils import (clean_directory, distance, calc_angle, 
                            determine_orientation, calc_vertical_angle, 
                            calc_arm_analysis_score, #Step 1
                            calc_lower_arm_score,     #Step 2
                            is_arm_crossing_upper_midline,  #Step 2a_a
                            are_arms_out_to_side,       # Step 2a_b
                            get_sign,
                            is_shoulder_raised,         # Step 1a
                            calc_wrist_pos_score,    # Step 3
                            get_tableA,
                            get_tableB,
                            get_tableC,
                            calc_neck_score,
                            calc_neck_bending,
                            calc_trunk_score,
                            rula_recommends,
                            calc_horizontal_angle,
                            add_recommendation_to_image
                            )

# Define directories and command
openpose_demo_exe = ".\\build_2D\\x64\\Release\\OpenPoseDemo.exe"
#input_dir = ".\examples\shr_project\in_img"
#output_images_dir = ".\examples\shr_project\out_img"
#output_json_dir = ".\examples\shr_project\out_json"

input_dir = "./examples/shr_project/in_img"
output_images_dir = "./examples/shr_project/out_img"
output_json_dir = "./examples/shr_project/out_json"

# Clean the output directories
for directory in [output_images_dir, output_json_dir]:
    clean_directory(directory)

# Run OpenPoseDemo with the specified parameters
command = [
    openpose_demo_exe,
    "--image_dir", input_dir,
    "--write_images", output_images_dir,
    "--write_images_format", "jpg",
    "--model_pose", "COCO",
    "--hand",
    "--write_json", output_json_dir
]

# Executing the Script
subprocess.run(command, check=True)

# Determine the Orientation of the images from only side poses
for json_file in os.listdir(output_json_dir):
    if "side" in json_file:  # Consider only the files with "side" in the filename
        json_file_path = os.path.join(output_json_dir, json_file)
        
        # Load the JSON data
        with open(json_file_path, "r") as side_file:
            data = json.load(side_file)
        
        # Check if pose_keypoints_2d is in the data
        if "people" in data and len(data["people"]) > 0 and "pose_keypoints_2d" in data["people"][0]:
            skeypoints = data["people"][0]["pose_keypoints_2d"]
            # Create a mapping from COCO keypoint labels to their respective indices
            lbl_skeypoints = {label: skeypoints[kp.COCO_KEYPOINT_LABELS[label]*3: (kp.COCO_KEYPOINT_LABELS[label]*3)
                            + 3] for label in kp.COCO_KEYPOINT_LABELS}
            
            # Add orientation to the JSON data
            data["orientation"] = determine_orientation(lbl_skeypoints['RHip'], lbl_skeypoints['LHip'])
            
            # Write the updated JSON data
            with open(json_file_path, "w") as side_file:
                json.dump(data, side_file, indent=4)
# Process side JSON files
for side_json_file in filter(lambda name: "_side" in name, os.listdir(output_json_dir)):
    side_json_file_path = os.path.join(output_json_dir, side_json_file)
    #print("FILE NAME: ({})".format(side_json_file))

        # Form the filename for the corresponding "_front" file
    front_json_file = side_json_file.replace("_side", "_front")
    front_json_file_path = os.path.join(output_json_dir, front_json_file)

    # Load the front JSON data
    with open(front_json_file_path, "r") as front_file:
        front_data = json.load(front_file)
        fkeypoints = front_data["people"][0]["pose_keypoints_2d"]
        # Create a mapping from COCO keypoint labels to their respective indices
        lbl_fkeypoints = {label: fkeypoints[kp.COCO_KEYPOINT_LABELS[label]*3: (kp.COCO_KEYPOINT_LABELS[label]*3)
                        + 3] for label in kp.COCO_KEYPOINT_LABELS}
        
        right_arm_cross, left_arm_cross = is_arm_crossing_upper_midline(lbl_fkeypoints["Neck"],
                                                                    lbl_fkeypoints["Nose"],
                                                                    lbl_fkeypoints["RShoulder"],
                                                                    lbl_fkeypoints["LShoulder"],
                                                                    lbl_fkeypoints["RWrist"],
                                                                    lbl_fkeypoints["LWrist"])
        #Step 2a_a
        front_data["s2a_a_right_arm_cross"] = 1 if right_arm_cross else 0
        front_data["s2a_a_left_arm_cross"] = 1 if left_arm_cross else 0

        right_arm_out, left_arm_out = are_arms_out_to_side(lbl_fkeypoints["RShoulder"],
                                                            lbl_fkeypoints["LShoulder"],
                                                            lbl_fkeypoints["RWrist"],
                                                            lbl_fkeypoints["LWrist"])
        # Step 2a_b
        front_data["s2a_b_right_arm_out"] = 1 if right_arm_out else 0
        front_data["s2a_b_left_arm_out"] = 1 if left_arm_out else 0

        # Step 1a
        shoulder_is_raised = is_shoulder_raised(lbl_fkeypoints["RShoulder"], lbl_fkeypoints["LShoulder"], lbl_fkeypoints["Neck"])
        front_data["s1a_shoulder_raised"] = shoulder_is_raised
        
        # Check if either of s2a data is 1
        s2a_score = ( front_data["s2a_a_right_arm_cross"] or front_data["s2a_a_left_arm_cross"]
                      or front_data["s2a_b_right_arm_out"] or front_data["s2a_b_left_arm_out"] )
        
        
        # Distance Between Neck and Each Eye should be same for the Neck to not be bent
        # Better if The Eyes and Shoulder Lines are parallel if picture is taken exactly from front
        # Front picture should be from Center
        front_data["s9a_neckbend_score"] = calc_neck_bending(lbl_fkeypoints["REye"],lbl_fkeypoints["LEye"],
                                                             lbl_fkeypoints["Neck"])
        s9a_neckbend_score = front_data["s9a_neckbend_score"]
    

    # Write the updated JSON front_data
    with open(front_json_file_path, "w") as front_file:
        json.dump(front_data, front_file, indent=4)    

    # Load the JSON data
    with open(side_json_file_path, "r") as side_file:
        side_data = json.load(side_file)
    
    skeypoints = side_data["people"][0]["pose_keypoints_2d"]
        # Create a mapping from COCO keypoint labels to their respective indices
    lbl_skeypoints = {label: skeypoints[kp.COCO_KEYPOINT_LABELS[label]*3: (kp.COCO_KEYPOINT_LABELS[label]*3)
                        + 3] for label in kp.COCO_KEYPOINT_LABELS}
        
    # Only proceed if orientation is 'right'
    if "orientation" in side_data and side_data["orientation"] == "right":
        skeypoints_hand = side_data["people"][0]["hand_left_keypoints_2d"]
        # Create a mapping from COCO keypoint labels to their respective indices
        lbl_skeypoints_hand = {label: skeypoints_hand[kp.HAND_KEYPOINT_LABELS[label]*3: (kp.HAND_KEYPOINT_LABELS[label]*3)
                        + 3] for label in kp.HAND_KEYPOINT_LABELS}
        ear = lbl_skeypoints["LEar"]
        hip = lbl_skeypoints["LHip"]
        elbow = lbl_skeypoints["LElbow"]
        shoulder = lbl_skeypoints["LShoulder"]
        knee = lbl_skeypoints["LKnee"]
        wrist = lbl_skeypoints["LWrist"]
        angle_b_sign = get_sign(shoulder[0], elbow[0])
        angle_a_sign = get_sign(lbl_skeypoints["Neck"][0], ear[0])
        angle_e_sign = get_sign(elbow[1], wrist[1])
        angle_c_sign = get_sign(hip[0],shoulder[0] )

    elif "orientation" in side_data and side_data["orientation"] == "left":
        skeypoints_hand = side_data["people"][0]["hand_right_keypoints_2d"]
        # Create a mapping from COCO keypoint labels to their respective indices
        lbl_skeypoints_hand = {label: skeypoints_hand[kp.HAND_KEYPOINT_LABELS[label]*3: (kp.HAND_KEYPOINT_LABELS[label]*3)
                        + 3] for label in kp.HAND_KEYPOINT_LABELS}
        ear = lbl_skeypoints["REar"]
        hip = lbl_skeypoints["RHip"]
        elbow = lbl_skeypoints["RElbow"]
        shoulder = lbl_skeypoints["RShoulder"]
        knee = lbl_skeypoints["RKnee"]
        wrist = lbl_skeypoints["RWrist"]
        angle_b_sign = get_sign(elbow[0], shoulder[0])
        angle_a_sign = get_sign(ear[0], lbl_skeypoints["Neck"][0])
        angle_c_sign = get_sign(shoulder[0],hip[0] )
        angle_e_sign = get_sign(wrist[1],elbow[1])
    # Calculate the angles
    angles = {}
         
    angles["ANGLE_A"] = angle_a_sign*(180 - calc_angle(ear, lbl_skeypoints["Neck"], hip))
    angles["ANGLE_B"] = angle_b_sign * calc_vertical_angle(elbow, shoulder)
    # Trunk Position, vertical Angle between Hip Shoulder and vertical line down from shoulder
    angles["ANGLE_C"] = angle_c_sign * calc_vertical_angle(hip, shoulder) 
    #calc_angle(lbl_skeypoints["Neck"], hip,knee)
    angles["ANGLE_D"] = 180 - calc_angle(elbow, wrist, lbl_skeypoints_hand["Middle2"])
    # Positive sign ANGLE E if wrist is lower than elbow, Negative otherwise
    angles["ANGLE_E"] = angle_e_sign * calc_horizontal_angle(elbow,wrist)    # OLD CALC calc_angle(shoulder,elbow, wrist)
    side_data.update(angles)
    #print("Y-wrist:ear({:.2f},{:.2f})".format( elbow[1],wrist[1]))
    #print("A:B:C:D:E({:.2f},{:.2f},{:.2f},{:.2f},{:.2f})".format( angles["ANGLE_A"]
    #                                                             ,angles["ANGLE_B"]
    #                                                             ,angles["ANGLE_C"]
    #                                                             ,angles["ANGLE_D"]
    #                                                             ,angles["ANGLE_E"]))

    
    side_data["s1_upper_arm_score"] = calc_arm_analysis_score(angles["ANGLE_B"]) + shoulder_is_raised
    side_data["s2_lower_arm_score"] = calc_lower_arm_score(angles["ANGLE_E"]) + s2a_score
    side_data["s3_wrist_pos_score"] = calc_wrist_pos_score(angles["ANGLE_D"])
    side_data["s4_wrist_tws_score"] = 1
    side_data["s5_LUTA_post_score"] = get_tableA(side_data["s1_upper_arm_score"], side_data["s2_lower_arm_score"], 
                                       side_data["s3_wrist_pos_score"])
    side_data["s6_muscleuse_score"] = 1
    side_data["s7_forceload_score"] = 0
    side_data["s8_wrist_arm_score"]  = (side_data["s7_forceload_score"] + side_data["s6_muscleuse_score"] 
                                 + side_data["s5_LUTA_post_score"] )

    side_data["s9_neck_score"]      = calc_neck_score(angles["ANGLE_A"]) + s9a_neckbend_score
    
    side_data["s10_trunk_score"]      = calc_trunk_score(angles["ANGLE_C"])
    
    # s10a (SKIPPED): Trunk is twisted OR Trunk is bending +1 
    
    side_data["s11_legs_score"]      = 1 # SKIPPED
    side_data["s12_tbleB_score"]     = get_tableB(side_data["s9_neck_score"] , side_data["s10_trunk_score"])
    side_data["s13_muscle_use_score"] = 1
    side_data["s14_force_load_score"] = 0
    side_data["s15_neck_trunck_leg_score"] = side_data["s12_tbleB_score"] + side_data["s13_muscle_use_score"]

    side_data["RULA_SCORE"] = get_tableC(side_data["s8_wrist_arm_score"],side_data["s15_neck_trunck_leg_score"])

    side_data["Recommendation"] = rula_recommends(side_data["RULA_SCORE"])
    #print("FILE NAME: ({}) Recommendation: {}".format(side_json_file, side_data["Recommendation"]))
       
    # Write the updated JSON side_data
    with open(side_json_file_path, "w") as side_file:
        json.dump(side_data, side_file, indent=4)

    recommendation = side_data.get("Recommendation", "No recommendation")
    # Extract filename without extension from the JSON file path
    json_file_name_without_ext = os.path.splitext(os.path.basename(side_json_file_path))[0]

    # Replace 'keypoints' with 'rendered' to get the corresponding image file name
    image_file_name = json_file_name_without_ext.replace('keypoints', 'rendered') + '.jpg'

    # Construct the full image path
    side_image_path = os.path.join(output_images_dir, image_file_name)

    # Define the output path for the image with the recommendation text
    output_image_with_text_path = side_image_path  # If you want to overwrite the original image

    # Call the function with display_image set to True if you want to see the image
    result = add_recommendation_to_image(side_image_path, recommendation, output_image_with_text_path, display_image=True)

    #if not result:
    #    print("There was an error adding the recommendation to the image.")