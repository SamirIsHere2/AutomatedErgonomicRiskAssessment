# File: directory_utils.py

import os
import math
import cv2

# Mapping for Upper, Lower Arms and Wrist Score
# This is Table A for Rula Calculation of Wrist and Arm Score
def get_tableA(Y, X, N):
    # Create a mapping of inputs to outputs
    ulw_tbla_map = {
        (1, 1, 1): 1,
        (1, 1, 2): 2,
        (1, 1, 3): 2,
        (1, 1, 4): 3,
        (1, 2, 1): 2,
        (1, 2, 2): 2,
        (1, 2, 3): 3,
        (1, 2, 4): 3,
        (1, 3, 1): 2,
        (1, 3, 2): 3,
        (1, 3, 3): 3,
        (1, 3, 4): 4,
        (2, 1, 1): 2,
        (2, 1, 2): 3,
        (2, 1, 3): 3,
        (2, 1, 4): 4,
        (2, 2, 1): 3,
        (2, 2, 2): 3,
        (2, 2, 3): 3,
        (2, 2, 4): 4,
        (2, 3, 1): 3,
        (2, 3, 2): 4,
        (2, 3, 3): 4,
        (2, 3, 4): 5,
        (3, 1, 1): 3,
        (3, 1, 2): 4,
        (3, 1, 3): 4,
        (3, 1, 4): 5,
        (3, 2, 1): 3,
        (3, 2, 2): 4,
        (3, 2, 3): 4,
        (3, 2, 4): 5,
        (3, 3, 1): 4,
        (3, 3, 2): 4,
        (3, 3, 3): 4,
        (3, 3, 4): 5,
        (4, 1, 1): 4,
        (4, 1, 2): 4,
        (4, 1, 3): 4,
        (4, 1, 4): 5,
        (4, 2, 1): 4,
        (4, 2, 2): 4,
        (4, 2, 3): 4,
        (4, 2, 4): 5,
        (4, 3, 1): 4,
        (4, 3, 2): 4,
        (4, 3, 3): 5,
        (4, 3, 4): 6,
        (5, 1, 1): 5,
        (5, 1, 2): 5,
        (5, 1, 3): 5,
        (5, 1, 4): 6,
        (5, 2, 1): 5,
        (5, 2, 2): 6,
        (5, 2, 3): 6,
        (5, 2, 4): 7,
        (5, 3, 1): 6,
        (5, 3, 2): 6,
        (5, 3, 3): 7,
        (5, 3, 4): 7,
        (6, 1, 1): 7,
        (6, 1, 2): 7,
        (6, 1, 3): 7,
        (6, 1, 4): 8,
        (6, 2, 1): 8,
        (6, 2, 2): 8,
        (6, 2, 3): 8,
        (6, 2, 4): 9,
        (6, 3, 1): 9,
        (6, 3, 2): 9,
        (6, 3, 3): 9,
        (6, 3, 4): 9
    }
    # Return the value for the given Y, X, N combination
    return ulw_tbla_map.get((Y, X, N), "No value found")

#
# Define the mapping using a dictionary
# Mapping for Upper, Lower Arms and Wrist Score
# This is Table A for Rula Calculation of Wrist and Arm Score
def get_tableC(H,S):
    # Create a mapping of inputs to outputs
    # Cap the values of H and S
    H = min(H, 8)
    S = min(S, 7)

    hs_map = {
        (1, 1): 1,
        (1, 2): 2,
        (1, 3): 3,
        (1, 4): 3,
        (1, 5): 4,
        (1, 6): 5,
        (1, 7): 5,
        (2, 1): 2,
        (2, 2): 2,
        (2, 3): 3,
        (2, 4): 4,
        (2, 5): 4,
        (2, 6): 5,
        (2, 7): 5,
        (3, 1): 3,
        (3, 2): 3,
        (3, 3): 3,
        (3, 4): 4,
        (3, 5): 4,
        (3, 6): 5,
        (3, 7): 6,
        (4, 1): 3,
        (4, 2): 3,
        (4, 3): 3,
        (4, 4): 4,
        (4, 5): 5,
        (4, 6): 6,
        (4, 7): 6,
        (5, 1): 4,
        (5, 2): 4,
        (5, 3): 4,
        (5, 4): 5,
        (5, 5): 6,
        (5, 6): 7,
        (5, 7): 7,
        (6, 1): 4,
        (6, 2): 4,
        (6, 3): 5,
        (6, 4): 6,
        (6, 5): 6,
        (6, 6): 7,
        (6, 7): 7,
        (7, 1): 5,
        (7, 2): 5,
        (7, 3): 6,
        (7, 4): 6,
        (7, 5): 7,
        (7, 6): 7,
        (7, 7): 7,
        (8, 1): 5,
        (8, 2): 5,
        (8, 3): 6,
        (8, 4): 7,
        (8, 5): 7,
        (8, 6): 7,
        (8, 7): 7
    }
    # Return the value for the given H, and S combination
    return hs_map.get((H,S), "No value found")
    
    # Define the mapping using a dictionary
