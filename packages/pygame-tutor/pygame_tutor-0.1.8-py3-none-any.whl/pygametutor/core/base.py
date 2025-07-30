#!/usr/bin/env python
# Pygame Tutor - Educational Platform by Sergey Samoylov
# LICENCE: GNU General Public License v3.0
# Source: https://github.com/sergey-samoylov/pygame-tutor

import pygame

from typing import Any

from pygametutor.core.code_viewer import CodeViewer
from pygametutor.core.screen import ScreenGeometry
from pygametutor.settings.constants import COLORS, FONT_NAME


class BaseLesson:
    """Base class for all lessons in the educational platform.

    Provides common functionality and interface for lessons including:
    - Screen geometry management
    - Code viewer integration
    - Event handling
    - Basic rendering of lesson title and controls

    Attributes:
        screen (pygame.Surface): The main display surface for the lesson.
        geo (ScreenGeometry): Handler for screen geometry calculations.
        width (int): Width of the screen in pixels.
        height (int): Height of the screen in pixels.
        center_x (int): X-coordinate of screen center.
        center_y (int): Y-coordinate of screen center.
        title (str): Title of the lesson displayed at the top left.
        code_viewer (CodeViewer): Component for displaying lesson source code.
        font_title (pygame.font.Font): Large font for lesson title.
        font_regular (pygame.font.Font): Regular font for UI elements.
    """

    def __init__(self, screen_geo: ScreenGeometry):
        """Initialize the base lesson with screen geometry.

        Args:
            screen_geo (ScreenGeometry): Contains screen dimensions and surface.
        """
        self.screen = screen_geo.surface
        self.geo = screen_geo  # Store full geometry handler

        # Common shortcuts
        self.width = screen_geo.width
        self.height = screen_geo.height
        self.center_x = screen_geo.center_x
        self.center_y = screen_geo.center_y

        self.title = "Untitled Lesson"

        self.code_viewer = CodeViewer(self.geo)
        self.code_viewer.load_source(self.__class__)

        self.font_title = pygame.font.SysFont(FONT_NAME, 64)
        self.font_regular = pygame.font.SysFont(FONT_NAME, 24)

    def handle_events(self, event: pygame.event.Event) -> bool:
        """Handle pygame events for the lesson.

        Args:
            event (pygame.event.Event): The event to handle.

        Returns:
            bool: True if the event was handled and should not propagate further.
        """
        return self.code_viewer.handle_events(event)

    def update(self, dt: float) -> bool:
        """Update lesson state.

        Args:
            dt (float): Delta time since last update in seconds.

        Returns:
            bool: True if the lesson state changed and requires redraw.
        """
        return False

    def draw(self):
        """Draw lesson content to the screen.

        Renders:
        - Background
        - Lesson title
        - Control hints (when code viewer is hidden)
        - Code viewer (when visible)
        """
        self.screen.fill(COLORS["background"])
        title = self.font_title.render(self.title, True, COLORS["highlight"])
        self.screen.blit(title, (50, 40))

        if not self.code_viewer.show_code:
            hint = self.font_regular.render(
                "Press S to view code | Arrows to navigate | Q to quit",
                True, COLORS["text"]
            )
            self.screen.blit(hint, (self.width - hint.get_width() - 40, 40))

        self.code_viewer.draw(self.screen)
