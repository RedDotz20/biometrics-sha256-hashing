"""Biometrics Hashing and Evaluation Analysis with SHA-256"""

import hashlib
import os
import random
from typing import List, Tuple
from sklearn.metrics import precision_score, recall_score, f1_score

def image_to_binary(image_path: str) -> bytes:
    """Reads an image file and returns its binary content."""
    try:
        with open(image_path, 'rb') as image_file:
            binary_data = image_file.read()
    except FileNotFoundError:
        print(f"Error: The file {image_path} was not found.")
        return b""
    except IOError:
        print(f"Error: An I/O error occurred while reading the file {image_path}.")
        return b""
    return binary_data

def generate_sha256_hash(data: bytes) -> str:
    """Generates the SHA-256 hash for the given data."""
    return hashlib.sha256(data).hexdigest()

def tamper_image(binary_data: bytes) -> bytes:
    """Simulate image tampering by altering the binary data."""
    if not binary_data:
        return b""
    tampered_data = bytearray(binary_data)
    index_to_modify = random.randint(0, len(tampered_data) - 1)
    new_value = random.randint(0, 255)
    tampered_data[index_to_modify] = new_value  # Random modification
    return bytes(tampered_data)

def evaluate_binary_vs_sha256(image_path: str, tampered: bool = False) -> Tuple[int, int]:
    """Compare raw binary data vs SHA-256 hash and evaluate using precision, recall, F1-score."""
    binary_image = image_to_binary(image_path)
    if not binary_image:
        return 0, 0
    original_sha256_hash = generate_sha256_hash(binary_image)

    if tampered:
        binary_image = tamper_image(binary_image)
        if not binary_image:
            return 0, 0

    predicted_label = 1 if generate_sha256_hash(binary_image) == original_sha256_hash else 0
    true_label = 1 if not tampered else 0  # If tampered, mismatch, otherwise match

    return true_label, predicted_label

def process_images_in_directory(directory: str) -> Tuple[float, float, float]:
    """Process all fingerprint images in the specified directory and return average metrics."""
    all_true_labels: List[int] = []
    all_predicted_labels: List[int] = []

    if not os.path.isdir(directory):
        print(f"Error: The directory {directory} does not exist.")
        return 0.0, 0.0, 0.0

    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            image_path = os.path.join(directory, filename)

            # Print which fingerprint image is being processed
            print(f"Processing original image: {filename}")

            # Test with original image (no tampering)
            true_label, predicted_label = evaluate_binary_vs_sha256(image_path, tampered=False)
            all_true_labels.append(true_label)
            all_predicted_labels.append(predicted_label)

            # Print which tampered fingerprint image is being processed
            print(f"Processing tampered image: {filename}")

            # Test with tampered image
            true_label, predicted_label = evaluate_binary_vs_sha256(image_path, tampered=True)
            all_true_labels.append(true_label)
            all_predicted_labels.append(predicted_label)

    if not all_true_labels or not all_predicted_labels:
        print("Error: No valid images processed.")
        return 0.0, 0.0, 0.0

    precision = precision_score(all_true_labels, all_predicted_labels)
    recall = recall_score(all_true_labels, all_predicted_labels)
    f1 = f1_score(all_true_labels, all_predicted_labels)

    return precision, recall, f1

def main():
    """Main Function"""
    # Path to the folder containing fingerprint images
    images_directory = "fingerprintDatasets"  # Folder with your fingerprint images

    # Process all images in the directory and get the average metrics
    precision, recall, f1 = process_images_in_directory(images_directory)

    # Output the average Precision, Recall, and F1-Score
    if precision != 0.0 or recall != 0.0 or f1 != 0.0:
        print(f"\nAverage Precision: {precision}")
        print(f"Average Recall: {recall}")
        print(f"Average F1-Score: {f1}")

if __name__ == "__main__":
    main()
