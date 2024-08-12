import os
import subprocess


def build_ffmpeg_command(input_folder: str, total_length: int, transitions) -> str:
    """
    Constructs an FFmpeg command to create a video from images in a folder,
    applying transitions between them.

    Args:
        input_folder: Path to the folder containing images.
        total_length: Desired total length of the output video in seconds.
        transitions: List of transition effects to use between images.

    Returns:
        The constructed FFmpeg command as a string.
    """

    image_files = [
        f
        for f in os.listdir(input_folder)
        if f.endswith((".jpg", ".jpeg", ".png"))
    ]

    num_images = len(image_files)
    if num_images < 2:
        return "Error: There must be at least 2 images in the input folder."

    # Adjust total length to account for transition durations
    total_length -= total_length * (20 / 100)
    len_of_each_image = total_length / num_images

    # Build the input part of the command
    input_part = ""
    for image_file in image_files:
        input_part += (
            f" -loop 1 -t {len_of_each_image} -i {os.path.join(input_folder, image_file)}"
        )

    # Build the filter complex part for transitions
    filter_complex_part = ""
    for i in range(num_images - 1):
        filter_complex_part += f"[{i}][{i+1}]xfade=transition={transitions[i % len(transitions)]}:duration={len_of_each_image / 2}:offset={len_of_each_image / 2}[tr{i+1}],"
    filter_complex_part = filter_complex_part.rstrip(", ")

    # Build the concat part to join transitioned segments
    concat_part = "; " + "".join([f"[tr{i}]" for i in range(1, num_images)]) + f"concat=n={num_images-1}[outv]"

    # Construct the final FFmpeg command
    command = f"ffmpeg -y {input_part} -filter_complex \"{filter_complex_part}{concat_part}\" -map \"[outv]\" outputs/output.mp4"
    print(command)  # Print the command for debugging/reference
    return command


def main():
    """
    Main function to execute the video creation process.
    """
    inputs = "inputs"
    total_length_of_video = 20
    list_of_transitions = ["slideup", "slideleft", "slidedown", "slideright", "fade", "radial", "fadewhite"]  # costumisable
    command = build_ffmpeg_command(inputs, total_length_of_video, list_of_transitions)
    subprocess.run(command, shell=True)


if __name__ == "__main__":
    main()
