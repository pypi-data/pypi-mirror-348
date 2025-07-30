#!/usr/bin/env python
# Pygame Tutor - Educational Platform by Sergey Samoylov
# LICENCE: GNU General Public License v3.0
# Source: https://github.com/sergey-samoylov/pygame-tutor

import pygame
from typing import List, Tuple

from pygametutor.core.base import BaseLesson
from pygametutor.core.screen import ScreenGeometry
from pygametutor.settings.constants import COLORS, FONT_NAME

class Lesson01Comet(BaseLesson):
    """Demonstrates animated comet with color-changing trail"""

    def __init__(self, screen_geo: ScreenGeometry):
        super().__init__(screen_geo)
        self.title = "Cosmic Comet"

        # Comet properties
        self.comet_pos = [screen_geo.quarter_x, screen_geo.center_y]
        self.comet_speed = 5
        self.comet_radius = 25
        self.trail_length = 15
        self.trail = []

        # Color options
        self.colors = [
            COLORS["Blue"],  # Bright blue
            COLORS["Orange"],    # Orange
            COLORS["Green"],     # Light green
            COLORS["Purple"],    # Lavender
            COLORS["Pink"]       # Pink
        ]
        self.current_color = 0

    def handle_events(self, event: pygame.event.Event) -> bool:
        handled = super().handle_events(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self._cycle_color()
            handled = True
        return handled

    def _cycle_color(self) -> None:
        """Cycle through available trail colors"""
        self.current_color = (self.current_color + 1) % len(self.colors)

    def update(self, dt: float) -> bool:
        if self.code_viewer.show_code:
            return False

        self._update_comet_position()
        self._update_trail()
        return False

    def _update_comet_position(self) -> None:
        """Handle comet movement and screen wrapping"""
        self.comet_pos[0] += self.comet_speed

        # Wrap around screen edges
        if self.comet_pos[0] > self.width + self.comet_radius:
            self.comet_pos[0] = -self.comet_radius
            self.comet_pos[1] = self.center_y

    def _update_trail(self) -> None:
        """Maintain comet trail effect"""
        self.trail.append(tuple(self.comet_pos))
        if len(self.trail) > self.trail_length:
            self.trail.pop(0)
    def _draw_control_hint(self):
        """Draw control hints"""
        hint_lines = [
            "Controls:",
            "Space - to change the comet color"
        ]

        font = pygame.font.SysFont(FONT_NAME, 22)
        y_pos = self.height - 180

        for i, line in enumerate(hint_lines):
            color = COLORS["accent"] if i == 0 else COLORS["text"]
            text = font.render(line, True, color)
            self.screen.blit(text, (50, y_pos + i * 30))


    def draw(self) -> None:
        super().draw()  # Draw base lesson elements
        
        if not self.code_viewer.show_code:
            self._draw_control_hint()

        if self.code_viewer.show_code:
            return

        self._draw_trail()
        self._draw_comet()

    def _draw_trail(self) -> None:
        """Render comet trail with fading effect"""
        for i, pos in enumerate(self.trail):
            # Calculate trail segment properties
            alpha = int(255 * (i/len(self.trail)))
            radius = int(self.comet_radius * (i/len(self.trail)))
            color = (*self.colors[self.current_color][:3], alpha)

            # Create trail segment surface
            trail_surf = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            pygame.draw.circle(trail_surf, color, (radius, radius), radius)
            self.screen.blit(trail_surf, (pos[0]-radius, pos[1]-radius))

    def _draw_comet(self) -> None:
        """Draw main comet body"""
        pygame.draw.circle(
            self.screen,
            self.colors[self.current_color],
            (int(self.comet_pos[0]), int(self.comet_pos[1])),
            self.comet_radius
        )
