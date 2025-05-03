# Micro-Manage-Killer

A sophisticated auto-clicker tool designed to simulate human-like computer interactions to help combat aggressive micro-management monitoring systems. This tool simulates natural user behavior including mouse movements, clicks, scrolling, keyboard inputs, and web browsing.

## Features

- Random mouse movements and clicks
- Natural scrolling patterns
- Keyboard input simulation
- Web browsing simulation
- Configurable action weights
- Randomized wait times between actions
- Multiple browser support (Chrome, Brave, Edge)

## Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- uv (Astral Python package manager) [https://docs.astral.sh/uv/]

### Windows Setup

```bash
# Install Python from https://www.python.org/downloads/
python -m pip install --upgrade pip
pip install -r requirements.txt
```
or
```bash
uv sync
```

### Linux Setup

```bash
# Install required packages
sudo apt-get update
sudo apt-get install -y python3-pip python3-xlib xvfb
pip3 install -r requirements.txt
```

### macOS Setup

```bash
# Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python and required packages
brew install python3
pip3 install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root with the following parameters:

```env
# Duration Settings
AUTO_CLICKER_HOURS=2                    # How long the script should run (in hours)
AUTO_CLICKER_MIN_WAIT_TIME=5            # Minimum wait time between actions (seconds)
AUTO_CLICKER_MAX_WAIT_TIME=15           # Maximum wait time between actions (seconds)

# Action Weights (must sum to 1.0)
AUTO_CLICKER_CLICK_WEIGHT=0.20          # Probability of mouse clicks
AUTO_CLICKER_SCROLL_WEIGHT=0.20         # Probability of scroll actions
AUTO_CLICKER_WEBSITE_WEIGHT=0.20        # Probability of website interactions
AUTO_PRESS_KEYBOARD_WEIGHT=0.20         # Probability of keyboard actions
OTHER_WEIGHT=0.05                       # Probability of other actions (movement, etc.)

# Browser Paths (Windows example)
CHROME_PATH=C:\Program Files\Google\Chrome\Application\chrome.exe
BRAVE_PATH=C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe
EDGE_PATH=C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe

# Websites to visit (comma-separated)
WEBSITES=https://www.google.com,https://www.github.com,https://www.stackoverflow.com
```

### Recommended Weight Configurations

Different scenarios require different action weights. Here are some recommended configurations:

#### Development Work Simulation
```env
AUTO_CLICKER_CLICK_WEIGHT=0.20
AUTO_CLICKER_SCROLL_WEIGHT=0.40
AUTO_CLICKER_WEBSITE_WEIGHT=0.20
AUTO_PRESS_KEYBOARD_WEIGHT=0.20
```

#### Research/Reading Simulation
```env
AUTO_CLICKER_CLICK_WEIGHT=0.10
AUTO_CLICKER_SCROLL_WEIGHT=0.50
AUTO_CLICKER_WEBSITE_WEIGHT=0.30
AUTO_PRESS_KEYBOARD_WEIGHT=0.10
```

#### Data Entry Simulation
```env
AUTO_CLICKER_CLICK_WEIGHT=0.30
AUTO_CLICKER_SCROLL_WEIGHT=0.20
AUTO_CLICKER_WEBSITE_WEIGHT=0.10
AUTO_PRESS_KEYBOARD_WEIGHT=0.40
```

## Usage

```bash
python auto_clicker.py
```

The script will:
1. Load configuration from `.env`
2. Display current settings
3. Begin simulating user activity
4. Run for the specified duration
5. Can be stopped at any time with Ctrl+C

## Monitoring Output

The script provides detailed logging of its activities:
- Action weights and configurations
- Runtime duration
- Website visit patterns
- Activity summaries

## Safety Features

- Random delays between actions
- Natural movement patterns
- Varied action sequences
- Browser tab management
- Automatic cleanup on exit

## Troubleshooting

### Linux Display Issues
If you encounter X11 display errors:
```bash
export DISPLAY=:0
xhost +
```

### Windows Permission Issues
Run the script as administrator if browser automation fails.

### macOS Security
Allow Python and your browsers in System Preferences > Security & Privacy.

## Disclaimer

This tool is designed for educational purposes and testing system resilience. Users are responsible for complying with their organization's policies and applicable laws.

## Contributing

Contributions are welcome! Please feel free to submit pull requests.

## License

MIT License - See LICENSE file for details 