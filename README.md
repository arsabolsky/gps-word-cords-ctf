# gps-word-cords-ctf
**Title:** Extracting GPS Coordinates from Photos to Reveal the CTF Flag

**Description:**
In this Capture The Flag (CTF) challenge, the participants are given a 
folder containing multiple photos. Each photo has GPS coordinates embedded 
in its metadata. The objective of the challenge is to extract these 
coordinates, plot them on a map, and reveal the hidden CTF flag.

**General Solution Guide:**

1. **Analyze the photos:** Begin by inspecting the photos to understand 
the challenge. Analyze the metadata to determine if it contains GPS 
coordinates.

2. **Extract GPS coordinates:** Use a programming language like Python 
with a library such as `piexif` or `exifread` to extract the GPS 
coordinates from the metadata of each photo.

3. **Convert coordinates:** If necessary, convert the GPS coordinates from 
degrees, minutes, and seconds (DMS) to decimal format.

4. **Plot coordinates on a map:** Use a mapping tool or library like 
Google Maps API, OpenStreetMap, or Leaflet to plot the coordinates on a 
map. Connect the points in the order they appear in the folder to form a 
path.

5. **Analyze the plotted path:** Visually inspect the path created by the 
plotted coordinates. The path should form a recognizable shape, text, or 
pattern that reveals the CTF flag.

6. **Submit the flag:** Once the flag is identified, submit it to complete 
the challenge.

**Sample Python Code for Extracting GPS Coordinates:**

```python
import os
import piexif

def dms_to_decimal(dms, ref):
    decimal = dms[0][0] / dms[0][1] + dms[1][0] / (dms[1][1] * 60) + 
dms[2][0] / (dms[2][1] * 3600)
    if ref in ['S', 'W']:
        decimal = -decimal
    return decimal

def extract_gps_coordinates(img_path):
    try:
        exif_dict = piexif.load(img_path)
    except FileNotFoundError:
        print(f"File {img_path} not found.")
        return

    lat_dms = exif_dict["GPS"].get(piexif.GPSIFD.GPSLatitude)
    lat_ref = exif_dict["GPS"].get(piexif.GPSIFD.GPSLatitudeRef)
    lng_dms = exif_dict["GPS"].get(piexif.GPSIFD.GPSLongitude)
    lng_ref = exif_dict["GPS"].get(piexif.GPSIFD.GPSLongitudeRef)

    if lat_dms and lat_ref and lng_dms and lng_ref:
        lat = dms_to_decimal(lat_dms, lat_ref.decode())
        lng = dms_to_decimal(lng_dms, lng_ref.decode())
        return lat, lng
    else:
        return None

photo_directory = "photos"
allowed_extensions = {".jpg", ".jpeg", ".png"}
photo_files = sorted(
    [file for file in os.listdir(photo_directory) if 
os.path.splitext(file)[1].lower() in allowed_extensions]
)

coordinates = []
for photo in photo_files:
    photo_path = os.path.join(photo_directory, photo)
    coords = extract_gps_coordinates(photo_path)
    if coords:
        coordinates.append(coords)
        print(f"Extracted GPS coordinates for {photo}: {coords}")

