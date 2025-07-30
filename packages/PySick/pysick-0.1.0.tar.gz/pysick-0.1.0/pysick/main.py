import pygame
from pysick.scene import Scene
from pysick.input import Input
import draw
from pysick.text import Text
import sys


# ----------- Scene Implementation -----------

class GameScene(Scene):
    def __init__(self, screen):
        super().__init__(screen)
        # Load assets
        self.player_img = load_image("player.png")
        self.player = Sprite(self.player_img, x=100, y=100, scale=2.0)

        enemy_frames = load_images("enemy_idle_", 4)
        self.enemy = AnimatedSprite(enemy_frames, frame_duration=0.2, x=400, y=100, scale=2.0)
        self.enemy.play(loop=True)

        self.font = load_font("arcade.ttf", 28)
        self.text = Text(self.font, size=28, color=(255, 255, 255))
        self.text.set_outline((0, 0, 0), width=2)
        self.text.set_shadow((30, 30, 30), offset=(3, 3))

        self.jump_sound = load_sound("jump.wav")

        self.score = 0

    def handle_event(self, event):
        Input.handle_event(event)
        if event.type == pygame.QUIT:
            self.running = False

    def update(self, dt):
        Input.begin_frame()

        # Movement speed pixels per second
        speed = 200

        vx = 0
        vy = 0
        if Input.is_held("left"):
            vx = -speed
        elif Input.is_held("right"):
            vx = speed

        if Input.is_held("up"):
            vy = -speed
        elif Input.is_held("down"):
            vy = speed

        self.player.set_velocity(vx, vy)
        self.player.update(dt)
        self.enemy.update(dt)

        # Play jump sound on space pressed
        if Input.is_down("jump"):
            self.jump_sound.play()
            self.score += 10

    def draw(self):
        self.screen.fill((100, 149, 237))  # Cornflower Blue background

        self.player.draw(self.screen)
        self.enemy.draw(self.screen)

        self.text.render_to(self.screen, f"Score: {self.score}", (20, 20))

# ----------- Main Game Loop -----------

def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("PySick Window")

    clock = pygame.time.Clock()
    scene.running = True

    while scene.running:
        dt = clock.tick(60) / 1000  # Delta time in seconds

        for event in pygame.event.get():
            scene.handle_event(event)

        scene.update(dt)
        scene.draw()
        pygame.display.flip()

    pygame.quit()
# === SICK Key Constants ===
SICK_K_UP = pygame.K_UP
SICK_K_DOWN = pygame.K_DOWN
SICK_K_LEFT = pygame.K_LEFT
SICK_K_RIGHT = pygame.K_RIGHT
SICK_K_SPACE = pygame.K_SPACE
SICK_K_RETURN = pygame.K_RETURN
SICK_K_ESCAPE = pygame.K_ESCAPE
SICK_K_BACKSPACE = pygame.K_BACKSPACE
SICK_K_TAB = pygame.K_TAB
SICK_K_LSHIFT = pygame.K_LSHIFT
SICK_K_RSHIFT = pygame.K_RSHIFT
SICK_K_LCTRL = pygame.K_LCTRL
SICK_K_RCTRL = pygame.K_RCTRL
SICK_K_LALT = pygame.K_LALT
SICK_K_RALT = pygame.K_RALT

# Letters
SICK_K_A = pygame.K_a
SICK_K_B = pygame.K_b
SICK_K_C = pygame.K_c
SICK_K_D = pygame.K_d
SICK_K_E = pygame.K_e
SICK_K_F = pygame.K_f
SICK_K_G = pygame.K_g
SICK_K_H = pygame.K_h
SICK_K_I = pygame.K_i
SICK_K_J = pygame.K_j
SICK_K_K = pygame.K_k
SICK_K_L = pygame.K_l
SICK_K_M = pygame.K_m
SICK_K_N = pygame.K_n
SICK_K_O = pygame.K_o
SICK_K_P = pygame.K_p
SICK_K_Q = pygame.K_q
SICK_K_R = pygame.K_r
SICK_K_S = pygame.K_s
SICK_K_T = pygame.K_t
SICK_K_U = pygame.K_u
SICK_K_V = pygame.K_v
SICK_K_W = pygame.K_w
SICK_K_X = pygame.K_x
SICK_K_Y = pygame.K_y
SICK_K_Z = pygame.K_z

# Numbers
SICK_K_0 = pygame.K_0
SICK_K_1 = pygame.K_1
SICK_K_2 = pygame.K_2
SICK_K_3 = pygame.K_3
SICK_K_4 = pygame.K_4
SICK_K_5 = pygame.K_5
SICK_K_6 = pygame.K_6
SICK_K_7 = pygame.K_7
SICK_K_8 = pygame.K_8
SICK_K_9 = pygame.K_9

# Function Keys
SICK_K_F1 = pygame.K_F1
SICK_K_F2 = pygame.K_F2
SICK_K_F3 = pygame.K_F3
SICK_K_F4 = pygame.K_F4
SICK_K_F5 = pygame.K_F5
SICK_K_F6 = pygame.K_F6
SICK_K_F7 = pygame.K_F7
SICK_K_F8 = pygame.K_F8
SICK_K_F9 = pygame.K_F9
SICK_K_F10 = pygame.K_F10
SICK_K_F11 = pygame.K_F11
SICK_K_F12 = pygame.K_F12
QUIT = pygame.QUIT
def keys_pressed():
    return pygame.key.get_pressed()
def MOUSE_DOWN():
    return pygame.MOUSEBUTTONDOWN
def MOUSE_POS():
    return pygame.mouse.get_pos()
def get_events():
    return pygame.event.get()
def quit():
    pygame.quit()
