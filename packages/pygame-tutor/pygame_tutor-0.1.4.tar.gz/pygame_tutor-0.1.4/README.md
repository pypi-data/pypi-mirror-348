# 🎮 Pygame Educational Platform

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

**A playful coding playground** where Python meets Pygame in interactive
lessons! Designed for educators and learners to explore programming concepts
through visual, hands-on examples.

![Demo GIF](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcW9rZ3NqZ3Z5dWZ2b2V5dGJhY2V6Z2V6ZGVoYzB0ZzJ1Z3B5ZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xT5LMHxhOfscxPfIfm/giphy.gif)

## ✨ Features

- **Interactive Coding Lessons**:
  - 🚀 Comet animation with color-changing trails
  - ⚛️ Physics playground with bouncing balls
  - ⌨️ Key detection with visual feedback
  - 🎯 Breakout game with proper collision physics

- **Educational Tools**:
  - 📜 Real-time code viewer (toggle with `S`)
  - 📝 Concept explanations in each lesson
  - ↔️ Easy navigation between lessons

- **Developer Friendly**:
  - 🧩 Modular lesson system
  - 📱 Responsive screen geometry
  - 🎨 Themed color system

## 🛠️ How to Use

1. Clone the repository:
   ```bash
   git clone https://github.com/sergey-samoylov/pygame-tutor
   cd pygame-tutor
   ```

2. Run the main program:
   ```bash
   python main.py
   ```

3. **Controls**:
   - `←` `→` arrows: Navigate between lessons
   - `S`: Toggle code viewer
   - `Q` or `ESC`: Quit
   - Lesson-specific controls shown in each activity

## 📚 Lessons Overview

| Lesson | Description | Key Concepts |
|--------|-------------|--------------|
| **Cosmic Comet** | Animated comet with colorful trail | Animation loops, Screen wrapping, Color interpolation |
| **Physics Playground** | Bouncing balls with gravity | Collision detection, Physics simulation, Vector math |
| **Key Detection Lab** | Visual keyboard input feedback | Event handling, Input processing, Visual feedback |
| **Breakout Game** | Classic brick-breaking game | Game state management, Collision resolution, Paddle control |

## 🎨 Color Theme

Based on the Tokyo Night palette:
```python
{
    "background": (26, 27, 38),    # Dark blue-gray
    "text": (169, 177, 214),       # Light gray-blue
    "highlight": (122, 162, 247),  # Bright blue
    "accent": (158, 206, 106),     # Soft green
    "Orange": (255, 179, 0),       # Vibrant orange
    "Purple": (204, 153, 255)      # Light purple
}
```

## 🧑‍💻 Development

To add a new lesson:
1. Create `lesson_XX_name.py` in the lessons directory
2. Implement the lesson class inheriting from `BaseLesson`
3. Add required methods: `update()`, `draw()`, `handle_events()`

Example lesson structure:
```python
class LessonXXName(BaseLesson):
    def __init__(self, screen_geo):
        super().__init__(screen_geo)
        self.title = "My Cool Lesson"
        
    def update(self, dt):
        # Update game state
        
    def draw(self):
        # Render graphics
        
    def handle_events(self, event):
        # Process input events
```

## 📜 License

This project is licensed under the GNU GPLv3 License - see the [LICENSE](LICENSE) file for details.

---

> "The best way to learn is by doing." - This project brings that philosophy to programming education through interactive Pygame examples.