def get_tableB(E,Q):
    # Create a mapping of inputs to outputs
    eq_map = {
    (1, 1): 1,
    (1, 2): 2,
    (1, 3): 3,
    (1, 4): 5,
    (1, 5): 6,
    (1, 6): 7,
    (2, 1): 2,
    (2, 2): 2,
    (2, 3): 4,
    (2, 4): 5,
    (2, 5): 6,
    (2, 6): 7,
    (3, 1): 3,
    (3, 2): 3,
    (3, 3): 4,
    (3, 4): 5,
    (3, 5): 6,
    (3, 6): 7,
    (4, 1): 5,
    (4, 2): 5,
    (4, 3): 6,
    (4, 4): 7,
    (4, 5): 7,
    (4, 6): 8,
    (5, 1): 7,
    (5, 2): 7,
    (5, 3): 7,
    (5, 4): 8,
    (5, 5): 8,
    (5, 6): 8,
    (6, 1): 8,
    (6, 2): 8,
    (6, 3): 8,
    (6, 4): 8,
    (6, 5): 9,
    (6, 6): 9
    }
    # Return the value for the given E, and Q combination
    return eq_map.get((E,Q), "No value found")
# Example usage
#result = get_value(1, 1, 1)
#print(result)  # Output: Value1

def clean_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            # elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

# Function to calculate the distance between two points
def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

# Function to calculate angle between three points
def calc_angle(point1, point2, point3):
    a = distance(point2, point3)
    b = distance(point1, point2)
    c = distance(point1, point3)
    # Law of cosines
    angle = math.acos((b**2 + a**2 - c**2) / (2 * b * a))
    # Convert to degrees
    return math.degrees(angle)

# Function to calculate the vertical angle for ANGLE_B
def calc_vertical_angle(point1, point2):
    vertical_point = (point2[0], point1[1])  # Same X as point2, same Y as point1 (directly below)
    return calc_angle(point1, point2, vertical_point)

def calc_horizontal_angle(point1, point2):
    horizontal_point = (point1[0], point2[1])  # Same X as point2, same Y as point1 (directly below)
    return calc_angle(point1, point2, horizontal_point)

# Function to determine the orientation based on keypoints 8 and 11
def determine_orientation(keypoint_8, keypoint_11):
    if keypoint_11[1] > keypoint_8[1]:  # Compare Y values
        return "right"
    else:
        return "left"  # Assume left if they are at the same level or keypoint 8 is lower

# calculate arm and wrist analysis upper arm position score, A Step 1
def calc_arm_analysis_score(angle_B):
    score = 0
    
    if angle_B >= -20 and angle_B <= 20:
        score = 1
    elif angle_B < -20: 
        score = 2
    elif angle_B > 20 and angle_B <= 45:
        score = 2
    elif angle_B > 45 and angle_B <= 90:
        score = 3
    elif angle_B > 90:
        score = 4

    return score

# Step 2: Locate Lower Arm Position
def calc_lower_arm_score(angle_E):
    if -10 <= angle_E <= 30:
        score = 1
    else:
        score = 2
    '''
    if (180 - angle_E) >= 60 and (180 - angle_E) <= 100:
        score = 1
    elif (180 - angle_E) >= 0 and (180 - angle_E) < 60:
        score = 2
    elif (180 - angle_E) < 0:
        score = 3
    '''   
    return score

# Step 3: calc_wrist_pos_score
import math

def calc_wrist_pos_score(angle_D):
  if abs(angle_D) < 1:
    return 1
  
  elif abs(angle_D) < 15:
    return 2
    
  else:
    return 3


# It's important to remember that this method provides a best guess based on the 
# available keypoints and the assumption that the person is facing the camera 
# with a posture that allows for a clear definition of the midline. 
# If the person is turned significantly to the side, the midline estimation would 
# not be accurate, and consequently, the determination of whether the arms are 
# crossing the midline would also be unreliable.

def is_arm_crossing_upper_midline(neck,nose,rshoulder,lshoulder,rwrist,lwrist):
    # Estimate the midline X-coordinate using the neck and nose (more vertical if the head is not rotated too much)
    midline_x = (neck[0] + nose[0]) / 2
    #print("neck:nose:midline: ({:.2f}, {:.2f},{:.2f})".format(neck[0],nose[0],midline_x))

    # Check if the X-coordinate of the wrist is on the opposite side of the shoulder relative to the estimated midline
    right_arm_cross = rwrist[0] < midline_x < rshoulder[0] or rshoulder[0] < midline_x < rwrist[0]
    #print("right_arm_cross:rwrist:rshoulder:midline: ({:.2f},{:.2f}, {:.2f},{:.2f})".format(right_arm_cross,rwrist[0],rshoulder[0],midline_x))
    left_arm_cross = lwrist[0] > midline_x > lshoulder[0] or lshoulder[0] > midline_x > lwrist[0]

    return right_arm_cross, left_arm_cross


