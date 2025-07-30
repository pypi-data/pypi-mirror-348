#!/usr/bin/env python
# Pygame Tutor - Educational Platform by Sergey Samoylov
# LICENCE: GNU General Public License v3.0
# Source: https://github.com/sergey-samoylov/pygame-tutor

import math
import pygame
import random

from typing import List, Dict

from pygametutor.core.base import BaseLesson
from pygametutor.core.screen import ScreenGeometry
from pygametutor.settings.constants import COLORS, FONT_NAME, NODE_CONTENT

class Lesson00About(BaseLesson):
    """Cosmic Information Explorer - Interactive About Page"""

    def __init__(self, screen_geo: ScreenGeometry):
        super().__init__(screen_geo)
        self.title = "Pygame Tutor Explorer"

        # Setup visual elements
        self._init_nodes()
        self._init_player()
        self._init_effects()

    def _init_nodes(self):
        """Initialize the interactive nodes"""
        self.nodes = [
            {
                'x': self.geo.relative_x(0.3),
                'y': self.geo.relative_y(0.3),
                'radius': 40,
                'color': COLORS["Blue"],
                'title': NODE_CONTENT["about"]["title"],
                'content': "\n".join(NODE_CONTENT["about"]["content"]),
                'discovered': False,
                'show_title': False,
                'title_alpha': 0
            },
            {
                'x': self.geo.relative_x(0.7),
                'y': self.geo.relative_y(0.4),
                'radius': 50,
                'color': COLORS["Pink"],
                'title': NODE_CONTENT["create"]["title"],
                'content': "\n".join(NODE_CONTENT["create"]["content"]),
                'discovered': False,
                'show_title': False,
                'title_alpha': 0
            },
            {
                'x': self.geo.relative_x(0.5),
                'y': self.geo.relative_y(0.7),
                'radius': 45,
                'color': COLORS["Green"],
                'title': NODE_CONTENT["navigation"]["title"],
                'content': "\n".join(NODE_CONTENT["navigation"]["content"]),
                'discovered': False,
                'show_title': False,
                'title_alpha': 0
            }
        ]
        self.current_node = None
        self.display_time = 0

    def _init_player(self):
        """Initialize player spacecraft"""
        self.player = {
            'x': self.center_x,
            'y': self.center_y,
            'radius': 15,
            'speed': 5,
            'trail': [],
            'color': COLORS["Purple"],
        }

    def _init_effects(self):
        """Initialize visual effects"""
        self.stars: List[Dict] = []
        self._generate_stars(200)

        # Font setup
        self.font_title = pygame.font.SysFont(FONT_NAME, 36, bold=True)
        self.font_content = pygame.font.SysFont(FONT_NAME, 24)
        self.font_node = pygame.font.SysFont(FONT_NAME, 20, bold=True)

        # Sound flag
        self.play_discovery_sound = False

    def _generate_stars(self, count: int):
        """Create background stars with parallax effect"""
        for _ in range(count):
            self.stars.append({
                'x': random.randint(0, self.width),
                'y': random.randint(0, self.height),
                'size': random.randint(1, 3),
                'speed': random.uniform(0.1, 0.5),
                'brightness': random.randint(100, 255)
            })

    def handle_events(self, event: pygame.event.Event) -> bool:
        handled = super().handle_events(event)

        if not self.code_viewer.show_code and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.current_node:
                self.current_node = None
                handled = True

        return handled

    def update(self, dt: float) -> bool:
        if self.code_viewer.show_code:
            return False

        self._update_player()
        self._update_nodes()
        self._update_stars()
        return False

    def _update_player(self):
        """Handle player movement and trail"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_h]:
            self.player['x'] = max(self.player['radius'], self.player['x'] - self.player['speed'])
        if keys[pygame.K_l]:
            self.player['x'] = min(self.width - self.player['radius'], self.player['x'] + self.player['speed'])
        if keys[pygame.K_k]:
            self.player['y'] = max(self.player['radius'], self.player['y'] - self.player['speed'])
        if keys[pygame.K_j]:
            self.player['y'] = min(self.height - self.player['radius'], self.player['y'] + self.player['speed'])

        # Update trail
        self.player['trail'].append((self.player['x'], self.player['y']))
        if len(self.player['trail']) > 20:
            self.player['trail'].pop(0)

    def _update_nodes(self):
        """Handle node interactions"""
        prev_node = self.current_node
        self.current_node = None

        for node in self.nodes:
            distance = math.hypot(
                self.player['x'] - node['x'],
                self.player['y'] - node['y']
            )

            # Handle title fading
            if node['show_title']:
                node['title_alpha'] = max(0, node['title_alpha'] - 2)
                if node['title_alpha'] <= 0:
                    node['show_title'] = False

            # Check collision
            if distance < self.player['radius'] + node['radius']:
                node['discovered'] = True
                self.current_node = node
                if prev_node != self.current_node:
                    self.play_discovery_sound = True
                    self.display_time = pygame.time.get_ticks()
                    node['show_title'] = True
                    node['title_alpha'] = 255

    def _update_stars(self):
        """Update starfield parallax effect"""
        for star in self.stars:
            star['y'] += star['speed']
            if star['y'] > self.height:
                star['y'] = 0
                star['x'] = random.randint(0, self.width)

    def draw(self) -> None:
        super().draw()

        if self.code_viewer.show_code:
            return

        self._draw_background()
        self._draw_player()
        self._draw_nodes()
        self._draw_node_content()

    def _draw_background(self):
        """Draw starfield background"""
        self.screen.fill(COLORS["background"])
        for star in self.stars:
            pygame.draw.circle(
                self.screen,
                (star['brightness'], star['brightness'], star['brightness']),
                (int(star['x']), int(star['y'])),
                star['size']
            )

    def _draw_player(self):
        """Draw player spacecraft and trail"""
        # Trail
        for i, (x, y) in enumerate(self.player['trail']):
            alpha = int(255 * (i / len(self.player['trail'])))
            pygame.draw.circle(
                self.screen,
                (*self.player['color'], alpha),
                (int(x), int(y)),
                int(self.player['radius'] * (i / len(self.player['trail'])))
            )

        # Player
        pygame.draw.circle(
            self.screen,
            self.player['color'],
            (int(self.player['x']), int(self.player['y'])),
            self.player['radius']
        )

    def _draw_nodes(self):
        """Draw interactive nodes"""
        for node in self.nodes:
            # Pulsing effect
            if not node['discovered']:
                pulse = 5 * math.sin(pygame.time.get_ticks() / 300)
                radius = node['radius'] + int(pulse)
                color = (
                    min(255, node['color'][0] + int(pulse * 2)),
                    min(255, node['color'][1] + int(pulse * 2)),
                    min(255, node['color'][2] + int(pulse * 2))
                )
            else:
                radius = node['radius']
                color = node['color']

            pygame.draw.circle(
                self.screen,
                color,
                (int(node['x']), int(node['y'])),
                radius
            )

            # Node title
            if node['show_title'] and node['title_alpha'] > 0:
                title_surface = self.font_node.render(node['title'], True, node['color'])
                title_surface.set_alpha(node['title_alpha'])
                self.screen.blit(
                    title_surface,
                    (node['x'] - title_surface.get_width() // 2,
                     node['y'] + node['radius'] + 10)
                )

    def _draw_node_content(self):
        """Draw expanded node content when active"""
        if not self.current_node:
            if not any(node['discovered'] for node in self.nodes):
                self._draw_instructions()
            return

        # Animated panel
        elapsed = (pygame.time.get_ticks() - self.display_time) / 500
        alpha = min(255, int(255 * elapsed * 3))
        size_factor = min(1.0, elapsed * 2)

        panel_width = int(self.width * 0.6 * size_factor)
        panel_height = int(self.height * 0.5 * size_factor)
        half_panel_width = panel_width // 2
        half_panel_height = panel_height // 2

        panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel.fill((*COLORS["background"][:3], 220))

        # Border
        border_color = (*self.current_node['color'], alpha)
        pygame.draw.rect(
            panel,
            border_color,
            (0, 0, panel_width, panel_height),
            5,
            15
        )

        self.screen.blit(
            panel,
            (self.center_x - half_panel_width,
             self.center_y - half_panel_height)
        )

        # Content
        title = self.font_title.render(
            self.current_node['title'],
            True,
            self.current_node['color']
        )
        self.screen.blit(
            title,
            (self.center_x - title.get_width() // 2,
             self.center_y - half_panel_height + 30)
        )

        # Text lines
        for i, line in enumerate(self.current_node['content'].split('\n')):
            text = self.font_content.render(line, True, COLORS["text"])
            self.screen.blit(
                text,
                (self.center_x - text.get_width() // 2,
                 self.center_y - half_panel_height + 80 + i * 30)
            )

        # Close hint
        if pygame.time.get_ticks() - self.display_time > 1000:
            hint = self.font_content.render(
                "Move the SPACECRAFT to continue exploring",
                True,
                COLORS["text"]
            )
            self.screen.blit(
                hint,
                (self.center_x - hint.get_width() // 2,
                 self.center_y + half_panel_height - 40)
            )

    def _draw_instructions(self):
        """Draw initial instructions"""
        hint = self.font_content.render(
            "Use Vim-keys [h, j, k, l] to explore information nodes",
            True,
            COLORS["text"]
        )
        self.screen.blit(
            hint,
            (self.center_x - hint.get_width() // 2,
             self.height - 90)
        )
