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

# Configure PyAutoGUI settings
pyautogui.PAUSE = 0.5  # Add a small pause between actions
pyautogui.MINIMUM_DURATION = 0.1  # Minimum time for mouse movements
pyautogui.MINIMUM_SLEEP = 0.1  # Minimum time between actions

# Get screen size
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
# Define safe margins (10% of screen size)
MARGIN = 50
SAFE_X_MIN = MARGIN
SAFE_X_MAX = SCREEN_WIDTH - MARGIN
SAFE_Y_MIN = MARGIN
SAFE_Y_MAX = SCREEN_HEIGHT - MARGIN

# Configure logging to show only redis
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


WEBSITES = os.getenv('WEBSITES', 'https://www.google.com,https://www.github.com,https://www.stackoverflow.com,https://www.reddit.com,https://www.youtube.com,https://www.nytimes.com,https://www.wikipedia.org,https://www.amazon.com,https://www.twitter.com,https://www.linkedin.com').split(',')

# Track opened websites with their open times

class RedisAction:
    def __init__(self):
        self.opened_websites = {}
        self.total_runtime_seconds = 0
        self.remaining_runtime_seconds = 0
        self.end_time = None
        self.browser_path = None
        self.logger = logging.getLogger(__name__)

    def get_safe_coordinates(self):
        """Get random coordinates within safe screen bounds"""
        x = random.randint(SAFE_X_MIN, SAFE_X_MAX)
        y = random.randint(SAFE_Y_MIN, SAFE_Y_MAX)
        return x, y

    def safe_mouse_move(self, x, y, relative=False):
        """Safely move mouse to coordinates"""
        try:
            if relative:
                current_x, current_y = pyautogui.position()
                target_x = current_x + x
                target_y = current_y + y
                
                # Check if target position is within safe bounds
                if SAFE_X_MIN <= target_x <= SAFE_X_MAX and SAFE_Y_MIN <= target_y <= SAFE_Y_MAX:
                    pyautogui.moveRel(x, y, duration=0.2)
            else:
                # Ensure coordinates are within safe bounds
                safe_x = max(SAFE_X_MIN, min(x, SAFE_X_MAX))
                safe_y = max(SAFE_Y_MIN, min(y, SAFE_Y_MAX))
                pyautogui.moveTo(safe_x, safe_y, duration=0.2)
        except pyautogui.FailSafeException:
            pass
        except Exception as e:
            pass

    def safe_click(self, x=None, y=None):
        """Safely click at coordinates"""
        try:
            if x is None or y is None:
                x, y = self.get_safe_coordinates()
            self.safe_mouse_move(x, y)
            pyautogui.click()
        except Exception as e:
            pass

    def safe_scroll(self, amount):
        """Safely scroll"""
        try:
            pyautogui.scroll(amount)
        except Exception as e:
            pass

    def safe_type(self, text):
        """Safely type text"""
        try:
            pyautogui.typewrite(text, interval=0.1)
        except Exception as e:
            pass

    def open_random_website(self):
        """Open a random website from the list using the specified browser"""
        website = random.choice(WEBSITES)
        
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
        try:
            pyautogui.hotkey('ctrl', 'w')
            if website in self.opened_websites:
                del self.opened_websites[website]
        except Exception as e:
            pass

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
        # Get random position within safe bounds
        x, y = self.get_safe_coordinates()
        
        # Move to random position
        self.safe_mouse_move(x, y)
        
        # Randomly choose action with weights
        action = random.choices(
            ['click', 'scroll', 'website', 'keyboard_press', 'mouse_move', 'mouse_move_relative', 'scroll_up', 'scroll_down'],
            weights=[
                float(os.getenv('REDIS_ACTION_CLICK_WEIGHT', 0.48)),
                float(os.getenv('REDIS_ACTION_SCROLL_WEIGHT', 0.48)),
                float(os.getenv('REDIS_ACTION_WEBSITE_WEIGHT', 0.04)),
                float(os.getenv('REDIS_PRESS_KEYBOARD_WEIGHT', 0.04)),
                float(os.getenv('OTHER_WEIGHT', 0.04)),
                float(os.getenv('OTHER_WEIGHT', 0.04)),
                float(os.getenv('OTHER_WEIGHT', 0.04)),
                float(os.getenv('OTHER_WEIGHT', 0.04))
            ],
            k=1
        )[0]
        
        if action == 'click':
            self.safe_click(x, y)
        elif action == 'scroll':
            scroll_amount = random.randint(-100, 100)
            self.safe_scroll(scroll_amount)
        elif action == 'mouse_move':
            self.safe_mouse_move(x, y)
        elif action == 'mouse_move_relative':
            rel_x = random.randint(-100, 100)
            rel_y = random.randint(-100, 100)
            self.safe_mouse_move(rel_x, rel_y, relative=True)
        elif action == 'keyboard_press':
            random_number = random.randint(1, 8)
            for i in range(random_number):
                self.safe_type(random.choice(string.ascii_letters + string.digits))
                time.sleep(0.1)
            for i in range(random_number):
                self.safe_type('\b')  # backspace
                time.sleep(0.1)
        elif action == 'scroll_up':
            self.safe_scroll(100)
        elif action == 'scroll_down':
            self.safe_scroll(-100)
        elif action == 'website':
            if os.getenv('WEBSITE_ENABLED', 'true') == 'true':
                self.open_random_website()