class PySick:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("PySick Window")
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.SysFont("Arial", 24)

        # Sprite placeholders
        self.player = {'x': 100, 'y': 100, 'w': 50, 'h': 50, 'color': (0, 255, 0), 'speed': 5}
        self.enemy = {'x': 300, 'y': 200, 'radius': 30, 'color': (255, 0, 0)}
    def set_title(self, title):
        pygame.display.set_caption(title)
    def fill(self, color):
        self.screen.fill(color)

    # === Drawing ===
    def draw_rect(self, x, y, width, height, color=(255, 255, 255), border=0):
        pygame.draw.rect(self.screen, color, pygame.Rect(x, y, width, height), border)

    def draw_circle(self, x, y, radius, color=(255, 255, 255), border=0):
        pygame.draw.circle(self.screen, color, (x, y), radius, border)

    def draw_line(self, start_pos, end_pos, color=(255, 255, 255), width=1):
        pygame.draw.line(self.screen, color, start_pos, end_pos, width)

    def draw_text(self, text, x, y, color=(255, 255, 255)):
        surface = self.font.render(text, True, color)
        self.screen.blit(surface, (x, y))

    # === Input Handling ===
    def get_keys(self):
        return pygame.key.get_pressed()

    def handle_input(self):
        keys = self.get_keys()
        if keys[pygame.K_LEFT]:
            self.player['x'] -= self.player['speed']
        if keys[pygame.K_RIGHT]:
            self.player['x'] += self.player['speed']
        if keys[pygame.K_UP]:
            self.player['y'] -= self.player['speed']
        if keys[pygame.K_DOWN]:
            self.player['y'] += self.player['speed']

    # === Sprite & Collision (basic) ===
    def check_collision(self, rect1, rect2):
        return rect1.colliderect(rect2)

    def get_player_rect(self):
        return pygame.Rect(self.player['x'], self.player['y'], self.player['w'], self.player['h'])

    def get_enemy_rect(self):
        r = self.enemy['radius']
        return pygame.Rect(self.enemy['x'] - r, self.enemy['y'] - r, r * 2, r * 2)

    # === Scene Update ===
    def update(self):
        pygame.display.flip()
        self.clock.tick(60)

    # === Scene Draw ===
    def render(self):
        self.screen.fill((30, 30, 30))
        self.draw_rect(self.player['x'], self.player['y'], self.player['w'], self.player['h'], self.player['color'])
        self.draw_circle(self.enemy['x'], self.enemy['y'], self.enemy['radius'], self.enemy['color'])
        self.draw_text("PySick — All-in-One", 10, 10)
        pygame.display.flip()
    # === Buttons ===
    def draw_button(self, x, y, w, h, text, color=(100, 100, 255), hover_color=(150, 150, 255), text_color=(255, 255, 255)):
        mouse_pos = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()[0]
        is_hover = pygame.Rect(x, y, w, h).collidepoint(mouse_pos)
        draw_color = hover_color if is_hover else color
        self.draw_rect(x, y, w, h, draw_color)
        self.draw_text(text, x + 10, y + 10, text_color)
        return is_hover and clicked

    # === More Shapes ===
    def draw_polygon(self, points, color=(255, 255, 255), border=0):
        pygame.draw.polygon(self.screen, color, points, border)

    def draw_ellipse(self, x, y, w, h, color=(255, 255, 255), border=0):
        rect = pygame.Rect(x, y, w, h)
        pygame.draw.ellipse(self.screen, color, rect, border)

    # === Mouse Input ===
    def get_mouse_pos(self):
        return pygame.mouse.get_pos()

    def is_mouse_pressed(self):
        return pygame.mouse.get_pressed()[0]

    # === Timers & Events ===
    def set_timer(self, event_id, interval_ms):
        pygame.time.set_timer(event_id, interval_ms)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.USEREVENT:
                print("[Timer Event] Custom timer triggered")

    # === Scene Management ===
    def change_scene(self, new_scene_func):
        self.current_scene = new_scene_func

    def scene_main_game(self):
        self.handle_input()
        self.render()
        self.draw_text("Press B for Button Test", 10, 40)

    def scene_with_button(self):
        self.screen.fill((20, 20, 50))
        if self.draw_button(300, 250, 200, 60, "Back to Game"):
            self.change_scene(self.scene_main_game)
        self.draw_text("This is a Button Scene", 280, 200)
        pygame.display.flip()

    # === Overriding run to handle scenes ===
    def run(self):
        self.current_scene = self.scene_main_game
        self.set_timer(pygame.USEREVENT, 5000)  # 5-second interval

        while self.running:
            self.handle_events()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_b]:
                self.change_scene(self.scene_with_button)

            self.update()
            if self.current_scene:
                self.current_scene()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

    def draw_button(self, x, y, width, height, text, color=(100, 100, 255), hover_color=(150, 150, 255),
                    text_color=(255, 255, 255), radius=10, animation_speed=5):
        mouse_pos = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()[0]
        is_hover = pygame.Rect(x, y, w, h).collidepoint(mouse_pos)

        # Animated hover effect
        draw_color = hover_color if is_hover else color
        border_radius = radius if is_hover else max(radius - animation_speed, 0)

        pygame.draw.rect(self.screen, draw_color, pygame.Rect(x, y, w, h), border_radius=border_radius)

        # Text rendering
        text_surface = self.font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=(x + w // 2, y + h // 2))
        self.screen.blit(text_surface, text_rect)

        return is_hover and clicked

    def gameloop(self):
        while self.running:
            self.handle_events()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_b]:
                self.change_scene(self.scene_with_button)

            self.update()

            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
else:
    print('Hi! from PySick.')
    print('This is PySick, an Module for 2D games, used inBoundPyGame')
