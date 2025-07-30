#!/usr/bin/env python
# pygame-tutor - Pure Pygame Educational Platform by Sergey Samoylov
# LICENCE: GNU General Public License v3.0
# Source: https://github.com/sergey-samoylov/pygame-tutor

from pathlib import Path

# Colors (Tokyo Night palette)
COLORS = {
    "background": (26, 27, 38),    # Dark blue-gray
    "text": (192, 202, 245),       # gray
    "highlight": (125, 207, 255),  # blue
    "accent": (158, 206, 106),     # green
    "warning": (255, 121, 198),    # pink
    "Pink": (255, 121, 198),
    "Purple": (204, 153, 255), 
    "Green": (158, 206, 106),
    "Orange": (255, 179, 0),
    "Blue": (125, 207, 255),
}

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
LESSONS_DIR = PROJECT_ROOT / "lessons"

# Display
DEFAULT_TITLE = "Pygame Tutor"
FONT_NAME = "DejaVu Sans"

# Used in 00 lesson and maybe other lessons (navigation for example)
NODE_CONTENT = {
    "about": {
        "title": "What is this?",
        "content": [
            "An interactive playground",
            "for learning Pygame",
            "through visual examples",
            "and live code exploration"
        ]
    },
    "create": {
        "title": "Create Lessons",
        "content": [
            "1. Make lesson_XX_name.py",
            "2. Class must be LessonXXName",
            "3. Implement required methods",
            "4. Inherit from BaseLesson"
        ]
    },
    "navigation": {
        "title": "Navigation",
        "content": [
            "← → : Move between lessons",
            "S : Toggle code view",
            "Q : Quit application"
        ]
    }
}