def main():
    logger.info(":::::::::  :::::::::: :::::::::  :::::::::::  ::::::::            :::      ::::::::  ::::::::::: :::::::::::  ::::::::  ::::    ::: ")
    logger.info(":+:    :+: :+:        :+:    :+:     :+:     :+:    :+:         :+: :+:   :+:    :+:     :+:         :+:     :+:    :+: :+:+:   :+: ")
    logger.info(" +:+    +:+ +:+        +:+    +:+     +:+     +:+               +:+   +:+  +:+            +:+         +:+     +:+    +:+ :+:+:+  +:+ ")
    logger.info(" +#++:++#:  +#++:++#   +#+    +:+     +#+     +#++:++#++       +#++:++#++: +#+            +#+         +#+     +#+    +:+ +#+ +:+ +#+ ")
    logger.info(" +#+    +#+ +#+        +#+    +#+     +#+            +#+       +#+     +#+ +#+            +#+         +#+     +#+    +#+ +#+  +#+#+# ")
    logger.info(" #+#    #+# #+#        #+#    #+#     #+#     #+#    #+#       #+#     #+# #+#    #+#     #+#         #+#     #+#    #+# #+#   #+#+# ")
    logger.info(" ###    ### ########## #########  ###########  ########        ###     ###  ########      ###     ###########  ########  ###    #### ")
    
    # Set end time (default to 1 hour if not specified)
    hours = int(os.getenv('REDIS_ACTION_HOURS', 1))
    end_time = datetime.now() + timedelta(hours=hours)
    total_runtime_seconds = hours * 3600

    redis_action = RedisAction()
    
    try:
        while datetime.now() < end_time:
            # Check if any websites need to be closed
            redis_action.check_websites_to_close(total_runtime_seconds)
            
            remaining_runtime_seconds = (end_time - datetime.now()).total_seconds()
            # Perform random action
            redis_action.perform_random_action(total_runtime_seconds, remaining_runtime_seconds)
            
            # Random wait between min and max wait times (default 5-15 seconds if not specified)
            wait_time = random.uniform(
                float(os.getenv('REDIS_ACTION_MIN_WAIT_TIME', 5)),
                float(os.getenv('REDIS_ACTION_MAX_WAIT_TIME', 15))
            )
            time.sleep(wait_time)
                
        logger.info(":::::::::  :::::::::: :::::::::  :::::::::::  ::::::::            :::      ::::::::  ::::::::::: :::::::::::  ::::::::  ::::    ::: ")
        logger.info(":+:    :+: :+:        :+:    :+:     :+:     :+:    :+:         :+: :+:   :+:    :+:     :+:         :+:     :+:    :+: :+:+:   :+: ")
        logger.info(" +:+    +:+ +:+        +:+    +:+     +:+     +:+               +:+   +:+  +:+            +:+         +:+     +:+    +:+ :+:+:+  +:+ ")
        logger.info(" +#++:++#:  +#++:++#   +#+    +:+     +#+     +#++:++#++       +#++:++#++: +#+            +#+         +#+     +#+    +:+ +#+ +:+ +#+ ")
        logger.info(" +#+    +#+ +#+        +#+    +#+     +#+            +#+       +#+     +#+ +#+            +#+         +#+     +#+    +#+ +#+  +#+#+# ")
        logger.info(" #+#    #+# #+#        #+#    #+#     #+#     #+#    #+#       #+#     #+# #+#    #+#     #+#         #+#     #+#    #+# #+#   #+#+# ")
        logger.info(" ###    ### ########## #########  ###########  ########        ###     ###  ########      ###     ###########  ########  ###    #### ")
    except KeyboardInterrupt:
        pass
    finally:
        # Close any remaining open websites
        for website in list(redis_action.opened_websites.keys()):
            redis_action.close_website(website)

if __name__ == "__main__":
    main() 