# Image Duplicate Finder

This utility identifies duplicate or visually similar images based on perceptual hashing. It compares a reference image against all images in a specified directory (including subdirectories) and outputs the results.

## How It Works

1. The program calculates a perceptual hash (pHash) of the reference image
2. It recursively finds all image files in the target directory
3. Each image is compared to the reference image by calculating the difference between their hashes
4. Images with a hash difference less than 5 are considered duplicates
5. Results are saved to the specified output file

## Example

```bash
python find-duplicates-to-csv.py ./product_catalog/reference.jpg --directory ./assets --output duplicates.csv
```

This will scan all images in the `./assets` directory, comparing them to `./product_catalog/reference.jpg`, and save any matches to `duplicates.csv`.

## Requirements

- Python 3.6+
- [Pillow](https://pillow.readthedocs.io/en/stable/) - The Python Imaging Library
- [ImageHash](https://github.com/JohannesBuchner/imagehash) - Perceptual image hashing for Python

## Installation

1. Install the required packages:

```bash
pip install Pillow imagehash
```

## Usage

There are two variants:

### 1. Text Output Version

```bash
python find-duplicates-to-text.py ./reference.jpg --directory ./gallery --output results.txt
```

Outputs a simple text file with each duplicate filename on a new line.

### 2. CSV Output Version

```bash
python find-duplicates-to-csv.py ./reference.jpg --directory ./gallery --output results.csv
```

Outputs a CSV file with three columns:
- Product ID (extracted from filename prefix before the first underscore)
- Asset ID (filename without extension)
- Filename (complete filename with extension)

### Parameters

- `reference_image`: Path to the reference image to compare against (required)
- `--directory` or `-d`: Directory to scan for duplicate images (defaults to the directory of the reference image)
- `--output` or `-o`: Path to save the results (defaults to `duplicate-images.txt` or `duplicate-images.csv`)

### License
This project is licensed under the MIT License - see the LICENSE file for details.