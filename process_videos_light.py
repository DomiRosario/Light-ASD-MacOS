import os
import random
import subprocess
import shutil

base_dir = os.path.dirname(os.path.abspath(__file__))

data_dir = os.path.abspath(os.path.join(base_dir, "../../Data/Videos"))
script_path = os.path.join(base_dir, "Columbia_test.py")

print(f"Base directory: {base_dir}")
print(f"Data directory: {data_dir}")
print(f"Script path: {script_path}")

video_files = []
for subdir in os.listdir(data_dir):
    if subdir == "s21":
        continue
    subdir_path = os.path.join(data_dir, subdir)
    if os.path.isdir(subdir_path):
        for root, dirs, files in os.walk(subdir_path):
            for file in files:
                if file.endswith(".mpg"):
                    video_files.append(os.path.join(root, file))

print(f"Total video files found: {len(video_files)}")

num_videos_to_process = 1000
if len(video_files) < num_videos_to_process:
    raise ValueError(
        "Not enough video files to process the requested number of videos."
    )

# Seed for reproducibility
random.seed(42)
videos_to_process = random.sample(video_files, num_videos_to_process)

processed_count = 0
total_videos = len(videos_to_process)

# Process each video
for video in videos_to_process:
    video_name = os.path.splitext(os.path.basename(video))[0]
    command = [
        "python",
        script_path,
        "--videoName",
        video_name,
        "--videoFolder",
        os.path.dirname(video),
    ]
    print(f"Running command: {' '.join(command)}")
    subprocess.run(command)

    # Move the scores.pckl file to the desired directory and rename it
    source_dir = os.path.join(os.path.dirname(video), video_name, "pywork")
    destination_dir = "/Users/domi/Bachelor-Thesis/results/light-asd"
    if os.path.exists(source_dir):
        scores_file = os.path.join(source_dir, "scores.pckl")
        if os.path.exists(scores_file):
            destination_file = os.path.join(
                destination_dir, f"{video_name}-scores.pckl"
            )
            shutil.move(scores_file, destination_file)
            print(f"Moved and renamed {scores_file} to {destination_file}")

        # Delete the folder containing the pywork directory
        folder_to_delete = os.path.join(os.path.dirname(video), video_name)
        shutil.rmtree(folder_to_delete)
        print(f"Deleted folder {folder_to_delete}")

    processed_count += 1
    remaining_videos = total_videos - processed_count
    print(f"Processed {processed_count} videos. {remaining_videos} videos remaining.")

print(f"Processed {processed_count} videos in total.")
