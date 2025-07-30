#!/usr/bin/env python
"""Main application module for Pygame Tutor educational platform.

This module handles the main application loop, lesson management, and user input.
It serves as the entry point for the pygame-tutor application.
"""
# Pygame Tutor by Sergey Samoylov
# LICENCE: GNU General Public License v3.0
# Source: https://github.com/sergey-samoylov/pygame-tutor


import pygame
import sys

from typing import List

from pygametutor.core.loader import load_lessons
from pygametutor.core.screen import ScreenGeometry
from pygametutor.settings.constants import COLORS, DEFAULT_TITLE


class Slideshow:
    """Main application class that manages lessons and display.

    Attributes:
        screen_geo (ScreenGeometry): Handles screen geometry calculations
        screen (pygame.Surface): Main display surface
        clock (pygame.time.Clock): Game clock for FPS control
        lessons (List): Loaded lesson classes
        current_lesson_index (int): Index of active lesson
        current_lesson: Currently active lesson instance
    """

    def __init__(self) -> None:
        """Initialize the application with display and lesson loading."""
        pygame.init()
        screen_surface = pygame.display.set_mode(
            (0, 0),
            pygame.FULLSCREEN,
        )
        # Central geometry handler
        self.screen_geo = ScreenGeometry(screen_surface)
        self.screen = self.screen_geo.surface  # Add direct surface reference

        pygame.display.set_caption(DEFAULT_TITLE)

        self.clock = pygame.time.Clock()
        self.lessons: List = load_lessons()
        self.current_lesson_index: int = 0
        self.current_lesson = None
        self.start_lesson(0)

    def start_lesson(self, index: int) -> None:
        """Start a lesson by index.

        Args:
            index: The index of the lesson to start
        """
        if 0 <= index < len(self.lessons):
            self.current_lesson_index = index
            self.current_lesson = self.lessons[index](self.screen_geo)

    def _handle_key(self, key: int) -> bool:
        """Handle keyboard input for application control.

        Args:
            key: The pygame key constant of the pressed key

        Returns:
            bool: True if key was handled, False otherwise
        """
        if key in (pygame.K_q, pygame.K_ESCAPE):
            return False  # Signal to quit
        elif key == pygame.K_RIGHT:
            self.start_lesson(
                (self.current_lesson_index + 1) % len(self.lessons)
            )
        elif key == pygame.K_LEFT:
            self.start_lesson(
                (self.current_lesson_index - 1) % len(self.lessons)
            )
        return True

    def run(self) -> None:
        """Run the main application loop."""
        running = True
        while running:
            dt = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if not self._handle_key(event.key):
                        running = False

                if self.current_lesson:
                    self.current_lesson.handle_events(event)

            if self.current_lesson:
                if self.current_lesson.update(dt):
                    self.start_lesson(
                        (self.current_lesson_index + 1) % len(self.lessons)
                    )
                self.current_lesson.draw()
                self._draw_nav_dots()

            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def _draw_nav_dots(self) -> None:
        """Draw navigation dots indicating current lesson position.

        The dots are centered at the bottom of the screen,
        with the current lesson's dot highlighted.
        """
        dot_radius = 8
        spacing = 20
        start_x = self.screen_geo.center_x - (len(self.lessons) * spacing) // 2

        for i in range(len(self.lessons)):
            color = (
                COLORS["Green"]
                if i == self.current_lesson_index
                else COLORS["text"]
            )
            pygame.draw.circle(
                self.screen,
                color,
                (start_x + i * spacing, self.screen_geo.height - 30),
                (dot_radius
                 if i == self.current_lesson_index
                 else dot_radius - 2)
            )

def main():
    """Entry point for pygame-tutor command."""
    app = Slideshow()
    app.run()

if __name__ == "__main__":
    main()

