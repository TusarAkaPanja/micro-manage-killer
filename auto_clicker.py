import pyautogui
import random
import time
import webbrowser
import subprocess
import platform
from datetime import datetime, timedelta
import os
import logging
import string
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


WEBSITES = os.getenv('WEBSITES', 'https://www.google.com,https://www.github.com,https://www.stackoverflow.com,https://www.reddit.com,https://www.youtube.com,https://www.nytimes.com,https://www.wikipedia.org,https://www.amazon.com,https://www.twitter.com,https://www.linkedin.com').split(',')

# Track opened websites with their open times

class AutoClicker:
    def __init__(self):
        self.opened_websites = {}
        self.total_runtime_seconds = 0
        self.remaining_runtime_seconds = 0
        self.end_time = None
        self.browser_path = None
        self.logger = logging.getLogger(__name__)

    def open_random_website(self):
        """Open a random website from the list using the specified browser"""
        website = random.choice(WEBSITES)
        self.logger.info(f"Opening website: {website}")
        
        if self.browser_path:
            # Open with specific browser
            if platform.system() == 'Windows':
                subprocess.Popen([self.browser_path, website])
            else:
                subprocess.Popen([self.browser_path, website])
        else:
            # Use default browser
            webbrowser.open(website)
            
        # Track when this website was opened
        self.opened_websites[website] = datetime.now()
        return website

    def close_website(self, website):
        """Close a website by keyboard shortcut"""
        # self.logger.info(f"Closing website: {website}")
        # Simulate Ctrl+W to close the tab
        pyautogui.hotkey('ctrl', 'w')
        # Remove from tracking
        if website in self.opened_websites:
            del self.opened_websites[website]

    def check_websites_to_close(self, total_runtime_seconds):
        """Check if any websites need to be closed based on 2% rule"""
        min_open_time_seconds = total_runtime_seconds * 0.02  # 2% of total runtime
        current_time = datetime.now()
        
        websites_to_close = []
        for website, open_time in self.opened_websites.items():
            time_open = (current_time - open_time).total_seconds()
            if time_open >= min_open_time_seconds:
                websites_to_close.append(website)
        
        for website in websites_to_close:
            self.close_website(website)

    def perform_random_action(self, total_runtime_seconds: int, remaining_runtime_seconds: int) -> None:
        """Perform a random action: click, scroll, or open website"""
        # Get screen size
        screen_width, screen_height = pyautogui.size()
        
        # Generate random position
        x = random.randint(0, screen_width - 1)
        y = random.randint(0, screen_height - 1)
        
        # Move to random position
        pyautogui.moveTo(x, y, duration=0.25)
        
        # Randomly choose action with weights
        # 48% chance to click, 48% chance to scroll, 4% chance to open website
        # k is the number of times to repeat the action
        action = random.choices(
            ['click', 'scroll', 'website','keyboard_press', 'mouse_move', 'mouse_move_relative', 'scroll_up', 'scroll_down'],
            weights=[float(os.getenv('AUTO_CLICKER_CLICK_WEIGHT', 0.48)), float(os.getenv('AUTO_CLICKER_SCROLL_WEIGHT', 0.48)), float(os.getenv('AUTO_CLICKER_WEBSITE_WEIGHT', 0.04)), float(os.getenv('AUTO_PRESS_KEYBOARD_WEIGHT', 0.04)), float(os.getenv('OTHER_WEIGHT', 0.04)), float(os.getenv('OTHER_WEIGHT', 0.04)), float(os.getenv('OTHER_WEIGHT', 0.04)), float(os.getenv('OTHER_WEIGHT', 0.04))],
            k=1
        )[0]
        # test_action = random.choices(
        #     ['keyboard_press', 'mouse_move', 'mouse_move_relative', 'scroll_up', 'scroll_down'],
        #     weights=[float(os.getenv('AUTO_PRESS_KEYBOARD_WEIGHT', 0.04)), float(os.getenv('OTHER_WEIGHT', 0.04)), float(os.getenv('OTHER_WEIGHT', 0.04)), float(os.getenv('OTHER_WEIGHT', 0.04)), float(os.getenv('OTHER_WEIGHT', 0.04))],
        #     k=1
        # )[0]
        
        if action == 'click':
            # self.logger.info(f"Clicking at position ({x}, {y})")
            pyautogui.click(x, y)
        elif action == 'scroll':
            scroll_amount = random.randint(-100, 100)
            # self.logger.info(f"Scrolling {scroll_amount} at position ({x}, {y})")
            pyautogui.scroll(scroll_amount)

        elif action == 'mouse_move':
            pyautogui.moveTo(x, y)

        elif action == 'mouse_move_relative':
            pyautogui.moveRel(x, y)
        
        elif action == 'keyboard_press':
            random_number = random.randint(1, 8)
            for i in range(random_number):
                # logger.info(f"Pressing {random.choice(string.ascii_letters + string.digits)}")
                pyautogui.press(random.choice(string.ascii_letters + string.digits))
                time.sleep(0.1)
            for i in range(random_number):
                # logger.info(f"Pressing backspace")
                pyautogui.press('backspace')
                time.sleep(0.1)

        elif action == 'scroll_up':
            pyautogui.scroll(100)

        elif action == 'scroll_down':
            pyautogui.scroll(-100)
        
        elif action == 'website':
            # Try to find Chrome or Brave browser
            if platform.system() == 'Windows':
                CHROME_PATH = os.getenv('CHROME_PATH')
                BRAVE_PATH = os.getenv('BRAVE_PATH')
                EDGE_PATH = os.getenv('EDGE_PATH')
                chrome_paths = [
                    CHROME_PATH,
                    BRAVE_PATH,
                    EDGE_PATH,
                ]
                for path in chrome_paths:
                    try:
                        if path:
                            if subprocess.run(["powershell", "-Command", f"Test-Path '{path}'"], 
                                            capture_output=True).stdout.strip() == b'True':
                                self.browser_path = path if os.path.exists(path) else None
                            break
                    except:
                        pass
            else:  # Linux/MacOS
                for browser in ['google-chrome', 'brave-browser']:
                    try:
                        if subprocess.run(['which', browser], 
                                        capture_output=True).returncode == 0:
                            self.browser_path = browser
                            break
                    except:
                        pass
            
            self.open_random_website()

