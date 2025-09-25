import os
import subprocess
import json
import cv2

# Define the paths for the input images, output images, and JSON output
input_dir = r'in_img1'  # Use raw string for Windows paths
output_img_dir = r'out_img1'
output_json_dir = r'out_json1'

# Function to put the text on the image
def put_text_on_image(image, text, position):
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1.5
    font_color = (255, 255, 255)
    line_type = 4

    # Ensure the position is a tuple of integers
    position = (int(position[0]), int(position[1]))

    cv2.putText(image, text, position, font, font_scale, font_color, line_type)

# Define the command to run OpenPoseDemo.exe
openpose_bin = r'.\build\x64\Release\OpenPoseDemo.exe'
command = [
    openpose_bin,
    '--image_dir', input_dir,
    '--write_images', output_img_dir,
    '--write_images_format', 'jpg',
    '--model_pose', 'COCO',
    '--hand',
    '--write_json', output_json_dir
]

# Run the OpenPoseDemo.exe command
subprocess.run(command)

# Overlay the keypoints onto the images
for json_file in os.listdir(output_json_dir):
    if json_file.endswith(".json"):
        json_path = os.path.join(output_json_dir, json_file)

        # Load JSON data
        with open(json_path, 'r') as f:
            json_data = json.load(f)

        if json_data['people']:
            keypoints = json_data['people'][0]['pose_keypoints_2d']
            # Adjust the base name to match the rendered images
            image_base_name = json_file.split("_keypoints")[0]
            image_name = image_base_name + "_rendered.jpg"
            image_path = os.path.join(output_img_dir, image_name)

            # Read the image
            image = cv2.imread(image_path)

            if image is not None:
                # Loop through every keypoint
                for i in range(0, len(keypoints), 3):
                    x, y, confidence = keypoints[i], keypoints[i + 1], keypoints[i + 2]
                    # Ensure x and y are integers
                    x = int(x)
                    y = int(y)

                    if confidence > 0.2:
                        # Overlay the index number (i//3 because each keypoint has 3 values: x, y, confidence)
                        put_text_on_image(image, str(i // 3), (x, y))
                output_image_path = os.path.join(output_img_dir, image_name)
                cv2.imwrite(output_image_path, image)
            else:
                print(f"Could not load image: {image_path}")
        else:
            print(f"No people detected in JSON: {json_path}")