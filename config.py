# User-specific configuration
# Copy this file to config_local.py and customize for your setup
# config_local.py is gitignored and won't be committed

# Your Twitter username for the following page URL
TWITTER_USERNAME = "whatsaplat"

# Chrome address bar coordinates on your screen
# To find: Take a screenshot and use a tool to get pixel coordinates
SEARCH_BAR_X = 290
SEARCH_BAR_Y = 81

# Dead space coordinates (area to move mouse when not clicking)
# Should be an empty area of the screen
DEADSPACE_X = 20
DEADSPACE_Y = 500

# Image recognition tolerance (0.0 to 1.0)
# Higher = stricter matching, Lower = more lenient
# Recommended: 0.7 to 0.9
IMAGE_TOLERANCE = 0.8

# Timing settings (in seconds)
SCROLL_DELAY = 0.2  # Delay after scrolling
CLICK_DELAY = 0.0   # Delay between unfollow clicks

# Scrolling settings
SCROLL_PIXELS = 600  # How many pixels to scroll each time

# Duplicate detection tolerance
# Coordinates within this distance (pixels) are considered duplicates
DUPLICATE_TOLERANCE = 50
