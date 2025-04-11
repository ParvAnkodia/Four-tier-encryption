### Encrypt Image - encrypt_image.py
from PIL import Image, ImageOps
import numpy as np
import random
import json

BLOCK_SIZE = 50  # Size of each block for shuffling


def invert_colors(image_array):
    # Invert the colors by subtracting each pixel from 255
    return 255 - image_array


def encrypt_image(image_path, output_path, shuffle_map_path):
    # Load the image
    img = Image.open(image_path)
    img = img.convert('RGB')  # Ensure 3-channel image

    # Apply negative color filter
    img = ImageOps.invert(img)

    # Convert to numpy array
    img_array = np.array(img)

    # Get image dimensions
    h, w, c = img_array.shape

    # Calculate the number of blocks
    num_blocks_x = w // BLOCK_SIZE
    num_blocks_y = h // BLOCK_SIZE

    # Create block indices
    block_indices = [(i, j) for i in range(num_blocks_y) for j in range(num_blocks_x)]

    # Shuffle block indices and store the mapping
    shuffled_indices = block_indices[:]
    random.shuffle(shuffled_indices)

    # Save the shuffle mapping
    shuffle_map = {str(index): shuffled_indices[i] for i, index in enumerate(block_indices)}
    with open(shuffle_map_path, 'w') as file:
        json.dump(shuffle_map, file)

    # Create an encrypted image array
    encrypted_array = np.zeros_like(img_array)

    # Shuffle blocks
    for index, shuffled_index in zip(block_indices, shuffled_indices):
        y, x = index
        shuffled_y, shuffled_x = shuffled_index
        block = img_array[y * BLOCK_SIZE:(y + 1) * BLOCK_SIZE, x * BLOCK_SIZE:(x + 1) * BLOCK_SIZE]
        encrypted_array[shuffled_y * BLOCK_SIZE:(shuffled_y + 1) * BLOCK_SIZE,
                         shuffled_x * BLOCK_SIZE:(shuffled_x + 1) * BLOCK_SIZE] = block

    # Convert the encrypted array back to an image
    encrypted_img = Image.fromarray(encrypted_array)

    # Save the encrypted image with negative colors
    encrypted_img.save(output_path)
    print(f"Encrypted image saved at {output_path}")
    print(f"Shuffle map saved at {shuffle_map_path}")


if __name__ == "__main__":
    input_image_path = input("Enter the path of the image to encrypt: ")
    output_image_path = input("Enter the output path for the encrypted image: ")
    shuffle_map_path = input("Enter the path to save the shuffle map (JSON file): ")
    encrypt_image(input_image_path, output_image_path, shuffle_map_path)

### Decrypt Image - decrypt_image.py
from PIL import Image, ImageOps
import numpy as np
import json

BLOCK_SIZE = 50  # Size of each block for shuffling


def decrypt_image(encrypted_path, shuffle_map_path, output_path):
    # Load the encrypted image
    encrypted_img = Image.open(encrypted_path)
    encrypted_img = encrypted_img.convert('RGB')

    # Convert to numpy array
    encrypted_array = np.array(encrypted_img)

    # Get image dimensions
    h, w, c = encrypted_array.shape

    # Calculate the number of blocks
    num_blocks_x = w // BLOCK_SIZE
    num_blocks_y = h // BLOCK_SIZE

    # Load the shuffle map
    with open(shuffle_map_path, 'r') as file:
        shuffle_map = json.load(file)

    # Convert keys back to tuples
    shuffle_map = {eval(key): tuple(value) for key, value in shuffle_map.items()}

    # Create decrypted image array
    decrypted_array = np.zeros_like(encrypted_array)

    # Place blocks back to their original positions
    for original_index, shuffled_index in shuffle_map.items():
        shuffled_y, shuffled_x = shuffled_index
        original_y, original_x = original_index
        block = encrypted_array[shuffled_y * BLOCK_SIZE:(shuffled_y + 1) * BLOCK_SIZE,
                                 shuffled_x * BLOCK_SIZE:(shuffled_x + 1) * BLOCK_SIZE]
        decrypted_array[original_y * BLOCK_SIZE:(original_y + 1) * BLOCK_SIZE,
                         original_x * BLOCK_SIZE:(original_x + 1) * BLOCK_SIZE] = block

    # Convert the decrypted array back to an image
    decrypted_img = Image.fromarray(decrypted_array)

    # Remove negative color filter by reapplying inversion
    decrypted_img = ImageOps.invert(decrypted_img)

    # Save the decrypted image
    decrypted_img.save(output_path)
    print(f"Decrypted image saved at {output_path}")


if __name__ == "__main__":
    encrypted_image_path = input("Enter the path of the encrypted image: ")
    shuffle_map_path = input("Enter the path of the shuffle map (JSON file): ")
    output_image_path = input("Enter the output path for the decrypted image: ")
    decrypt_image(encrypted_image_path, shuffle_map_path, output_image_path)
