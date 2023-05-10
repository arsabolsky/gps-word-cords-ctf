import csv
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def draw_text_image(text):
    font_size = 24
    font = ImageFont.truetype("arial.ttf", font_size)
    text_size = font.getsize(text)
    img = Image.new('1', text_size, color=255)
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), text, font=font, fill=0)
    return img


def extract_waypoints(img, start_lat, start_lon, scale):
    width, height = img.size
    img_array = np.array(img)
    waypoints = []
    for y in range(height):
        for x in range(width):
            if img_array[y, x] == 0:
                lat = start_lat + ((height - y) * scale)  # Reverse the y-axis
                lon = start_lon + (x * scale)
                waypoints.append((lat, lon))
    return waypoints


def write_to_csv(coordinates, filename):
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Latitude', 'Longitude'])
        for lat, lon in coordinates:
            csvwriter.writerow([lat, lon])

def main():
    text = "@CleverUSB"
    start_lat = 40.0000
    start_lon = -100.0000
    scale = 0.0001

    img = draw_text_image(text)

    img_array = np.array(img)
    waypoints = extract_waypoints(img, start_lat, start_lon, scale)
    write_to_csv(waypoints, 'text_coordinates.csv')
    print("CSV file created: text_coordinates.csv")

if __name__ == '__main__':
    main()
