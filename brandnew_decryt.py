from PIL import Image
import numpy as np
import random

BLOCK_SIZE = 50  # Size of each block for shuffling

def decrypt_image(encrypted_path, output_path):
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

    # Create block indices
    block_indices = [(i, j) for i in range(num_blocks_y) for j in range(num_blocks_x)]

    # Sort shuffled indices based on their positions during encryption
    shuffled_indices = block_indices[:]
    random.shuffle(shuffled_indices)

    # Reverse the shuffle
    reverse_mapping = {shuffled: original for original, shuffled in zip(block_indices, shuffled_indices)}

    # Create decrypted image array
    decrypted_array = np.zeros_like(encrypted_array)

    # Place blocks back to their original positions
    for shuffled_index, original_index in reverse_mapping.items():
        shuffled_y, shuffled_x = shuffled_index
        original_y, original_x = original_index
        block = encrypted_array[shuffled_y * BLOCK_SIZE:(shuffled_y + 1) * BLOCK_SIZE,
                                 shuffled_x * BLOCK_SIZE:(shuffled_x + 1) * BLOCK_SIZE]
        decrypted_array[original_y * BLOCK_SIZE:(original_y + 1) * BLOCK_SIZE,
                         original_x * BLOCK_SIZE:(original_x + 1) * BLOCK_SIZE] = block

    # Save the decrypted image
    decrypted_img = Image.fromarray(decrypted_array)
    decrypted_img.save(output_path)
    print(f"Decrypted image saved at {output_path}")

if __name__ == "__main__":
    encrypted_image_path = input("Enter the path of the encrypted image: ")
    output_image_path = input("Enter the output path for the decrypted image: ")
    decrypt_image(encrypted_image_path, output_image_path)
