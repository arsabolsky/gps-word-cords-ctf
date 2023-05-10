import os
import csv
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def extract_gps_info(img):
    exif_data = img._getexif()
    gps_info = {}
    if exif_data:
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            if tag_name == 'GPSInfo':
                for gps_tag in value:
                    sub_tag = GPSTAGS.get(gps_tag, gps_tag)
                    gps_info[sub_tag] = value[gps_tag]

    if 'GPSLatitude' in gps_info and 'GPSLongitude' in gps_info:
        return gps_info
    else:
        return None

def get_decimal_coordinates(info):
    lat_data = info['GPSLatitude']
    lat = float(lat_data[0]) + (float(lat_data[1]) / 60) + (float(lat_data[2]) / 3600)
    if info['GPSLatitudeRef'] == 'S':
        lat = -lat

    lon_data = info['GPSLongitude']
    lon = float(lon_data[0]) + (float(lon_data[1]) / 60) + (float(lon_data[2]) / 3600)
    if info['GPSLongitudeRef'] == 'W':
        lon = -lon

    return lat, lon

def main():
    folder_path = "Images"
    csv_path = "gps_coordinates.csv"
    
    with open(csv_path, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Latitude", "Longitude"])
        
        for filename in os.listdir(folder_path):
            if filename.endswith(".jpeg") or filename.endswith(".jpg"):
                image_path = os.path.join(folder_path, filename)
                with Image.open(image_path) as img:
                    gps_info = extract_gps_info(img)
                    if gps_info:
                        lat, lon = get_decimal_coordinates(gps_info)
                        writer.writerow([lat, lon])

if __name__ == '__main__':
    main()
