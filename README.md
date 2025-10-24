# Twitter Unfollower/Follower Bot

An automated tool for managing Twitter/X followers using image recognition and GUI automation.

## Warning

This tool automates interactions with Twitter/X using GUI automation. Use at your own risk. Automated actions may violate Twitter's Terms of Service and could result in account suspension or termination. The authors are not responsible for any consequences of using this tool.

## Features

- **Unfollow All**: Automatically unfollow all users you're currently following
- **Follow Random**: Follow random users from a list of target profiles
- Uses image recognition to locate UI elements (works across different screen sizes)
- Configurable delays and tolerances

## Requirements

- Python 3.11 or higher
- Google Chrome browser
- Windows, macOS, or Linux

## Installation

### Using Poetry (recommended)

```bash
poetry install
```

### Using pip

```bash
pip install -r requirements.txt
```

## Setup

1. **Configure your settings** in `constants.py`:
   - `SEARCH_BAR_COORD`: Coordinates of Chrome's address bar
   - `BASE_UNFOLLOW_URL`: Your Twitter following page URL
   - `UNFOLLOW_COORD`: Coordinates of the unfollow confirmation button
   - Adjust timing and tolerance values as needed

2. **Add target profiles** (for follow feature):
   - Edit `data/target_profiles.txt`
   - Add one Twitter profile URL per line
   - Example: `https://x.com/username`

3. **Update reference images** (if needed):
   - The tool uses image recognition to find buttons
   - Reference images are in `assets/follow_button_images/` and `assets/unfollow_button_images/`
   - Take new screenshots if your UI looks different

## Usage

### CLI Interface

Unfollow all users:
```bash
python cli.py unfollow
```

Follow random users (specify count):
```bash
python cli.py follow 10
```

### Direct Script Usage

Run unfollow script:
```bash
python unfollow_all.py
```

Run follow script:
```bash
python follow_random.py
```

## Project Structure

```
twitter-unfollower/
├── assets/                      # Reference images for button detection
│   ├── follow_button_images/
│   └── unfollow_button_images/
├── data/                        # Data files
│   └── target_profiles.txt     # List of profiles to follow from
├── chrome.py                    # Chrome browser management
├── cli.py                       # Command-line interface
├── constants.py                 # Configuration constants
├── follow_random.py             # Follow automation logic
├── image_rec.py                 # Image recognition utilities
├── unfollow_all.py              # Unfollow automation logic
├── window.py                    # Window management utilities
├── pyproject.toml               # Poetry configuration
└── README.md                    # This file
```

## How It Works

1. **Chrome Management**: Kills existing Chrome instances and launches a fresh one
2. **Window Focus**: Activates the Chrome window for automation
3. **Image Recognition**: Uses OpenCV template matching to find buttons on screen
4. **GUI Automation**: Uses PyAutoGUI to click buttons and navigate pages
5. **Scrolling**: Automatically scrolls to load more content

## Troubleshooting

### Buttons not detected
- Update reference images in `assets/` folders
- Adjust `IMAGE_REC_TOLERANCE` in `constants.py` (lower = more lenient, higher = stricter)

### Wrong coordinates clicked
- Update coordinate constants in `constants.py`
- Use a screenshot tool to find exact pixel coordinates

### Script running too fast/slow
- Adjust timing constants in `constants.py`:
  - `SCROLL_PAUSE_TIME`
  - `UNFOLLOW_CLICK_TIMEOUT`

## Contributing

Feel free to submit issues and pull requests.

## License

This project is provided as-is for educational purposes.
