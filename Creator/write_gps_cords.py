import os
import pandas as pd
import piexif

def decimal_to_dms(decimal):
    degrees = int(decimal)
    sub_minutes = abs((decimal - degrees) * 60)
    minutes = int(sub_minutes)
    sub_seconds = abs((sub_minutes - minutes) * 60)
    seconds = round(sub_seconds * 1000)
    return degrees, minutes, seconds

def dms_to_rational(dms):
    return [(int(value[0]), value[1]) for value in zip(dms, (1, 1, 1000))]

def set_gps_coordinates(img_path, lat, lng):
    try:
        exif_dict = piexif.load(img_path)
    except FileNotFoundError:
        print(f"File {img_path} not found.")
        return

    lat_dms = decimal_to_dms(abs(lat))
    lng_dms = decimal_to_dms(abs(lng))

    gps_ifd = {
        piexif.GPSIFD.GPSLatitudeRef: "N" if lat >= 0 else "S",
        piexif.GPSIFD.GPSLatitude: dms_to_rational(lat_dms),
        piexif.GPSIFD.GPSLongitudeRef: "E" if lng >= 0 else "W",
        piexif.GPSIFD.GPSLongitude: dms_to_rational(lng_dms),
    }

    exif_dict["GPS"] = gps_ifd
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, img_path)

def main():
    csv_path = "text_coordinates.csv"
    photo_directory = "Images"
    allowed_extensions = {".jpg", ".jpeg"}

    if not os.path.exists(csv_path):
        print(f"CSV file '{csv_path}' not found.")
        return

    if not os.path.exists(photo_directory):
        print(f"Directory '{photo_directory}' not found.")
        return

    df = pd.read_csv(csv_path)

    photo_files = sorted(
        [file for file in os.listdir(photo_directory) if os.path.splitext(file)[1].lower() in allowed_extensions]
    )

    num_rows = len(df)
    num_photos = len(photo_files)

    if num_rows > num_photos:
        print(f"Warning: The number of rows in the CSV ({num_rows}) is greater than the number of photos in the directory ({num_photos}). Only the first {num_photos} rows will be processed.")
        num_rows = num_photos

    for index in range(num_rows):
        photo_path = os.path.join(photo_directory, photo_files[index])
        set_gps_coordinates(photo_path, df.at[index, "Latitude"], df.at[index, "Longitude"])
        print(f"Updated GPS coordinates for {photo_files[index]}")

if __name__ == "__main__":
    main()
