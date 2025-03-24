"""
Find duplicate assets of a reference image based on the file hash

Args:
    reference_image_path (str): Path to the reference image
    directory_path (str): Path to the directory to scan
    output_file_path (str): Path to save the results

Usage:
    python main.py ./reference.jpg --directory ./gallery --output output-file.txt

"""

import os
import argparse
from PIL import Image
import imagehash

def find_duplicates_of_image(reference_image_path, directory_path, output_file_path):

    print(f"Using reference image: {reference_image_path}")
    print(f"Scanning directory: {directory_path}")
    print(f"Results will be saved to: {output_file_path}")
    
    # Calculate hash of reference image
    try:
        reference_img = Image.open(reference_image_path)
        # Using perceptual hash (phash) which is good for finding similar images
        reference_hash = imagehash.phash(reference_img)
        print("Reference image processed successfully.")
    except Exception as e:
        print(f"Failed to process the reference image: {e}")
        return
    
    # Get all image files in the directory
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
    image_files = []
    
    for root, _, files in os.walk(directory_path):
        for file in files:
            if os.path.splitext(file.lower())[1] in image_extensions:
                image_files.append(os.path.join(root, file))
    
    print(f"Found {len(image_files)} image files to process")
    
    # Find duplicates of the reference image
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
            
            # Compare hashes - lower value means more similar
            # Using a threshold of 5 for similarity (adjust as needed)
            if reference_hash - img_hash < 5:
                duplicates.append(os.path.basename(file_path)) # Output the filename not the file path
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
        
        processed += 1
        if processed % 10 == 0 or processed == len(image_files):
            print(f"Processed {processed}/{len(image_files)} images...")
    
    # Report results
    print("\n--- RESULTS ---")
    
    if len(duplicates) == 0:
        print("No duplicate images found matching the reference image.")
        # Write empty file to indicate no duplicates
        with open(output_file_path, 'w') as f:
            pass
    else:
        print(f"Found {len(duplicates)} duplicates of the reference image.")
        
        # Write duplicates to output file
        with open(output_file_path, 'w') as f:
            f.write('\n'.join(duplicates))
        
        print(f"Duplicate filenames have been saved to {output_file_path}")

def main():
    parser = argparse.ArgumentParser(description='Find duplicates of a reference image in a directory.')
    parser.add_argument('reference_image', help='Path to the reference image')
    parser.add_argument('--directory', '-d', help='Directory to scan (defaults to directory containing reference image)')
    parser.add_argument('--output', '-o', default='duplicate-images.txt', help='Output file path (defaults to duplicate-images.txt)')
    
    args = parser.parse_args()
    
    reference_image_path = args.reference_image
    directory_path = args.directory or os.path.dirname(reference_image_path) or '.'
    output_file_path = args.output
    
    print('Image Duplicate Finder')
    print('=====================')
    
    find_duplicates_of_image(reference_image_path, directory_path, output_file_path)

if __name__ == "__main__":
    main()