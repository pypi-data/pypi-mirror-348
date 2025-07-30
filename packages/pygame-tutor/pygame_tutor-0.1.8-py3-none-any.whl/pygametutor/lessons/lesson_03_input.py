#!/usr/bin/env python
# Pygame Tutor - Educational Platform by Sergey Samoylov
# LICENCE: GNU General Public License v3.0
# Source: https://github.com/sergey-samoylov/pygame-tutor

import pygame
import random

from typing import Dict, Tuple

from pygametutor.core.base import BaseLesson
from pygametutor.settings.constants import COLORS, FONT_NAME

class Lesson03Input(BaseLesson):
    """Dramatic Key Detection with Visual Feedback"""

    def __init__(self, screen_geo):
        super().__init__(screen_geo)
        self.title = "Key Detection Lab"

        # Key display system
        self.active_key = None
        self.key_display_time = 0
        self.display_duration = 1.0  # seconds
        self.key_font = pygame.font.SysFont(FONT_NAME, 120, bold=True)
        self.code_font = pygame.font.SysFont("DejaVu Sans Mono", 30)

        # Help text
        self.help_text = [
            "Press any key to see dramatic feedback",
            "Key detection stops when code is visible (S)"
        ]

    def handle_events(self, event: pygame.event.Event) -> bool:
        # Always let base handle code view toggle first
        handled = super().handle_events(event)

        # Ignore key detection when code is visible
        if self.code_viewer.show_code:
            return handled

        if event.type == pygame.KEYDOWN:
            # Don't capture navigation keys
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_q):
                return handled

            self.active_key = {
                'name': pygame.key.name(event.key).upper(),
                'code': f"pygame.K_{pygame.key.name(event.key)}",
                'color': self._random_bright_color(),
                'time': pygame.time.get_ticks()
            }
            handled = True

        return handled

    def _random_bright_color(self) -> Tuple[int, int, int]:
        """Generate a random bright color from Tokyo Night palette variants"""
        variants = [
            COLORS["Blue"],
            COLORS["Orange"],
            COLORS["Green"],
            COLORS["Purple"],
            COLORS["Pink"],
        ]
        return random.choice(variants)

    def update(self, dt: float) -> bool:
        super().update(dt)

        # Clear key display after duration
        if self.active_key and not self.code_viewer.show_code:
            elapsed = (pygame.time.get_ticks() - self.active_key['time']) / 1000
            if elapsed >= self.display_duration:
                self.active_key = None

        return False

    def draw(self) -> None:
        super().draw()  # Draw base elements

        # Draw help text when no key is active
        if not self.active_key and not self.code_viewer.show_code:
            font = pygame.font.SysFont(FONT_NAME, 24)
            for i, line in enumerate(self.help_text):
                text = font.render(line, True, COLORS["text"])
                self.screen.blit(text, (50, 120 + i * 30))

        # Draw active key effect
        if self.active_key and not self.code_viewer.show_code:
            self._draw_key_effect()

        # Draw implementation hint
        if not self.code_viewer.show_code:
            self._draw_detection_hint()

    def _draw_key_effect(self):
        """Draw the dramatic key press effect with proper animations"""
        # Calculate animation progress (0.0 to 1.0)
        elapsed_ms = pygame.time.get_ticks() - self.active_key['time']
        progress = min(elapsed_ms / (self.display_duration * 1000), 1.0)

        # Create key surface
        key_surf = self.key_font.render(
            self.active_key['name'],
            True,
            self.active_key['color']
        )

        # Center the key display using screen_geo
        key_rect = key_surf.get_rect(center=(self.center_x, self.center_y - 50))

        # Draw key character
        self.screen.blit(key_surf, key_rect)

        # Draw key code below
        code_surf = self.code_font.render(
            self.active_key['code'],
            True,
            COLORS["text"]
        )
        code_rect = code_surf.get_rect(center=(self.center_x, self.center_y + 80))
        self.screen.blit(code_surf, code_rect)

        # Fade out effect (last 30% of duration)
        if progress > 0.7:
            alpha = int(255 * (1 - (progress - 0.7) / 0.3))
            fade_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            fade_surf.fill((*COLORS["background"][:3], alpha))
            self.screen.blit(fade_surf, (0, 0))

    def _draw_detection_hint(self):
        """Draw key detection implementation hint"""
        hint_lines = [
            "Key Detection Implementation:",
            "1. Check event.type == pygame.KEYDOWN",
            "2. Get key name: pygame.key.name(event.key)",
            "3. Get key constant: pygame.K_<key>"
        ]

        font = pygame.font.SysFont(FONT_NAME, 22)
        y_pos = self.height - 180

        for i, line in enumerate(hint_lines):
            color = COLORS["accent"] if i == 0 else COLORS["text"]
            text = font.render(line, True, color)
            self.screen.blit(text, (50, y_pos + i * 30))
