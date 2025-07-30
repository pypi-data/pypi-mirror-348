#!/usr/bin/env python
# Pygame Tutor - Educational Platform by Sergey Samoylov
# LICENCE: GNU General Public License v3.0
# Source: https://github.com/sergey-samoylov/pygame-tutor

import importlib

from pathlib import Path
from typing import List, Type

from pygametutor.settings.constants import LESSONS_DIR


def load_lessons() -> List[Type]:
    """Load all available lesson classes from the lessons directory.

    Scans the LESSONS_DIR for Python files matching 'lesson_*.py' pattern,
    imports them, validates properly structured lesson classes.
    Returns a fallback BaseLesson if no valid lessons are found.

    Returns:
        List[Type]: List of loaded lesson classes, or a single BaseLesson
                   if no valid lessons were found.

    Notes:
        - Lesson files must be named 'lesson_*.py'
        - Each lesson class name should be PascalCase version of the filename
          (e.g., 'lesson_basics.py' -> 'LessonBasics')
        - Valid lessons must implement 'draw' and 'handle_events' methods
    """
    lessons = []
    LESSONS_DIR.mkdir(exist_ok=True)

    for lesson_file in sorted(LESSONS_DIR.glob("lesson_*.py")):
        if lesson_file.stem == "__init__":
            continue

        try:
            PACKAGE_ROOT = __package__.split('.')[0]
            module_path = f"{PACKAGE_ROOT}.lessons.{lesson_file.stem}"
            module = importlib.import_module(module_path)
            class_name = "".join(
                part.capitalize()
                for part in lesson_file.stem.split("_")
            )

            if hasattr(module, class_name):
                lesson_class = getattr(module, class_name)
                if all(hasattr(lesson_class, m)
                   for m in ['draw', 'handle_events']):
                    lessons.append(lesson_class)
        except Exception as e:
            print(f"Error loading {lesson_file}: {e}")

    return lessons or [get_fallback_lesson()]


def get_fallback_lesson() -> Type:
    """Get the base lesson class as a fallback when no lessons are available.

    Returns:
        Type: The BaseLesson class from core.base module.
    """
    from pygametutor.core.base import BaseLesson
    return BaseLesson
