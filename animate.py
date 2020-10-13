"""
PoseNet Movement Visualizer
by Brian Yu

October 2020
"""

import csv
import cv2
import os
import sys
import numpy

from PIL import Image, ImageColor, ImageDraw, ImageFont

# Set video parameters
WIDTH = 600
HEIGHT = 600
FPS = 15

# Frame on which to start generating animation
START_FRAME = 60

# Set size and font for dots and labels
DOT_RADIUS = 5
FONT = ImageFont.truetype(f"OpenSans-Regular.ttf", 12)

# Define colors
BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 255)
GRAY = (214, 214, 214, 255)
RED = (255, 0, 0, 255)
GREEN = (0, 255, 0, 255)
BLUE = (0, 0, 255, 255)
ORANGE = (212, 175, 66, 255)
YELLOW = (255, 255, 0, 255)
TEAL = (33, 207, 201, 255)
PURPLE = (207, 33, 204, 255)

# Toggles whether text labels should appear alongside dots
SHOULD_LABEL = True

# Toggles which fields to include in the animation
FIELDS = [
    (True, "nose", GRAY),

    (False, "leftEye", BLUE),
    (False, "rightEye", BLUE),

    (False, "leftEar", WHITE),
    (False, "rightEar", WHITE),

    (True, "leftShoulder", YELLOW),
    (True, "rightShoulder", YELLOW),

    (True, "leftElbow", BLUE),
    (True, "rightElbow", BLUE),

    (True, "leftWrist", RED),
    (True, "rightWrist", RED),

    (True, "leftHip", GREEN),
    (True, "rightHip", GREEN),

    (True, "leftKnee", ORANGE),
    (True, "rightKnee", ORANGE),

    (True, "leftAnkle", TEAL),
    (True, "rightAnkle", TEAL),

]


def main():

    # Check usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python animation.py posenet.csv")

    # Initialize video file
    fourcc = cv2.VideoWriter_fourcc(*"FMP4")
    video = cv2.VideoWriter("animation.mp4", fourcc, FPS, (WIDTH, HEIGHT))

    # Loop over PoseNet data one row at a time
    for row in csv.DictReader(open(sys.argv[1])):

        # Ensure frame is past starting value
        frame = int(row["frame"])
        if frame < START_FRAME:
            continue

        # Generate a blank image for each frame
        img = Image.new("RGBA", (WIDTH, HEIGHT), color=BLACK)
        draw = ImageDraw.Draw(img)

        # Consider all possible data values for the frame
        for include, field, color in FIELDS:

            # Don't plot fields that are marked as skipped
            if not include:
                continue

            # Extract coordinate position of body part
            x = row[f"{field}_x"]
            y = row[f"{field}_y"]

            # Plot body part if both x and y values are present
            if x and y:
                x = float(x)
                y = float(y)
                draw.ellipse(
                    [(x - DOT_RADIUS, y - DOT_RADIUS),
                     (x + DOT_RADIUS, y + DOT_RADIUS)],
                    fill=color
                )

                # If labeling enabled, draw label next to dot
                if SHOULD_LABEL:
                    draw.text(
                        [x + DOT_RADIUS, y + DOT_RADIUS],
                        field,
                        fill=WHITE,
                        font=FONT
                    )

        # Write frame to video
        print(f"Writing frame {frame} to video...")
        video.write(cv2.cvtColor(numpy.array(img), cv2.COLOR_RGB2BGR))

        # Uncomment to save images as individual frames in addition to video
        # img.save(os.path.join("frames", f"{str(frame).zfill(5)}.png"))

    # Release video
    video.release()


if __name__ == "__main__":
    main()
