# fpsUpscale
Upscale the frames-per-second of a video by a constant scale factor using linear interpolation (cubic/spline interpolation should come soon).

## Usage
```
upscaler.py inFile outFile k method
```
where `k` is the scale factor by which the video fps is scaled by. `method` must either be "cubic" or "linear".
