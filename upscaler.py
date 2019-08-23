import argparse
import cv2
import math
import numpy as np
import sys

def lerp(f1, f2, t):
    return (1 - t) * f1 + t * f2

# Only interpolate on H (hue) and S (saturation) channels
def lerp_hls(f1, f2, t):
    h = lerp(f1[:, :, 0], f2[:, :, 0], t).reshape(f1.shape[0], f1.shape[1], 1)
    s = lerp(f1[:, :, 2], f2[:, :, 2], t).reshape(f1.shape[0], f1.shape[1], 1)
    l = f1[:, :, 1].reshape(f1.shape[0], f1.shape[1], 1)
    return np.concatenate((h, l, s), axis = 2)

parser = argparse.ArgumentParser()
parser.add_argument("inFile", type = str, help = "File path of the video you want to upscale")
parser.add_argument("outFile", type = str, help = "File path of the upscaled video")
parser.add_argument("k", type = int, help = "How much you are scaling the framerate by (must be integer)")

args = parser.parse_args()
in_file, out_file, k = args.inFile, args.outFile, args.k

cap = cv2.VideoCapture(in_file)

in_file_fps = cap.get(cv2.CAP_PROP_FPS)
in_file_frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

print("file fps:", in_file_fps)
print("file frame count:", in_file_frame_count)
print("file width:", width)
print("file height:", height)

if k < 1:
    raise Exception("k must be greater than 1")

fps = in_file_fps * k

out = cv2.VideoWriter(out_file, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))

t_vals = np.linspace(0, 1, k + 1)[1:]

# Setup progress bar
n_segments = (k * in_file_frame_count) // 100
sys.stdout.write("[%s]" % (" " * n_segments))
sys.stdout.flush()
sys.stdout.write("\b" * (n_segments + 1))

first_frame = True
i = 0
while True:
    ret, frame = cap.read()

    if ret:
        if first_frame:
            prev = frame
            first_frame = False
            out.write(frame)
            cv2.imshow("Frame:", frame)
            i += 1

        else:
            for t in t_vals:
                new_frame = np.uint8(lerp(prev, frame, t))
                out.write(new_frame)
                cv2.imshow("Frame", new_frame)
                i += 1

            if np.array_equal(frame, prev):
                raise Exception("frames are equal")

        if i % 100 == 99:
            sys.stdout.write("-")
            sys.stdout.flush()

        if cv2.waitKey(25) & 0xFF == ord("q"):
            break
         
    else:
        break

sys.stdout.write("]\n")

cv2.destroyAllWindows()
out.release()
