#!/usr/bin/env python
# Pygame Tutor - Educational Platform by Sergey Samoylov
# LICENCE: GNU General Public License v3.0
# Source: https://github.com/sergey-samoylov/pygame-tutor

import math
import pygame
import random

from typing import List, Tuple, Dict

from pygametutor.core.base import BaseLesson
from pygametutor.settings.constants import COLORS, FONT_NAME


class Lesson04Breakout(BaseLesson):
    """Interactive Breakout Game Lesson demonstrating collision detection.

    This lesson teaches:
    - Basic game loop implementation
    - Collision detection principles
    - Velocity and bounce physics
    - Game state management
    - Event handling

    Controls Vim-keys:
    - h: Move paddle left
    - l: Move paddle right
    - SPACE: Start/pause game or restart when game over
    """

    def __init__(self, screen_geo):
        """Initialize the Breakout game lesson.

        Args:
            screen_geo (ScreenGeometry): Screen geometry handler.
        """
        super().__init__(screen_geo)
        self.title = "Breakout Game"

        # Initialize game elements
        self._init_game_elements()
        self._create_bricks()

        # Fonts
        self.font_large = pygame.font.SysFont(FONT_NAME, 48)
        self.font_medium = pygame.font.SysFont(FONT_NAME, 32)

        # Help text
        self.help_text = [
            "SPACE: Start/Pause",
            "h: Move left",
            "l: Move right"
        ]

    def _init_game_elements(self):
        """Initialize game elements and state."""
        self.paddle = {
            'width': min(200, self.width // 5),
            'height': 25,
            'x': self.center_x - 100,
            'y': self.height - 100,
            'speed': 8,
            'color': COLORS["Green"]
        }

        self.ball = {
            'x': self.center_x,
            'y': self.center_y + 70,
            'radius': 20,
            'dx': 4 * random.choice([-1, 1]),
            'dy': -4,
            'color': COLORS["Orange"]
        }

        # Brick settings
        self.brick_rows = 5
        self.brick_cols = 10
        self.brick_width = self.width // self.brick_cols - 5
        self.brick_height = 20
        self.bricks: List[Dict] = []

        # Game state
        self.score = 0
        self.lives = 3
        self.game_active = False
        self.key_h_pressed = False
        self.key_l_pressed = False
        self.key_press_time = 0
        self.key_display_duration = 0.5  # seconds

    def _create_bricks(self):
        """Initialize the brick layout with colored rows."""
        brick_colors = [
            COLORS["Pink"],
            COLORS["Purple"],
            COLORS["Green"],
            COLORS["Orange"],
            COLORS["Blue"],
        ]

        start_y = self.geo.relative_y(0.3)  # 30% from top

        for row in range(self.brick_rows):
            for col in range(self.brick_cols):
                self.bricks.append({
                    'x': 5 + col * (self.brick_width + 5),
                    'y': start_y + row * (self.brick_height + 5),
                    'width': self.brick_width,
                    'height': self.brick_height,
                    'color': brick_colors[row],
                    'visible': True
                })

    def handle_events(self, event: pygame.event.Event) -> bool:
        """Handle game-specific events.

        Args:
            event (pygame.event.Event): The event to handle.

        Returns:
            bool: True if event was handled, False otherwise.
        """
        handled = super().handle_events(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self._handle_space_press()
                handled = True
            elif event.key == pygame.K_h:
                self.key_h_pressed = True
                self.key_press_time = pygame.time.get_ticks()
            elif event.key == pygame.K_l:
                self.key_l_pressed = True
                self.key_press_time = pygame.time.get_ticks()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_h:
                self.key_h_pressed = False
            elif event.key == pygame.K_l:
                self.key_l_pressed = False

        return handled

    def _handle_space_press(self):
        """Handle space bar press for game control."""
        if self.lives <= 0:  # Game over - full reset
            self.lives = 3
            self.score = 0
            self._create_bricks()
            self._reset_ball()
            self.game_active = True
        else:  # Regular pause/unpause
            self.game_active = not self.game_active

    def update(self, dt: float) -> bool:
        """Update game state.

        Args:
            dt (float): Delta time since last update.

        Returns:
            bool: True if screen needs redraw, False otherwise.
        """
        if not self.game_active or self.code_viewer.show_code:
            return False

        self._update_paddle()
        self._update_ball()
        self._check_collisions()
        self._update_key_indicators()

        return False

    def _update_paddle(self):
        """Update paddle position based on key states."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_h] and self.paddle['x'] > 0:
            self.paddle['x'] -= self.paddle['speed']
        if keys[pygame.K_l] and self.paddle['x'] < self.width - self.paddle['width']:
            self.paddle['x'] += self.paddle['speed']

    def _update_ball(self):
        """Update ball position and handle wall collisions."""
        self.ball['x'] += self.ball['dx']
        self.ball['y'] += self.ball['dy']

        # Wall collisions
        if (self.ball['x'] <= self.ball['radius'] or
                self.ball['x'] >= self.width - self.ball['radius']):
            self.ball['dx'] *= -1
        if self.ball['y'] <= self.ball['radius']:
            self.ball['dy'] *= -1

        # Bottom boundary (lose life)
        if self.ball['y'] > self.height:
            self.lives -= 1
            if self.lives > 0:
                self._reset_ball()
            else:
                self.game_active = False

    def _check_collisions(self):
        """Check and handle all game collisions."""
        # Paddle collision
        if (self.ball['y'] + self.ball['radius'] >= self.paddle['y'] and
            self.ball['y'] - self.ball['radius'] <= self.paddle['y'] + self.paddle['height'] and
            self.ball['x'] >= self.paddle['x'] and
            self.ball['x'] <= self.paddle['x'] + self.paddle['width']):

            hit_pos = (self.ball['x'] - self.paddle['x']) / self.paddle['width']
            self.ball['dx'] = 5 * (hit_pos - 0.5) * 2
            self.ball['dy'] = -abs(self.ball['dy'])

        # Brick collisions
        for brick in self.bricks:
            if brick['visible'] and self._check_brick_collision(brick):
                brick['visible'] = False
                self.ball['dy'] *= -1
                self.score += 10
                break

        # Level complete
        if all(not brick['visible'] for brick in self.bricks):
            self._create_bricks()
            self._reset_ball()

    def _update_key_indicators(self):
        """Update key press indicator states."""
        current_time = pygame.time.get_ticks()
        if (current_time - self.key_press_time) > (self.key_display_duration * 1000):
            self.key_h_pressed = False
            self.key_l_pressed = False

    def _check_brick_collision(self, brick: Dict) -> bool:
        """Check if ball collides with a brick using circle-rect collision.

        Args:
            brick (Dict): Brick dictionary with position and dimensions.

        Returns:
            bool: True if collision occurred, False otherwise.
        """
        closest_x = max(brick['x'], min(self.ball['x'], brick['x'] + brick['width']))
        closest_y = max(brick['y'], min(self.ball['y'], brick['y'] + brick['height']))

        distance = math.hypot(self.ball['x'] - closest_x, self.ball['y'] - closest_y)
        return distance <= self.ball['radius']

    def _reset_ball(self):
        """Reset ball to starting position with random direction."""
        self.ball.update({
            'x': self.center_x,
            'y': self.center_y,
            'dx': 4 * random.choice([-1, 1]),
            'dy': -4
        })

    def draw(self) -> None:
        """Draw all game elements."""
        super().draw()  # Draw base elements

        if self.code_viewer.show_code:
            return

        self._draw_game_elements()
        self._draw_ui()

    def _draw_game_elements(self):
        """Draw all game objects (bricks, paddle, ball)."""
        # Draw bricks
        for brick in self.bricks:
            if brick['visible']:
                pygame.draw.rect(
                    self.screen,
                    brick['color'],
                    (brick['x'], brick['y'], brick['width'], brick['height'])
                )

        # Draw paddle
        pygame.draw.rect(
            self.screen,
            self.paddle['color'],
            (self.paddle['x'], self.paddle['y'], self.paddle['width'], self.paddle['height'])
        )

        # Draw ball
        pygame.draw.circle(
            self.screen,
            self.ball['color'],
            (int(self.ball['x']), int(self.ball['y'])),
            self.ball['radius']
        )

    def _draw_ui(self):
        """Draw user interface elements (score, controls, messages)."""
        # Draw key indicators
        key_font = pygame.font.SysFont(FONT_NAME, 48, bold=True)
        h_color = COLORS["Purple"] if self.key_h_pressed else COLORS["text"]
        l_color = COLORS["Purple"] if self.key_l_pressed else COLORS["text"]

        self.screen.blit(
            key_font.render("H", True, h_color),
            (20, self.center_y - 24)
        )
        self.screen.blit(
            key_font.render("L", True, l_color),
            (self.width - 40, self.center_y - 24)
        )

        # Draw score and lives
        score_text = self.font_medium.render(f"Score: {self.score}", True, COLORS["text"])
        lives_text = self.font_medium.render(f"Lives: {self.lives}", True, COLORS["text"])
        self.screen.blit(score_text, (50, 210))
        self.screen.blit(lives_text, (self.width - lives_text.get_width() - 50, 210))

        # Draw help text when paused
        if not self.game_active:
            font = pygame.font.SysFont(FONT_NAME, 24)
            for i, line in enumerate(self.help_text):
                text = font.render(line, True, COLORS["text"])
                self.screen.blit(text, (50, 120 + i * 30))

            # Draw start message
            if all(brick['visible'] for brick in self.bricks):
                text = self.font_medium.render("Press SPACE to Start", True, COLORS["highlight"])
            else:
                text = self.font_medium.render("Press SPACE to Continue", True, COLORS["highlight"])
            self.screen.blit(text, (self.center_x - text.get_width()//2, self.center_y))
