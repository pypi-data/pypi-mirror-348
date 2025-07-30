#!/usr/bin/env python
# Pygame Tutor - Educational Platform by Sergey Samoylov
# LICENCE: GNU General Public License v3.0
# Source: https://github.com/sergey-samoylov/pygame-tutor

import inspect
import pygame

from typing import Type, Any

from pygametutor.core.screen import ScreenGeometry
from pygametutor.settings.constants import COLORS


class CodeViewer:
    """A component for displaying and navigating through source code.

    Provides functionality to:
    - Load Python source code from class objects
    - Display code with syntax highlighting
    - Scroll through code with keyboard controls
    - Toggle visibility with a hotkey

    Attributes:
        screen_geo (ScreenGeometry): Screen geometry handler.
        width (int): Screen width in pixels.
        height (int): Screen height in pixels.
        show_code (bool): Whether the code viewer is currently visible.
        code_scroll (int): Current scroll position in lines.
        code_lines (list[str]): Loaded source code lines.
        code_font (pygame.font.Font): Font used for code display.
        visible_lines (int): Number of lines visible at once.
        line_height (int): Height of each line in pixels.
        code_surface (pygame.Surface): Rendered code surface.
        scroll_step (int): Number of lines to scroll per action.
        scroll_repeat_delay (int): Delay before scroll repeats (ms).
        last_scroll_time (int): Timestamp of last scroll action.
        scroll_direction (int): Current scroll direction (-1, 0, 1).
    """

    def __init__(self, screen_geo: ScreenGeometry):
        """Initialize code viewer with screen geometry.

        Args:
            screen_geo (ScreenGeometry): Contains screen dimensions and surface.
        """
        self.screen_geo = screen_geo
        self.width = screen_geo.width
        self.height = screen_geo.height

        # Viewer state
        self.show_code = False
        self.code_scroll = 0
        self.code_lines = []

        # Display settings
        self.code_font = pygame.font.SysFont("DejaVu Sans Mono", 20)
        self.visible_lines = 15
        self.line_height = 24
        self.code_surface = None

        # Scrolling behavior
        self.scroll_step = 3  # Lines per scroll
        self.scroll_repeat_delay = 300  # ms
        self.last_scroll_time = 0
        self.scroll_direction = 0  # 0=stopped, 1=down, -1=up

    def load_source(self, class_obj: Type) -> None:
        """Load source code from a class object.

        Args:
            class_obj (Type): The class object to extract source code from.
        """
        self.code_lines = inspect.getsource(class_obj).splitlines()
        self._generate_surface()

    def _generate_surface(self) -> None:
        """Generate the code surface with syntax highlighting.

        Creates a surface with the visible portion of code, applying:
        - Line fading at edges
        - Syntax highlighting rules
        - Proper line spacing
        """
        surface_height = self.visible_lines * self.line_height
        self.code_surface = pygame.Surface(
            (self.width - 100, surface_height),
            pygame.SRCALPHA
        )

        for i in range(self.visible_lines):
            if i + self.code_scroll >= len(self.code_lines):
                break

            # Calculate line alpha (fade at edges)
            alpha = 255
            pos_ratio = i / self.visible_lines
            if pos_ratio < 0.2:
                alpha = int(255 * (pos_ratio / 0.2))
            elif pos_ratio > 0.8:
                alpha = int(255 * ((1 - pos_ratio) / 0.2))

            line = self.code_lines[i + self.code_scroll]

            # Syntax highlighting rules
            color = (*COLORS["text"], alpha)
            if line.strip().startswith(("def ", "class ")):
                color = (*COLORS["accent"], alpha)
            elif any(kw in line for kw in ["if ", "else:", "for ", "while "]):
                color = (*COLORS["Blue"], alpha)
            elif line.strip().startswith(('"""', "'''")):
                color = (*COLORS["Purple"], alpha)
            elif "#" in line:
                color = (*COLORS["highlight"], alpha)
            elif any(op in line for op in ["=", "+=", "-=", "=="]):
                color = (*COLORS["Green"], alpha)

            text = self.code_font.render(line, True, color)
            self.code_surface.blit(text, (10, i * self.line_height))

    def handle_events(self, event: pygame.event.Event) -> bool:
        """Handle keyboard events for code viewer.

        Args:
            event (pygame.event.Event): The event to handle.

        Returns:
            bool: True if the event was handled, False otherwise.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                self.show_code = not self.show_code
                return True
            elif self.show_code:
                if event.key == pygame.K_j:
                    self._scroll(self.scroll_step)
                    self.scroll_direction = 1
                    self.last_scroll_time = pygame.time.get_ticks()
                    return True
                elif event.key == pygame.K_k:
                    self._scroll(-self.scroll_step)
                    self.scroll_direction = -1
                    self.last_scroll_time = pygame.time.get_ticks()
                    return True
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_j, pygame.K_k):
                self.scroll_direction = 0
                return True
        return False

    def update(self) -> None:
        """Handle continuous scrolling when keys are held down.

        Should be called from the main game loop to enable smooth scrolling.
        """
        if (self.scroll_direction and
                pygame.time.get_ticks() - self.last_scroll_time >
                self.scroll_repeat_delay):
            self._scroll(self.scroll_direction)
            self.last_scroll_time = pygame.time.get_ticks()

    def _scroll(self, lines: int) -> None:
        """Internal scroll handler with boundary checking.

        Args:
            lines (int): Number of lines to scroll (positive or negative).
        """
        self.code_scroll = max(0, min(
            self.code_scroll + lines,
            len(self.code_lines) - self.visible_lines
        ))
        self._generate_surface()

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the code viewer interface.

        Args:
            screen (pygame.Surface): The target surface to draw on.
        """
        if not self.show_code:
            return

        # Constants for layout
        container_width = self.width - 100
        container_height = 400
        container_y = self.screen_geo.center_y - container_height // 2

        # Semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((*COLORS["background"][:3], 200))
        screen.blit(overlay, (0, 0))

        # Code container
        container = pygame.Rect(
            50,  # Left margin
            container_y,
            container_width,
            container_height
        )
        pygame.draw.rect(screen, (*COLORS["background"][:3], 230), container,
                         0, 10)
        pygame.draw.rect(screen, COLORS["accent"], container, 2, 10)

        # Code content
        code_y = container_y + 20  # Top padding
        screen.blit(self.code_surface, (60, code_y))

        # Footer info
        font = pygame.font.SysFont("DejaVu Sans", 20)
        info_text = (f"Lines {self.code_scroll+1}-"
                     f"{min(self.code_scroll+self.visible_lines, len(self.code_lines))} "
                     f"of {len(self.code_lines)}")
        info = font.render(info_text, True, COLORS["text"])
        screen.blit(info, (60, container_y + container_height + 30))
