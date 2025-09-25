import subprocess
import os
import sys

def run_openpose(image_dir, output_image_dir, output_json_dir):
    # Define the path to the OpenPoseDemo executable
    openpose_demo_exe = r"C:\Users\sairu\Samir\openpose\build\x64\Release\OpenPoseDemo.exe"
    
    # Make sure the output directories exist
    os.makedirs(output_image_dir, exist_ok=True)
    os.makedirs(output_json_dir, exist_ok=True)

    # Define the command and arguments
    command = [
        openpose_demo_exe,
        '--image_dir', image_dir,
        '--write_images', output_image_dir,
        '--write_images_format', 'jpg',
        '--hand',
        '--face',
        '--model_pose', 'BODY_25',
        '--write_json', output_json_dir
    ]

    # Run the command
    subprocess.run(command)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python run_openpose.py <input_image_dir> <output_image_dir> <output_json_dir>")
        sys.exit(1)
    
    in_img_dir = sys.argv[1]
    out_img_dir = sys.argv[2]
    out_json_dir = sys.argv[3]

    run_openpose(in_img_dir, out_img_dir, out_json_dir)