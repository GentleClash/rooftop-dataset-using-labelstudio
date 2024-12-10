import os
import re
import shutil

def serialize_images(folder_path, prefix='satellite_crop_', start_index=1):
    """
    Systematically rename image files to ensure sequential naming
    
    :param folder_path: Path to the folder containing images
    :param prefix: Prefix for the new filename
    :param start_index: Starting index for serialization
    """
    # Supported image extensions
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff']
    
    # Get all image files in the directory
    image_files = [f for f in os.listdir(folder_path) 
                   if os.path.isfile(os.path.join(folder_path, f)) 
                   and os.path.splitext(f)[1].lower() in image_extensions]
    
    # Sort files to maintain some semblance of original order
    # This will sort based on the original filename
    image_files.sort(key=lambda x: extract_number(x))
    
    # Rename files
    current_index = start_index
    for filename in image_files:
        # Get the file extension
        file_ext = os.path.splitext(filename)[1]
        
        # Create new filename
        new_filename = f"{prefix}{current_index:04d}{file_ext}"
        
        # Full paths
        old_path = os.path.join(folder_path, filename)
        new_path = os.path.join(folder_path, new_filename)
        
        # Rename the file
        shutil.move(old_path, new_path)
        
        print(f"Renamed: {filename} -> {new_filename}")
        
        # Increment index
        current_index += 1
    
    print(f"\nTotal images processed: {len(image_files)}")
    print(f"Serialization complete. New files start from {prefix}{start_index:04d}")

def extract_number(filename):
    """
    Extract numeric value from filename for sorting
    
    :param filename: Filename to extract number from
    :return: Extracted number or 0 if no number found
    """
    # Try to extract number from filename
    match = re.search(r'(\d+)', filename)
    return int(match.group(1)) if match else 0

def main():
    # Default folder path (current directory)
    folder_path = 'satellite_images'
    
    # Ensure folder exists
    if not os.path.exists(folder_path):
        print(f"Error: Folder {folder_path} does not exist!")
        return
    
    # Run serialization
    serialize_images(
        folder_path=folder_path,
        prefix='satellite_crop_',
        start_index=1
    )

if __name__ == "__main__":
    main()