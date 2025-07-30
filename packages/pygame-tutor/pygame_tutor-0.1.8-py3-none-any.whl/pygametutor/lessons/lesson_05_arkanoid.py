#!/usr/bin/env python
# Pygame Tutor - Educational Platform by Sergey Samoylov
# LICENCE: GNU General Public License v3.0
# Source: https://github.com/sergey-samoylov/pygame-tutor

import pygame

from pathlib import Path
from typing import List, Tuple

from pygametutor.core.base import BaseLesson
from pygametutor.settings.constants import COLORS, FONT_NAME


class Lesson05Arkanoid(BaseLesson):
    """Classic Arkanoid game demonstrating platform integration.

    This lesson teaches:
    - Rect-based collision detection
    - Game state management
    - Velocity vectors
    - Event handling patterns
    - Image loading with fallbacks

    Controls:
    - h: Move platform left
    - l: Move platform right
    - Mouse: Direct platform control
    - SPACE: Restart game
    """

    def __init__(self, screen_geo):
        """Initialize the Arkanoid game lesson.

        Args:
            screen_geo (ScreenGeometry): Screen geometry handler.
        """
        super().__init__(screen_geo)
        self.title = "Classic Arkanoid"

        # Load game assets
        self._load_assets()

        # Initialize game state
        self._reset_game()

        # Educational content
        self.concepts = [
            "CONTROLS:",
            "h: Move left",
            "l: Move right",
            "Mouse: Direct control",
            "SPACE: Restart game",
            "",
            "GAME CONCEPTS:",
            "• Collision detection",
            "• Velocity vectors",
            "• Event handling"
        ]

    def _load_assets(self):
        """Load game images and initialize game area."""
        img_dir = Path(__file__).parent / "img"
        self.platform_img = self._load_image("platform.png", (100, 30))
        self.ball_img = self._load_image("ball.png", (50, 50))
        self.enemy_img = self._load_image("enemy.png", (50, 50))

        # Game area (original size, centered)
        self.game_width = 500
        self.game_height = 500
        self.game_rect = pygame.Rect(
            self.center_x - self.game_width // 2,
            self.center_y - self.game_height // 2 + 50,  # Slightly lower
            self.game_width,
            self.game_height
        )

    def _load_image(self, filename, size):
        """Load image with fallback to colored rectangle.

        Args:
            filename (str): Image filename to load.
            size (tuple): Target size as (width, height).

        Returns:
            pygame.Surface: Loaded or generated surface.
        """
        try:
            img = pygame.image.load(str(Path(__file__).parent / "img" / filename))
            return pygame.transform.scale(img, size)
        except:
            surf = pygame.Surface(size)
            surf.fill(COLORS["highlight"])
            return surf

    def _reset_game(self):
        """Reset game to initial state."""
        self.platform = pygame.Rect(
            self.game_rect.x + 200,
            self.game_rect.y + 430,  # Bottom area
            100, 30
        )
        self.ball = pygame.Rect(
            self.game_rect.x + 225,
            self.game_rect.y + 400,
            50, 50
        )
        self.ball_speed = [3, -3]  # Start moving up
        self._create_enemies()
        self.game_over = False
        self.victory = False
        self.move_left = False
        self.move_right = False

    def _create_enemies(self):
        """Create enemy pattern using triangular layout."""
        self.enemies = []
        for row in range(3):
            y = self.game_rect.y + 5 + row * 55
            count = 9 - row  # Decreasing pattern
            start_x = self.game_rect.x + 5 + 27.5 * row
            for i in range(count):
                x = start_x + i * 55
                self.enemies.append(pygame.Rect(x, y, 50, 50))

    def handle_events(self, event: pygame.event.Event) -> bool:
        """Handle game-specific events.

        Args:
            event (pygame.event.Event): The event to handle.

        Returns:
            bool: True if event was handled, False otherwise.
        """
        handled = super().handle_events(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                self.move_left = True
                handled = True
            elif event.key == pygame.K_l:
                self.move_right = True
                handled = True
            elif event.key == pygame.K_SPACE and self.game_over:
                self._reset_game()
                handled = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_h:
                self.move_left = False
                handled = True
            elif event.key == pygame.K_l:
                self.move_right = False
                handled = True

        elif event.type == pygame.MOUSEMOTION:
            if not self.game_over:
                mouse_x = event.pos[0] - 50  # Center on paddle
                self.platform.x = max(
                    self.game_rect.left,
                    min(mouse_x, self.game_rect.right - 100)
                )

        return handled

    def update(self, dt: float) -> bool:
        """Update game state.

        Args:
            dt (float): Delta time since last update.

        Returns:
            bool: True if screen needs redraw, False otherwise.
        """
        if self.game_over or self.code_viewer.show_code:
            return False

        self._update_platform()
        self._update_ball()
        self._check_collisions()

        return False

    def _update_platform(self):
        """Update platform position based on input."""
        if self.move_left:
            self.platform.x = max(self.game_rect.left, self.platform.x - 5)
        if self.move_right:
            self.platform.x = min(self.game_rect.right - 100, self.platform.x + 5)

    def _update_ball(self):
        """Update ball position and handle wall collisions."""
        self.ball.x += self.ball_speed[0]
        self.ball.y += self.ball_speed[1]

        # Wall collisions
        if (self.ball.left <= self.game_rect.left or
                self.ball.right >= self.game_rect.right):
            self.ball_speed[0] *= -1
        if self.ball.top <= self.game_rect.top:
            self.ball_speed[1] *= -1

    def _check_collisions(self):
        """Check and handle all game collisions."""
        # Platform collision
        if self.ball.colliderect(self.platform):
            self.ball_speed[1] = -abs(self.ball_speed[1])  # Always bounce up

        # Enemy collisions
        for enemy in self.enemies[:]:
            if self.ball.colliderect(enemy):
                self.enemies.remove(enemy)
                self.ball_speed[1] *= -1
                break

        # Game over conditions
        if self.ball.top > self.game_rect.bottom:
            self.game_over = True
            self.victory = False
        elif not self.enemies:
            self.game_over = True
            self.victory = True

    def draw(self) -> None:
        """Draw all game elements."""
        super().draw()  # Draw base elements

        if self.code_viewer.show_code:
            return

        self._draw_game_area()
        self._draw_game_elements()
        self._draw_game_state()

    def _draw_game_area(self):
        """Draw game boundary and background."""
        pygame.draw.rect(self.screen, COLORS["text"], self.game_rect, 2)

    def _draw_game_elements(self):
        """Draw all game objects (enemies, platform, ball)."""
        # Draw enemies
        for enemy in self.enemies:
            self.screen.blit(self.enemy_img, enemy)

        # Draw platform and ball
        self.screen.blit(self.platform_img, self.platform)
        self.screen.blit(self.ball_img, self.ball)

    def _draw_game_state(self):
        """Draw game state information and controls."""
        # Draw control hints
        if not self.code_viewer.show_code:
            self._draw_controls_hint()

        # Game over message
        if self.game_over:
            msg = "VICTORY!" if self.victory else "GAME OVER"
            color = COLORS["Green"] if self.victory else COLORS["Purple"]
            text = pygame.font.SysFont(FONT_NAME, 50).render(msg, True, color)
            self.screen.blit(
                text,
                (self.center_x - text.get_width() // 2,
                 self.center_y - text.get_height() // 2)
            )
            restart = pygame.font.SysFont(FONT_NAME, 24).render(
                "Press SPACE to restart", True, COLORS["text"])
            self.screen.blit(
                restart,
                (self.center_x - restart.get_width() // 2,
                 self.center_y + 40)
            )

    def _draw_controls_hint(self):
        """Draw control hints at bottom of screen."""
        hint_lines = [
            "Vim-Key Controls:",
            "1. h - to move LEFT",
            "2. l - to move RIGHT",
            "3. Space - to resume game at the end"
        ]

        font = pygame.font.SysFont(FONT_NAME, 22)
        y_pos = self.height - 180

        for i, line in enumerate(hint_lines):
            color = COLORS["accent"] if i == 0 else COLORS["text"]
            text = font.render(line, True, color)
            self.screen.blit(text, (50, y_pos + i * 30))
