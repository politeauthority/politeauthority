ffmpeg -framerate 1 -pattern_type glob -i '/home/alix/photos/*.jpg' \
           -c:v libx264 -r 30 -pix_fmt yuv420p /home/alix/out.mp4
