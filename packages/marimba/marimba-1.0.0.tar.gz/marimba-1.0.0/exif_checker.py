#!/usr/bin/env python3
"""
EXIF Header Corruption Checker (No ExifTool Required)

This script recursively checks JPG files for the specific EXIF header corruption issues
found in FlowCam images, as shown by exiftool validation:
- Tag values overlapping IFD
- Missing required EXIF/JPEG tags
- Odd offsets for tags
"""

import os
import argparse
import re
import struct
from pathlib import Path
import io

# We'll need to install these libraries if not already available
try:
    from PIL import Image, ExifTags
    import exifread
except ImportError:
    print("Required libraries not found. Please install them using:")
    print("pip install Pillow exifread")
    exit(1)


def check_image_exif_corruption(image_path):
    """
    Check for the specific EXIF corruption issues found in the exiftool output.

    Returns a tuple of (is_corrupted, error_details)
    """
    is_corrupted = False
    error_details = []
    corruption_markers = []

    # Open the file as bytes to check for JPEG/EXIF structure issues
    try:
        with open(image_path, 'rb') as f:
            # Check JPEG header
            header = f.read(2)
            if header != b'\xff\xd8':
                error_details.append("Not a valid JPEG file")
                return True, "\n".join(error_details)

            # Search for EXIF header marker
            f.seek(0)
            data = f.read(256)  # Read enough bytes for EXIF header

            # Look for APP1 marker (0xFFE1) which contains EXIF data
            app1_pos = data.find(b'\xff\xe1')
            if app1_pos >= 0:
                # Check if Exif identifier is present
                exif_pos = data.find(b'Exif\x00\x00', app1_pos)
                if exif_pos > 0:
                    # Calculate if there's a potential alignment issue
                    if (exif_pos - app1_pos) % 2 != 0:
                        corruption_markers.append("EXIF header alignment issue detected")
                        is_corrupted = True
                else:
                    # APP1 marker without Exif identifier might be corrupted
                    corruption_markers.append("APP1 marker without proper EXIF identifier")
                    is_corrupted = True
            else:
                # No APP1 marker found
                corruption_markers.append("No APP1/EXIF marker found")
                is_corrupted = True
    except Exception as e:
        error_details.append(f"Error checking file structure: {str(e)}")
        return True, "\n".join(error_details)

    # Use exifread for more targeted analysis
    try:
        with open(image_path, 'rb') as f:
            tags = exifread.process_file(f, details=True)

            # Count missing required tags as mentioned in the exiftool output
            required_tags = [
                "EXIF ExifVersion",
                "EXIF ComponentsConfiguration",
                "EXIF FlashpixVersion",
                "EXIF ColorSpace",
                "EXIF ExifImageWidth",
                "EXIF ExifImageHeight",
                "GPS GPSVersionID",
                "Image XResolution",
                "Image YResolution",
                "Image ResolutionUnit",
                "Image YCbCrPositioning"
            ]

            missing_tags = [tag for tag in required_tags if not any(tag in t for t in tags)]

            if len(missing_tags) >= 5:  # If several required tags are missing
                corruption_markers.append(f"Missing {len(missing_tags)} required EXIF/JPEG tags")
                is_corrupted = True

            # Check for DateTimeOriginal tag which was mentioned in the overlapping issue
            date_time_tag = next((t for t in tags if "DateTimeOriginal" in t), None)
            if date_time_tag:
                # Try to detect potential overlap by checking string format
                tag_value = str(tags[date_time_tag])
                # If the tag value doesn't look like a date
                if not re.match(r'\d{4}:\d{2}:\d{2}', tag_value):
                    corruption_markers.append(f"Possible tag value overlap in {date_time_tag}")
                    is_corrupted = True
    except Exception as e:
        # Only consider it corrupted if it's specifically an EXIF error
        if "EXIF" in str(e) or "Corrupted" in str(e):
            error_details.append(f"Error analyzing EXIF: {str(e)}")
            return True, "\n".join(error_details)

    # Add the corruption markers to our error details
    error_details.extend(corruption_markers)

    # Try to check if the file can be properly opened with Pillow
    try:
        with Image.open(image_path) as img:
            # Try to access EXIF data - check for potential errors
            try:
                exif = img._getexif()
                if exif is None and corruption_markers:
                    # If we have corruption markers and no EXIF data can be read
                    is_corrupted = True
            except Exception:
                # If we can't read EXIF data at all with Pillow
                is_corrupted = True
                error_details.append("Cannot read EXIF data with Pillow")
    except Exception:
        # If we can't open the image at all with Pillow
        is_corrupted = True
        error_details.append("Cannot open image with Pillow")

    return is_corrupted, "\n".join(error_details)


def process_directory(directory, verbose=False):
    """
    Recursively process all JPG files in the directory and its subdirectories.

    Args:
        directory: Directory path to process
        verbose: Whether to print detailed validation output

    Returns:
        dict: Statistics on files processed and corrupted
    """
    stats = {
        'total': 0,
        'corrupted': 0,
        'corrupted_files': []
    }

    # Find all JPG files (case insensitive)
    jpg_pattern = re.compile(r'\.jpe?g$', re.IGNORECASE)

    for root, _, files in os.walk(directory):
        for file in files:
            if jpg_pattern.search(file):
                file_path = os.path.join(root, file)
                stats['total'] += 1
                print(f"Checking: {file_path}")

                is_corrupted, error_details = check_image_exif_corruption(file_path)

                if is_corrupted:
                    stats['corrupted'] += 1
                    stats['corrupted_files'].append(file_path)
                    print(f"CORRUPTED: {file_path}")

                    if verbose:
                        print("Error details:")
                        print(error_details)

    return stats


def main():
    parser = argparse.ArgumentParser(
        description='Check JPG files for FlowCam-specific EXIF header corruption issues.')
    parser.add_argument('directory', help='Directory to recursively search for JPG files')
    parser.add_argument('--verbose', action='store_true', help='Print detailed error output')
    parser.add_argument('--output', help='Output file to save the list of corrupted files')
    parser.add_argument('--max-files', type=int, default=0,
                        help='Maximum number of files to process (0 for all files)')

    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: {args.directory} is not a valid directory.")
        return 1

    print(f"Processing directory: {args.directory}")
    print("Checking for FlowCam-specific EXIF corruption issues...")

    stats = process_directory(args.directory, args.verbose)

    print("\nSummary:")
    print(f"Total files processed: {stats['total']}")
    print(f"Corrupted files found: {stats['corrupted']}")

    if args.output and stats['corrupted'] > 0:
        with open(args.output, 'w') as f:
            for file_path in stats['corrupted_files']:
                f.write(f"{file_path}\n")
        print(f"List of corrupted files saved to: {args.output}")

    return 0


if __name__ == "__main__":
    exit(main())