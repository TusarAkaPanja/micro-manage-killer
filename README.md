# Auto Clicker with Website Navigation

This script performs random actions on your computer, including:
- Clicking at random screen positions
- Scrolling up/down at random positions
- Opening random websites from a predefined list

## Features

- Random actions with configurable frequency
- Opens websites in Chrome or Brave browser (when available)
- Websites stay open for at least 2% of the total runtime
- Can run in Docker container for isolation

## Requirements (Local)

- Python 3.6+
- PyAutoGUI package
- Chrome or Brave browser (optional, will use default browser if not found)

## Running Locally

1. Install requirements:
   ```
   pip install -r requirements.txt
   ```

2. Run the script:
   ```
   python auto_clicker.py
   ```

3. Press `Ctrl+C` to stop the script at any time

## Running with Docker

### Using Docker Compose (Recommended)

1. Build and run the container:
   ```
   docker-compose up --build
   ```

2. To stop:
   ```
   docker-compose down
   ```

### Using Docker directly

1. Build the Docker image:
   ```
   docker build -t auto-clicker .
   ```

2. Run the container:
   ```
   docker run --rm auto-clicker
   ```

## Configuration

Edit the `auto_clicker.py` file to customize:
- `WEBSITES` list to change which websites are randomly opened
- Modify the weights in `random.choices()` to adjust the probability of different actions
- Change the `hours` variable in `main()` to adjust the total runtime
- Adjust the wait time range in `random.uniform(5, 15)` to change the delay between actions

## How it Works

1. The script runs for a specified duration (default: 1 hour)
2. Every 5-15 seconds, it performs a random action:
   - 40% chance: Click at a random screen position
   - 40% chance: Scroll at a random screen position
   - 20% chance: Open a random website
3. Websites remain open for at least 2% of the total runtime (72 seconds for 1 hour)
4. All websites are closed when the script ends 