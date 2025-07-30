#!/usr/bin/env python
# Pygame Tutor - Educational Platform by Sergey Samoylov
# LICENCE: GNU General Public License v3.0
# Source: https://github.com/sergey-samoylov/pygame-tutor

import pygame

class ScreenGeometry:
    """Centralized screen geometry calculations"""
    def __init__(self, screen_surface):
        self.surface = screen_surface
        self.rect = screen_surface.get_rect()
        
        # Basic dimensions
        self.width = self.rect.width
        self.height = self.rect.height
        
        # Horizontal positions
        self.center_x = self.rect.centerx
        self.quarter_x = self.width // 4
        self.three_quarter_x = self.width * 3 // 4
        self.left_pad = 50
        self.right_pad = self.width - 50
        
        # Vertical positions
        self.center_y = self.rect.centery
        self.third_y = self.height // 3
        self.two_thirds_y = self.height * 2 // 3
        self.top_pad = 50
        self.bottom_pad = self.height - 50
        
        # Common ratios (0.0-1.0)
        self.ratios = {
            'center': (0.5, 0.5),
            'top_left': (0.25, 0.25),
            'bottom_right': (0.75, 0.75)
        }
    
    def relative_pos(self, x_ratio, y_ratio):
        """Convert ratio (0.0-1.0) to absolute position"""
        return (
            int(self.width * x_ratio),
            int(self.height * y_ratio)
        )
    
    def relative_x(self, ratio):
        """Get horizontal position from ratio"""
        return int(self.width * ratio)
    
    def relative_y(self, ratio):
        """Get vertical position from ratio"""
        return int(self.height * ratio)