def are_arms_out_to_side(rshoulder,lshoulder,rwrist,lwrist, threshold=125):
    # Check if the wrists are outside the vertical line through the shoulders
    right_arm_out = rwrist[0]+threshold < rshoulder[0]
    left_arm_out = lwrist[0]-threshold > lshoulder[0]
    #print("right_arm_out:rwrist:rshoulder: ({:.2f},{:.2f}, {:.2f})".format(right_arm_out,rwrist[0],rshoulder[0]))
    #print("left_arm_out:lwrist:lshoulder: ({:.2f},{:.2f}, {:.2f})".format(left_arm_out,lwrist[0],lshoulder[0]))
    
    return right_arm_out, left_arm_out

tolerance = 1e-5 
def get_sign(keypoint1, keypoint2):
    if math.isclose(keypoint1, keypoint2, abs_tol=tolerance):
        # x values are nearly equal, return 0
        return 0
    elif keypoint1 > keypoint2:  
        return 1
    else:   
        return -1

def is_shoulder_raised(rshoulder,lshoulder, neck, threshold=75):
    #print("diff1:diff2: ({:.2f}, {:.2f})".format((rshoulder[1] - neck[1]),(lshoulder[1] - neck[1])))

    rshoulder_high = neck[1] - rshoulder[1]
    lshoulder_high = neck[1] - lshoulder[1]
    absdiff = abs(rshoulder_high+lshoulder_high)
    #print("rshoulder[1]:lshoulder[1]:neck[1]: ({:.2f},{:.2f}, {:.2f})".format(rshoulder[1],lshoulder[1],neck[1]))
    #print("rshoulder_high:lshoulder_high:absdiff: ({:.2f},{:.2f},{:.2f})".format(rshoulder_high,lshoulder_high,absdiff))
    
    if (absdiff < 2):
        return 0
    elif (absdiff > threshold):
        return 1
    else:
        return 0
    
def calc_neck_score(angle_A):
    if angle_A < -10:
        return 4
    elif angle_A <= 10:
        return 1
    elif 10 < angle_A <= 20:
        return 2
    elif angle_A > 20:
        return 3
    
def calc_trunk_score(angle_C):
    if angle_C < 1:
        return 1
    elif angle_C <= 20:
        return 2
    elif 20 < angle_C <= 60:
        return 3
    elif angle_C > 60:
        return 4
                            

def calc_neck_bending(reye,leye,neck):
    reye2neck = distance(reye, neck)
    leye2neck = distance(leye, neck)
    #print("reye2neck:leye2neck: ({:.2f},{:.2f})".format(reye2neck,leye2neck))
    
    if (abs(reye2neck-leye2neck)>50):
        #print("BENT")
        return 1
    else:
        #print("NOT BENT")
        return 0

def rula_recommends(rula_score):
    if rula_score == 7:
        return "Investigate and Implement Change"
    elif 5 <= rula_score <= 6:
        return "Further Investigation, Change Soon"
    elif 3 <= rula_score <= 4:
        return "Further Investigation, Change May be Needed"
    elif 1 <= rula_score <= 2:
        return "Acceptable Posture"
    else:
        return "COULD NOT RECOMMEND"

import cv2

def add_recommendation_to_image(image_path, recommendation, output_path, display_image=False):
    # Read the image using OpenCV
    image = cv2.imread(image_path)

    if image is None:
        print(f"Error: Image at {image_path} not found.")
        return False

    # Set the font, scale, and thickness of the text to be added
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 3.0  # Default font scale
    font_thickness = 6  # Default font thickness

    # Choose a color for the text, here it's white for better contrast
    text_color = (0, 0, 0)

    # Get the text size, needed for positioning the text
    (text_width, text_height), _ = cv2.getTextSize(recommendation, font, font_scale, font_thickness)

    # Calculate the position for the text (top-left of the image)
    text_position = (10, text_height + 10)  # 10 pixels from the top

    # Put the text on the image
    cv2.putText(image, recommendation, text_position, font, font_scale, text_color, font_thickness)

    # If display_image is True, display the image
        # If display_image is True, display the image
    if display_image:
        # Calculate new dimensions for the window
        new_width = image.shape[1] // 3
        new_height = image.shape[0] // 3

        # Create a named window that can be resized
        cv2.namedWindow('Image with Recommendation', cv2.WINDOW_NORMAL)

        # Resize the window to one-third of the original size
        cv2.resizeWindow('Image with Recommendation', new_width, new_height)

        # Display the image
        cv2.imshow('Image with Recommendation', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # Save the image with recommendation to the output path
    cv2.imwrite(output_path, image)