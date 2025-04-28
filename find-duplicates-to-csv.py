"""
Finds duplicate assets based on the file hash of a reference image
and outputs any results to a .csv file with 3 columns (Product ID, Asset ID, Filename)
 
Args:
    reference_image_path (str): Path to the reference image
    directory_path (str): Path to the directory to scan
    output_file_path (str): Path to save the results

Usage:
    python find-duplicates-to-csv.py ./reference.jpg --directory ./gallery --output output-file.csv
"""

import os
import argparse
import csv
import re
from PIL import Image 
import imagehash

def extract_product_id(filename):
    """
    Extract product ID from filename assuming format: productID_restOfFilename
    Returns the entire filename if pattern doesn't match
    """
    match = re.match(r"^([^_]+)_", filename)
    return match.group(1) if match else filename

def find_duplicates_of_image(reference_image_path, directory_path, output_file_path):
    print(f"Using reference image: {reference_image_path}")
    print(f"Scanning directory: {directory_path}")
    print(f"Results will be saved to: {output_file_path}")
    
    # Calculate perceptual hash of reference image
    try:
        reference_img = Image.open(reference_image_path)
        reference_hash = imagehash.phash(reference_img)
        print("Reference image processed successfully.")
    except Exception as e:
        print(f"Failed to process the reference image: {e}")
        return
    
    # Define supported image formats and collect all matching files from directory
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
    image_files = [
        os.path.join(root, file)
        for root, _, files in os.walk(directory_path)
        for file in files if os.path.splitext(file.lower())[1] in image_extensions
    ]
    
    print(f"Found {len(image_files)} image files to process")
    
    # Compare each image against the reference image
    duplicates = []
    processed = 0
    
    for file_path in image_files:
        # Skip the reference image itself
        if os.path.abspath(file_path) == os.path.abspath(reference_image_path):
            processed += 1
            continue
        
        try:
            img = Image.open(file_path)
            img_hash = imagehash.phash(img)
            
            # Images with hash difference less than 5 are considered similar
            if reference_hash - img_hash < 5:
                filename = os.path.basename(file_path)
                # Extract asset ID as the filename without extension
                asset_id, _ = os.path.splitext(filename)
                # Extract product ID using regex pattern
                product_id = extract_product_id(filename)
                duplicates.append([product_id, asset_id, filename])
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
        
        # Update and display progress periodically
        processed += 1
        if processed % 10 == 0 or processed == len(image_files):
            print(f"Processed {processed}/{len(image_files)} images...")
    
    # Report and save results to CSV file
    print("\n--- RESULTS ---")
    
    if not duplicates:
        print("No duplicate images found matching the reference image.")
        # Create empty output file when no duplicates found
        open(output_file_path, 'w').close()
    else:
        print(f"Found {len(duplicates)} duplicates of the reference image.")
        
        # Write results to CSV with headers and one duplicate per row
        with open(output_file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Product ID", "Asset ID", "Filename"])  # CSV header row
            writer.writerows(duplicates)  # Write all duplicate entries
        
        print(f"Duplicate filenames have been saved to {output_file_path}")

def main():
    # Configure command-line argument parsing
    parser = argparse.ArgumentParser(description='Find duplicates of a reference image in a directory and save results as CSV.')
    parser.add_argument('reference_image', help='Path to the reference image')
    parser.add_argument('--directory', '-d', help='Directory to scan (defaults to directory containing reference image)')
    parser.add_argument('--output', '-o', default='duplicate-images.csv', help='Output CSV file path (defaults to duplicate-images.csv)')
    
    args = parser.parse_args()
    
    # Set default directory to reference image location if not provided
    reference_image_path = args.reference_image
    directory_path = args.directory or os.path.dirname(reference_image_path) or '.'
    output_file_path = args.output
    
    print('Image Duplicate Finder')
    print('=====================')
    
    find_duplicates_of_image(reference_image_path, directory_path, output_file_path)

if __name__ == "__main__":
    main()