import pyautogui
import time
import os
from PIL import Image
import keyboard
import random
import sys

class SatelliteImageScraper:
    def __init__(self, base_folder='satellite_images', 
                 crop_width=500, crop_height=500, 
                 crop_x_offset=100, crop_y_offset=100, batch = 50):
        """
        Initialize the scraper with a defined movement border and random positioning
        """
        self.base_folder = base_folder
        self.crop_width = crop_width
        self.crop_height = crop_height
        self.crop_x_offset = crop_x_offset
        self.crop_y_offset = crop_y_offset
        self.batch = batch
        
        # Disable fail-safe
        pyautogui.FAILSAFE = False
        
        # Create base folder
        os.makedirs(base_folder, exist_ok=True)
        
        # Image counter
        # Check if images already exist in the folder
        # Get the last images's number and start from there
        image_files = os.listdir(base_folder)
        self.image_counter = 0
        image_files = [f for f in image_files if f.endswith('.png')]
        if image_files:
            image_files.sort()
            last_image = image_files[-1]
            last_image_number = int(last_image.split('_')[-1].split('.')[0])
            self.image_counter = last_image_number


        
        
        # Define movement border
        self.setup_movement_border()

    def setup_movement_border(self):
        """
        Define a movement area in the middle of the screen
        """
        # Get screen dimensions
        screen_width, screen_height = pyautogui.size()
        
        # Define border as 60% of screen width and height
        self.border_width = int(screen_width * 0.6)
        self.border_height = int(screen_height * 0.6)
        
        # Calculate border start coordinates (centered)
        self.border_start_x = int((screen_width - self.border_width) / 2)
        self.border_start_y = int((screen_height - self.border_height) / 2)
        
        # Border end coordinates
        self.border_end_x = self.border_start_x + self.border_width
        self.border_end_y = self.border_start_y + self.border_height
        
        print(f"Movement Border:")
        print(f"  Start: ({self.border_start_x}, {self.border_start_y})")
        print(f"  End: ({self.border_end_x}, {self.border_end_y})")
        print(f"  Size: {self.border_width}x{self.border_height}")

    def move_to_random_position(self):
        """
        Move cursor to a random position within the defined border
        """
        # Generate random x and y coordinates within the border
        random_x = random.randint(self.border_start_x, self.border_end_x)
        random_y = random.randint(self.border_start_y, self.border_end_y)
        
        # Move cursor to the random position
        pyautogui.moveTo(random_x, random_y, duration=0.5)
        
        print(f"Moved to random position: ({random_x}, {random_y})")

    def capture_and_crop_screen(self):
        """
        Capture and crop the screen
        """
        screenshot = pyautogui.screenshot()
        cropped_image = screenshot.crop((
            self.crop_x_offset, 
            self.crop_y_offset, 
            self.crop_x_offset + self.crop_width, 
            self.crop_y_offset + self.crop_height
        ))
        self.image_counter += 1
        self.batch -= 1
        filename = os.path.join(
            self.base_folder, 
            f'satellite_crop_{self.image_counter:04d}.png'
        )
        cropped_image.save(filename)
        print(f"Saved cropped image: {filename}")

    def drag_map(self, drag_distance=400, direction='right'):
        """
        Drag map within the defined movement border
        """
        # Get current mouse position
        current_x, current_y = pyautogui.position()
        
        # Get safe drag coordinates
        new_x, new_y = self.get_safe_drag_coordinates(current_x, current_y, drag_distance, direction)
        
        # Calculate relative drag
        drag_x = new_x - current_x
        drag_y = new_y - current_y
   
        pyautogui.drag(drag_x, drag_y, duration=1.5)
        
        return direction

    def get_safe_drag_coordinates(self, current_x, current_y, drag_distance, direction):
        """
        Calculate safe drag coordinates within the movement border
        """
        new_x, new_y = current_x, current_y
        
        if direction == 'right':
            new_x = min(current_x + drag_distance, self.border_end_x)
        elif direction == 'left':
            new_x = max(current_x - drag_distance, self.border_start_x)
        elif direction == 'up':
            new_y = max(current_y - drag_distance, self.border_start_y)
        elif direction == 'down':
            new_y = min(current_y + drag_distance, self.border_end_y)
        
        return new_x, new_y

    def run(self):
        """
        Main run method for the scraper
        """
        print("Satellite Image Crop and Capture Script")
        print("---------------------------------------")
        print("Instructions:")
        print("1. Open Google Maps in Satellite View")
        print("2. Position the view exactly where you want to start")
        print(f"3. Will crop images to {self.crop_width}x{self.crop_height}")
        print("4. Moves within a defined border in the screen center")
        print("5. Cursor will move to random positions before capture")
        
        # Drag sequence
        drag_sequence = ['right', 'down', 'left', 'up']
        current_choice = random.choice(drag_sequence)
        previous_choice = current_choice
        compliments = {
            'right': 'left',
            'left': 'right',
            'up': 'down',
            'down': 'up'
        }

        while True:
            # Move to a random position within the border
            self.move_to_random_position()
            
            time.sleep(2)
            keyboard.press_and_release('c')
            self.capture_and_crop_screen()
            
            # Choose next drag direction
            current_choice = random.choice(drag_sequence)
            while current_choice == compliments[previous_choice]:
                current_choice = random.choice(drag_sequence)

            # Drag map
            self.drag_map(direction=current_choice)
            previous_choice = current_choice
            
            # Check for exit
            if self.batch == 0 or keyboard.is_pressed('q'):
                print("Finished capturing images.")
                break

def main():
    try:
        batch = sys.argv[1]
    except:
        batch = 50

        #Debug printing
    print(f"Batch: {batch}")
    scraper = SatelliteImageScraper(
        base_folder='satellite_images',
        crop_width=650,
        crop_height=650,
        crop_x_offset=100,
        crop_y_offset=200,
        batch = 50
    )
    scraper.run()

if __name__ == "__main__":
    time.sleep(2)
    main()