def main():
    logger.info("Auto-clicker started. Press Ctrl+C to stop.")
    
    # Set end time (default to 1 hour if not specified)
    hours = int(os.getenv('AUTO_CLICKER_HOURS', 1))
    end_time = datetime.now() + timedelta(hours=hours)
    total_runtime_seconds = hours * 3600
    
    logger.info(f"Will run until: {end_time.strftime('%H:%M:%S')}")
    logger.info(f"Website close delay: {total_runtime_seconds * 0.02:.1f} seconds (2% of total runtime)")
    logger.info(f"Click weight: {os.getenv('AUTO_CLICKER_CLICK_WEIGHT', 0.48)}")
    logger.info(f"Scroll weight: {os.getenv('AUTO_CLICKER_SCROLL_WEIGHT', 0.48)}")
    logger.info(f"Website weight: {os.getenv('AUTO_CLICKER_WEBSITE_WEIGHT', 0.04)}")
    logger.info(f"Min wait time: {os.getenv('AUTO_CLICKER_MIN_WAIT_TIME', 5)}")
    logger.info(f"Max wait time: {os.getenv('AUTO_CLICKER_MAX_WAIT_TIME', 15)}")
    logger.info(f"Websites: {os.getenv('WEBSITES', 'https://www.google.com,https://www.github.com,https://www.stackoverflow.com,https://www.reddit.com,https://www.youtube.com,https://www.nytimes.com,https://www.wikipedia.org,https://www.amazon.com,https://www.twitter.com,https://www.linkedin.com')}")
    logger.info(f"GO GET SOME LIFE for {hours} hours")
    logger.info(f"--------------------------------")

    auto_clicker = AutoClicker()
    
    try:
        while datetime.now() < end_time:
            # Check if any websites need to be closed
            auto_clicker.check_websites_to_close(total_runtime_seconds)
            
            remaining_runtime_seconds = (end_time - datetime.now()).total_seconds()
            # Perform random action
            auto_clicker.perform_random_action(total_runtime_seconds, remaining_runtime_seconds)
            
            # Random wait between min and max wait times (default 5-15 seconds if not specified)
            wait_time = random.uniform(
                float(os.getenv('AUTO_CLICKER_MIN_WAIT_TIME', 5)),
                float(os.getenv('AUTO_CLICKER_MAX_WAIT_TIME', 15))
            )
            # logger.info(f"Waiting {wait_time:.1f} seconds...")
            time.sleep(wait_time)
                
        logger.info("Finished running.")
    except KeyboardInterrupt:
        logger.info("Auto-clicker stopped by user.")
    finally:
        # Close any remaining open websites
        for website in list(auto_clicker.opened_websites.keys()):
            auto_clicker.close_website(website)

if __name__ == "__main__":
    main() 