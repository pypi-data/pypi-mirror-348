#!/usr/bin/env python
# Pygame Tutor - Educational Platform by Sergey Samoylov
# LICENCE: GNU General Public License v3.0
# Source: https://github.com/sergey-samoylov/pygame-tutor

import math
import pygame
import random

from typing import List, Dict

from pygametutor.core.base import BaseLesson
from pygametutor.settings.constants import COLORS, FONT_NAME

class Lesson02Physics(BaseLesson):
    """Interactive Physics Playground - Balls, Gravity, and Collisions"""

    def __init__(self, screen_geo):
        super().__init__(screen_geo)
        self.title = "Physics Playground"

        # Physics properties (editable with keys)
        self.gravity = 0.5
        self.elasticity = 0.8
        self.balls: List[Dict] = []

        # Educational content
        self.concepts = [
            "PHYSICS CONTROLS:",
            "G: Gravity (Current: {:.1f})".format(self.gravity),
            "E: Elasticity (Current: {:.0%})".format(self.elasticity),
            "SPACE: Reset simulation",
            "CLICK: Add new ball",
            "",
            "PHYSICS CONCEPTS:",
            "• Conservation of momentum",
            "• Elastic collisions",
            "• Gravity acceleration"
        ]

        # Initialize with 3 balls
        for _ in range(3):
            self._add_ball()

    def _add_ball(self):
        """Create a new physics ball with random properties"""
        radius = random.randint(15, 35)
        self.balls.append({
            'x': random.randint(radius, self.width - radius),
            'y': random.randint(radius, self.geo.third_y),  # Use screen_geo's third_y
            'radius': radius,
            'dx': random.uniform(-4, 4),
            'dy': random.uniform(-3, 0),
            'color': random.choice([
                COLORS["highlight"],
                (255, 179, 0),  # Orange
                (158, 206, 106), # Green
                (204, 153, 255)  # Purple
            ]),
            'trail': []
        })

    def handle_events(self, event: pygame.event.Event) -> bool:
        handled = super().handle_events(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            self._add_ball()
            handled = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Reset
                self.balls.clear()
                for _ in range(3):
                    self._add_ball()
                handled = True
            elif event.key == pygame.K_g:  # Adjust gravity
                self.gravity = (self.gravity + 0.1) % 2.0
                self.concepts[1] = "G: Gravity (Current: {:.1f})".format(self.gravity)
                handled = True
            elif event.key == pygame.K_e:  # Adjust elasticity
                self.elasticity = (self.elasticity + 0.1) % 1.1
                self.concepts[2] = "E: Elasticity (Current: {:.0%})".format(self.elasticity)
                handled = True

        return handled

    def update(self, dt: float) -> bool:
        super().update(dt)

        # Update each ball's physics
        for ball in self.balls:
            # Apply forces
            ball['dy'] += self.gravity

            # Update position
            ball['x'] += ball['dx']
            ball['y'] += ball['dy']

            # Store trail (max 10 points)
            ball['trail'].append((ball['x'], ball['y']))
            if len(ball['trail']) > 10:
                ball['trail'].pop(0)

            # Wall collisions
            if ball['x'] - ball['radius'] < 0:
                ball['x'] = ball['radius']
                ball['dx'] = -ball['dx'] * self.elasticity
            elif ball['x'] + ball['radius'] > self.width:
                ball['x'] = self.width - ball['radius']
                ball['dx'] = -ball['dx'] * self.elasticity

            if ball['y'] - ball['radius'] < 0:
                ball['y'] = ball['radius']
                ball['dy'] = -ball['dy'] * self.elasticity
            elif ball['y'] + ball['radius'] > self.height:
                ball['y'] = self.height - ball['radius']
                ball['dy'] = -ball['dy'] * self.elasticity

        # Ball-to-ball collisions
        for i, b1 in enumerate(self.balls):
            for b2 in self.balls[i+1:]:
                dx = b2['x'] - b1['x']
                dy = b2['y'] - b1['y']
                distance = math.hypot(dx, dy)

                if distance < b1['radius'] + b2['radius']:
                    # Collision resolution
                    angle = math.atan2(dy, dx)
                    overlap = (b1['radius'] + b2['radius'] - distance) / 2

                    # Repel balls
                    b1['x'] -= overlap * math.cos(angle)
                    b1['y'] -= overlap * math.sin(angle)
                    b2['x'] += overlap * math.cos(angle)
                    b2['y'] += overlap * math.sin(angle)

                    # Swap velocities (simplified physics)
                    b1['dx'], b2['dx'] = b2['dx'], b1['dx']
                    b1['dy'], b2['dy'] = b2['dy'], b1['dy']

        return False

    def draw(self) -> None:
        super().draw()  # Base draws background and code viewer

        if self.code_viewer.show_code:
            return

        # Draw educational panel
        self._draw_physics_info()

        # Draw trails
        for ball in self.balls:
            for i, (x, y) in enumerate(ball['trail']):
                alpha = int(255 * (i / len(ball['trail'])))
                radius = int(ball['radius'] * (i / len(ball['trail'])))

                trail_surf = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
                color = (*ball['color'], alpha)
                pygame.draw.circle(trail_surf, color, (radius, radius), radius)
                self.screen.blit(trail_surf, (x - radius, y - radius))

        # Draw balls
        for ball in self.balls:
            pygame.draw.circle(
                self.screen,
                ball['color'],
                (int(ball['x']), int(ball['y'])),
                ball['radius']
            )

    def _draw_physics_info(self):
        """Draw physics info panel with proper layering and color coding"""
        panel_width = 350
        panel_height = 300
        panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)

        # Background with 85% opacity
        panel.fill((*COLORS["background"][:3], 217))  # 85% of 255

        font = pygame.font.SysFont(FONT_NAME, 22)

        # Organized content with different colors
        sections = [
            {
                "title": "PHYSICS CONTROLS:",
                "items": [
                    ("G", "Gravity (Current: {:.1f})".format(self.gravity)),
                    ("E", "Elasticity (Current: {:.0%})".format(self.elasticity)),
                    ("SPACE", "Reset simulation"),
                    ("CLICK", "Add new ball")
                ]
            },
            {
                "title": "PHYSICS CONCEPTS:",
                "items": [
                    "Conservation of momentum",
                    "Elastic collisions",
                    "Gravity acceleration"
                ]
            }
        ]

        y_offset = 15
        for section in sections:
            # Draw section title (green accent)
            title_surf = font.render(section["title"], True, COLORS["accent"])
            panel.blit(title_surf, (15, y_offset))
            y_offset += 30

            for item in section["items"]:
                if isinstance(item, tuple):  # Key-value pair
                    key, text = item
                    # Draw key (yellow highlight)
                    key_surf = font.render(key + ":", True, COLORS["highlight"])
                    panel.blit(key_surf, (25, y_offset))
                    # Draw value (normal text)
                    text_surf = font.render(text, True, COLORS["text"])
                    panel.blit(text_surf, (25 + key_surf.get_width() + 5, y_offset))
                else:  # Plain text item
                    text_surf = font.render("• " + item, True, COLORS["text"])
                    panel.blit(text_surf, (25, y_offset))
                y_offset += 25
            y_offset += 10  # Space between sections

        # Position panel in bottom-left corner using screen_geo
        self.screen.blit(panel, (20, self.height - panel_height - 20))
