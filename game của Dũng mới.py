import pygame
import random
import sys
import cv2
import mediapipe as mp
difficulty = "normal"
story_lines = [
    "Vào một nơi xa xôi, có hành tinh tên Cheems 01A3.",
    "Nơi ấy có con cheems siêu to khổng lồ che lấp cả bầu trời, nó hấp thụ tinh hoa của trời đất để trở nên to lớn và là thủ lĩnh của rất nhiều quát vật ở đây.",
    "Và tại đây, bạn được spawn ra dưới hình hài là một quả trứng ếch bé nhỏ. ",
    "Bạn phải tìm cách né tránh, lẩn trốn kẻ thù và những chướng ngoại vật, ăn thật nhiều để tích lũy năng lượng cho cơ thể tiến hóa",
    "Hãy sống sót và hãy ghi nhớ rằng nếu không còn thức ăn đó không phải là bug đó là tính năng ( hãy chú ý đến những thứ đứng yên).",
    " Chúc bạn may mắn !"
]
finger_control = False
pygame.init()
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)
mp_draw = mp.solutions.drawing_utils

cap = None# webcam (chỉ mở khi cần)
prev_finger_pos = None
pygame.mixer.init()
prev_finger_x = None
prev_finger_y = None
def difficulty_menu():
    global difficulty, finger_control
    btn_normal = Button("Normal", 280, 250, 240, 50)
    btn_hard = Button("Hard", 280, 320, 240, 50)
    btn_extreme = Button("Extreme", 280, 390, 240, 50)
    btn_finger = Button("Finger Control", WIDTH - 200, 20, 180, 40)
    btn_finger.color = (200, 200, 200)
    while True:
        screen.fill((50, 80, 50))

        title = font.render("CHON DO KHO", True, (255, 255, 255))
        screen.blit(title, (WIDTH//2 - 80, 150))
        if finger_control:
            btn_finger.color = (0, 255, 200)
        else:
            btn_finger.color = (200, 200, 200)

        btn_normal.draw()
        btn_hard.draw()
        btn_extreme.draw()
        btn_finger.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_finger.is_clicked(event.pos):
                    s_click.play()
                    finger_control = True
                    difficulty = "extreme"
                    game_loop()
                if btn_normal.is_clicked(event.pos):
                    finger_control = False
                    release_camera() 
                    difficulty = "normal"
                    s_click.play()
                    game_loop()

                if btn_hard.is_clicked(event.pos):
                    finger_control = False
                    release_camera() 
                    difficulty = "hard"
                    s_click.play()
                    game_loop()

                if btn_extreme.is_clicked(event.pos):
                    finger_control = False
                    release_camera() 
                    difficulty = "extreme"
                    s_click.play()
                    game_loop()

        pygame.display.flip()
# Âm thanh nút
s_click = pygame.mixer.Sound("assets/amthanhnhannut.mp3")

# Âm thanh di chuyển
s_move = pygame.mixer.Sound("assets/tiengdichuyennhanvat.mp3")

# Âm thanh predator tới gần
s_predator = pygame.mixer.Sound("assets/tiengrankeukhitoigan.mp3")

# Âm thanh ăn
s_eat = pygame.mixer.Sound("assets/tiengan.mp3")

# Âm thanh biến thành SuperFrog
s_super = pygame.mixer.Sound("assets/tienggong.mp3")

# Âm thanh chiến thắng
s_win = pygame.mixer.Sound("assets/tienganmung.mp3")
pygame.mixer.music.load("assets/recording.mp3")
pygame.mixer.music.set_volume(0.5)
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tadpoles tales")
BG_MENU = pygame.transform.scale(
    pygame.image.load("assets/aoho.png"), (WIDTH, HEIGHT)
)

BG_GAME = pygame.transform.scale(
    pygame.image.load("assets/hinhnen.png"), (WIDTH, HEIGHT)
)
font = pygame.font.Font("arial.ttf", 24)
# --- Tải ảnh nhân vật ---
# --- Tải animation cho từng stage ---
def load_frames(prefix, count, size):
    frames = []
    for i in range(count):
        img = pygame.image.load(f"assets/{prefix}{i}.png")
        img = pygame.transform.scale(img, size)
        frames.append(img)
    return frames
SUPER_ATTACK_FRAME = pygame.transform.scale(
    pygame.image.load("assets/frog_super0.png"), (90, 90)
)
# Tadpole1: 5 frame
TADPOLE1_FRAMES = [
    pygame.transform.scale(pygame.image.load("assets/tadpole1_0a.png"), (45, 45)),
    pygame.transform.scale(pygame.image.load("assets/tadpole1_1a.png"), (45, 45)),
    pygame.transform.scale(pygame.image.load("assets/tadpole1_2a.png"), (45, 45)),
    pygame.transform.scale(pygame.image.load("assets/tadpole1_3a.png"), (45, 45)),
    pygame.transform.scale(pygame.image.load("assets/tadpole1_4a.png"), (45, 45)),
]

# Tadpole2: 4 frame
TADPOLE2_FRAMES = [
    pygame.transform.scale(pygame.image.load("assets/tadpole2_0.png"), (55, 55)),
    pygame.transform.scale(pygame.image.load("assets/tadpole2_1.png"), (55, 55)),
    pygame.transform.scale(pygame.image.load("assets/tadpole2_2.png"), (55, 55)),
    pygame.transform.scale(pygame.image.load("assets/tadpole2_3.png"), (55, 55)),
]

# Baby frog: 4 frame
BABY_FRAMES = [
    pygame.transform.scale(pygame.image.load("assets/frog_baby0.png"), (65, 65)),
    pygame.transform.scale(pygame.image.load("assets/frog_baby1a.png"), (65, 65)),
    pygame.transform.scale(pygame.image.load("assets/frog_baby2a.png"), (65, 65)),
    pygame.transform.scale(pygame.image.load("assets/frog_baby3a.png"), (65, 65)),
]

# AdultFrog (ảnh đứng yên)
ADULT_FRAME = pygame.transform.scale(pygame.image.load("assets/frog_adult.png"), (80, 80))

# SuperFrog
SUPER_FRAME = pygame.transform.scale(pygame.image.load("assets/frog_super.png"), (90, 90))
MICROBE1_IMG = pygame.transform.scale(
    pygame.image.load("assets/microbe1.png"), (20, 20)
)

MICROBE2_IMG = pygame.transform.scale(
    pygame.image.load("assets/microbe2.png"), (30, 30)
)

STAGES = [
    ("Egg", [pygame.transform.scale(pygame.image.load("assets/egg.png"), (30, 30))]),
    ("Tadpole", TADPOLE1_FRAMES),
    ("Tadpole2", TADPOLE2_FRAMES),
    ("BabyFrog", BABY_FRAMES),
    ("AdultFrog", [ADULT_FRAME]),
    ("SuperFrog", [SUPER_FRAME]),
]
def draw_dialogue_box(text):
    box_height = 140
    box_rect = pygame.Rect(0, HEIGHT - box_height, WIDTH, box_height)

    pygame.draw.rect(screen, (0, 0, 0), box_rect)
    pygame.draw.rect(screen, (255, 255, 255), box_rect, 2)

    font = pygame.font.Font("arial.ttf", 24)

    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] < WIDTH - 40:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "

    lines.append(current_line)

    y = HEIGHT - box_height + 20
    for line in lines:
        rendered = font.render(line, True, (255, 255, 255))
        screen.blit(rendered, (20, y))
        y += 28

def story_screen():
    current_line = 0
    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        screen.fill((0, 0, 0))  # màn hình đen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                s_click.play()
                current_line += 1

                if current_line >= len(story_lines):
                    difficulty_menu()   # sang chọn chế độ
                    return

        draw_dialogue_box(story_lines[current_line])
        pygame.display.flip()
# =====================================================
# BUTTON
# =====================================================
class Button:
    def __init__(self, text, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = font.render(text, True, (0, 0, 0))
        self.color = (200, 200, 200)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text, (self.rect.x + 20, self.rect.y + 10))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


# =====================================================
# PREDATOR
# =====================================================
PREDATOR_IMG = pygame.transform.scale(
    pygame.image.load("assets/predator0a.png"), (70, 70)
)
class Predator:
    def __init__(self, safe_zone):
        self.frames = [
            pygame.transform.scale(pygame.image.load(f"assets/predator{i}a.png"), (90, 90))
            for i in range(8)
        ]
        self.anim_index = 0
        self.anim_speed = 0.2
        
        self.original_img = self.frames[0]
        self.img = self.original_img
        self.anim_forward = True

        while True:
            x = random.randint(50, WIDTH - 50)
            y = random.randint(50, HEIGHT - 50)
            if (x - safe_zone[0])**2 + (y - safe_zone[1])**2 > 250**2:
                break

        self.mask = pygame.mask.from_surface(self.img)
        self.rect = self.img.get_rect(center=(x, y))
        self.speed = 1.4
        self.vx = random.choice([-1, 1]) * self.speed
        self.vy = random.choice([-1, 1]) * self.speed
        self.direction = "right"
        self.change_timer = 0

    def update_direction(self):
        if self.vx < 0:
            self.direction = "left"
        elif self.vx > 0:
            self.direction = "right"

        # lật ảnh theo hướng
        if self.direction == "left":
            self.img = pygame.transform.flip(self.original_img, True, False)
        else:
            self.img = self.original_img

        self.mask = pygame.mask.from_surface(self.img)

    def move(self, player):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        dist = (dx*dx + dy*dy) ** 0.5

        if dist < 250:
            if dist != 0:
                self.vx = dx / dist * self.speed * 1.2
                self.vy = dy / dist * self.speed * 1.2
        else:
            self.change_timer += 1
            if self.change_timer > random.randint(50, 120):
                self.vx = random.choice([-1, 0, 1]) * self.speed
                self.vy = random.choice([-1, 0, 1]) * self.speed
                self.change_timer = 0

        self.rect.x += self.vx
        self.rect.y += self.vy

        # chạm tường bật lại
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.vx *= -1
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.vy *= -1

        # cập nhật hướng theo vx
        self.update_direction()

    def draw(self):
    # Animation ping-pong 0→7→0→…
        if self.anim_forward:
            self.anim_index += self.anim_speed
            if self.anim_index >= len(self.frames) - 1:
                self.anim_index = len(self.frames) - 1
                self.anim_forward = False
        else:
            self.anim_index -= self.anim_speed
            if self.anim_index <= 0:
                self.anim_index = 0
                self.anim_forward = True

        img = self.frames[int(self.anim_index)]

        if self.direction == "left":
            img = pygame.transform.flip(img, True, False)

        screen.blit(img, self.rect)



# PLAYER
# =====================================================
class Player:
    def super_attack(self):
        self.is_attacking = True
        self.attack_timer = 20   # số frame tồn tại hiệu ứng (≈ 0.33s)

    def __init__(self):
        self.tp_cooldown = 0
        self.stage = 0
        frames = STAGES[self.stage][1]
        self.frames = frames               # lưu list frame để animate
        self.img = frames[0]               # frame đầu tiên
        self.mask = pygame.mask.from_surface(self.img)
        self.rect = self.img.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.speed = 3
        self.is_attacking = False
        self.attack_timer = 0
        self.eat_count = 0
        self.microbe2_count = 0
        self.has_moved = False

        self.direction = "right"  # hướng mặt hiện tại
        self.anim_index = 0
        self.anim_speed = 0.15  # tốc độ chuyển frame
        if difficulty == "extreme":
            if self.stage == 1:      # Tadpole1
                self.speed = 3 / 2
            elif self.stage == 2:    # Tadpole2
                self.speed = 3 * 0.75

    def teleport(self):
        if self.tp_cooldown > 0 or difficulty != "extreme":
            return

        dist = 140  # khoảng dịch chuyển

        if self.direction == "up":
            self.rect.y -= dist
        elif self.direction == "down":
            self.rect.y += dist
        elif self.direction == "left":
            self.rect.x -= dist
        elif self.direction == "right":
            self.rect.x += dist

        self.tp_cooldown = 40  # 40 frame để hồi

    def evolve(self):
        if self.stage == 0:
            self.stage = 1
        elif self.stage == 1 and self.eat_count >= 5:
            self.stage = 2
        elif self.stage == 2 and self.eat_count >= 10:
            self.stage = 3
        elif self.stage == 3 and self.eat_count >= 20:
            self.stage = 4
        elif self.stage == 4 and self.microbe2_count >= 37:
            s_super.play()
            self.stage = 5
            explosion_effect(self.rect.centerx, self.rect.centery)

        center = self.rect.center
        frames = STAGES[self.stage][1]
        self.frames = frames
        self.img = frames[0]
        self.mask = pygame.mask.from_surface(self.img)
        self.rect = self.img.get_rect(center=center)


    def move(self, keys, finger_pos=None):
        old_rect = self.rect.copy()

    # ================= FINGER CONTROL =================
        if finger_control:
            if finger_pos is None:
                return old_rect

            fx, fy = finger_pos

        # di chuyển theo tốc độ ngón tay (1:1)
            dx = fx - self.rect.centerx
            dy = fy - self.rect.centery

            self.rect.centerx += int(dx * 0.35)
            self.rect.centery += int(dy * 0.35)

            self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))
            if abs(dx) > abs(dy):
                self.direction = "right" if dx > 0 else "left"
            else:
                self.direction = "down" if dy > 0 else "up"

            return old_rect
   
        # ---- WASD GIỮ NGUYÊN ----
        if not self.has_moved and (keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]):
            s_move.play()
            s_move.set_volume(0.3)
            self.has_moved = True
            self.evolve()
        old_rect = self.rect.copy()
        # ---- Xác định hướng ----
        if keys[pygame.K_w]:
            self.direction = "up"
        elif keys[pygame.K_s]:
            self.direction = "down"
        elif keys[pygame.K_a]:
            self.direction = "left"
        elif keys[pygame.K_d]:
            self.direction = "right"

# ---- Di chuyển ----
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed

        if keys[pygame.K_s] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed

        if keys[pygame.K_d] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        return old_rect
        if self.tp_cooldown>0:
            self.tp_cooldown-=1
        return old_rect
    def draw(self):
        frames = self.frames
        if self.stage == 5 and self.is_attacking:
             screen.blit(SUPER_ATTACK_FRAME, self.rect)
             self.attack_timer -= 1
             if self.attack_timer <= 0:
                 self.is_attacking = False
             return
    # Tăng frame theo thời gian
        self.anim_index += self.anim_speed
        if self.anim_index >= len(frames):
            self.anim_index = 0

        img = frames[int(self.anim_index)]

    # Xoay theo hướng
        four_dir = [1, 2, 3]  # tadpole1, tadpole2, baby

        if self.stage in four_dir:
            if self.direction == "left":
                img = pygame.transform.flip(img, True, False)
            elif self.direction == "up":
                img = pygame.transform.rotate(img, 90)
            elif self.direction == "down":
                img = pygame.transform.rotate(img, -90)

        else:
        # egg, adult, super only flip left/right
            if self.direction == "left":
                img = pygame.transform.flip(img, True, False)

        screen.blit(img, self.rect)

# MICROBE
# =====================================================
class Microbe:
    def __init__(self):
        self.type = random.choice([1, 2])

        if self.type == 1:
            self.original_img = MICROBE1_IMG
        else:
            self.original_img = MICROBE2_IMG

        self.img = self.original_img
        self.rect = self.img.get_rect(
            center=(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50))
        )

        if self.type == 2:
            self.vx = random.uniform(-1, 1)
            self.vy = random.uniform(-1, 1)
        else:
            self.vx = 0
            self.vy = 0

        self.direction = "right"
        self.frames = [self.original_img]
        self.anim_index = 0
        if difficulty == "hard":
            if self.type == 2:
                self.vx *= 1.6
                self.vy *= 1.6

        if difficulty == "extreme":
            if self.type == 2:
                self.vx *= 2
                self.vy *= 2
    def update_direction(self):
        if self.type == 1:
            return  # microbe1 đứng yên, không xoay

        if self.vx < 0:
            self.direction = "left"
        elif self.vx > 0:
            self.direction = "right"

        if self.direction == "left":
            self.img = pygame.transform.flip(self.original_img, True, False)
        else:
            self.img = self.original_img

    def move(self):
        if self.type == 2:
            self.rect.x += self.vx
            self.rect.y += self.vy

            if self.rect.left < 0 or self.rect.right > WIDTH:
                self.vx *= -1
            if self.rect.top < 0 or self.rect.bottom > HEIGHT:
                self.vy *= -1

            self.update_direction()

    def draw(self):
        screen.blit(self.original_img, self.rect)
def get_finger_position():
    global cap

    if cap is None:
        cap = cv2.VideoCapture(0)

    ret, frame = cap.read()
    if not ret:
        return None

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if not result.multi_hand_landmarks:
        return None

    hand = result.multi_hand_landmarks[0]
    finger = hand.landmark[8]

    x = int(finger.x * WIDTH)
    y = int(finger.y * HEIGHT)

    return x, y
def release_camera():
    global cap
    if cap is not None:
        cap.release()
        cap = None
# GAME LOOP
# =====================================================
def explosion_effect(x, y):
    for size in range(10, 200, 15):
        screen.blit(BG_GAME, (0, 0))
        pygame.draw.circle(screen, (255, 255, 100), (x, y), size, 5)
        pygame.display.flip()
        pygame.time.delay(30)

def game_loop():
    pygame.mixer.music.play(-1)
    player = Player()
    microbes = [Microbe() for _ in range(10)]
    if difficulty == "normal":
        predators = [Predator(player.rect.center) for _ in range(2)]
    elif difficulty == "hard":
        predators = [Predator(player.rect.center) for _ in range(4)]
    elif difficulty == "extreme":
        predators = [Predator(player.rect.center) for _ in range(5)]
    paused = False
    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)
        screen.blit(BG_GAME, (0, 0))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
               pygame.quit()
               sys.exit()

            if event.type == pygame.KEYDOWN:

               if event.key == pygame.K_SPACE:
                  s_click.play()
                  paused = not paused

               if event.key == pygame.K_p:
                  player.teleport()

        if paused:
            txt = font.render("Paused (SPACE to resume)", True, (255, 255, 255))
            screen.blit(txt, (WIDTH//2 - 160, HEIGHT//2))
            pygame.display.flip()
            continue

        keys = pygame.key.get_pressed()
        hand_pos = None
        if finger_control:
            hand_pos = get_finger_position()

        old_rect = player.move(keys, hand_pos)
        # --------------------------
        # MICROBE COLLISION
        # --------------------------
        for m in microbes[:]:

            # microbe2 là vật cản khi stage <=2
            if m.type == 2 and player.stage <= 2:
                if player.rect.colliderect(m.rect):
                    player.rect = old_rect
                    continue

            # microbe1 ăn giai đoạn <=2
            if m.type == 1 and player.stage <= 2:
                if player.rect.colliderect(m.rect):
                    player.eat_count += 1
                    player.evolve()
                    s_eat.play()
                    microbes.remove(m)
                    microbes.append(Microbe())
                    continue

            # microbe2 để lên SuperFrog
            if m.type == 2:
                if player.rect.colliderect(m.rect):
                    player.microbe2_count += 1
                    player.evolve()
                    s_eat.play()
                    microbes.remove(m)
                    microbes.append(Microbe())
                    continue

            # stage >= 3 ăn cả hai
            if player.stage >= 3 and player.rect.colliderect(m.rect):
                player.eat_count += 1
                player.evolve()
                s_eat.play()
                microbes.remove(m)
                microbes.append(Microbe())
                continue
            count_m1 = sum(1 for m in microbes if m.type == 1)
            count_m2 = sum(1 for m in microbes if m.type == 2)
 
            if count_m1 == 0:
                add_n = random.randint(1, 4)
                for _ in range(add_n):        # số lượng bạn muốn
                     new_m = Microbe()
                     new_m.type = 1
                     new_m.img = MICROBE1_IMG
                     microbes.append(new_m)

            if count_m2 == 0:
                for _ in range(3):        # số lượng bạn muốn
                     new_m = Microbe()
                     new_m.type = 2
                     new_m.img = MICROBE2_IMG
                     new_m.vx = random.uniform(-1, 1)
                     new_m.vy = random.uniform(-1, 1)
                     microbes.append(new_m)
        # --------------------------
        # PREDATOR COLLISION
        # --------------------------
        for p in predators:
            p.move(player)

            offset = (p.rect.x - player.rect.x, p.rect.y - player.rect.y)
            # Âm thanh predator tới gần
            dx = player.rect.centerx - p.rect.centerx
            dy = player.rect.centery - p.rect.centery
            dist = (dx*dx + dy*dy) ** 0.5
            if player.stage < 5 and dist <= 50:
                 s_predator.play()
            if player.mask.overlap(p.mask, offset):
                
                if player.stage == 5:
        # SUPER FROG ĂN ĐƯỢC PREDATOR
                    player.super_attack()   # <<< THÊM DÒNG NÀY
                    predators.remove(p)
                    if len(predators) == 0:
                         pygame.mixer.music.stop()
                         win_screen()
                         return
                else:
                     pygame.mixer.music.stop()
                     game_over_screen()
                     return

        # --------------------------
        # DRAW
        # --------------------------
        player.draw()
        for m in microbes:
            m.move()
            m.draw()
        for p in predators:
            p.draw()

        # thanh tiến hóa đại khái
        pygame.draw.rect(screen, (30, 30, 30), (20, 10, 200, 20))
        fill = min(player.eat_count % 5, 5) * 40
        pygame.draw.rect(screen, (0, 200, 0), (20, 10, fill, 20))

        text2 = font.render(f"Microbe2 eaten: {player.microbe2_count}/37", True, (255, 255, 255))
        screen.blit(text2, (20, 40))

        pygame.display.flip()
if cap:
    cap.release()
    cap = None

# =====================================================
# MENU
# =====================================================
def main_menu():
    play_btn = Button("PLAY", 280, 300, 240, 50)
    quit_btn = Button("QUIT", 280, 370, 240, 50)

    while True:
        screen.blit(BG_MENU, (0, 0))

        play_btn.draw()
        quit_btn.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_btn.is_clicked(event.pos):
                    s_click.play()
                    story_screen()

                if quit_btn.is_clicked(event.pos):
                    s_click.play()
                    pygame.quit()
                    sys.exit()
        pygame.mixer.music.stop()
        pygame.display.flip()
def win_screen():
    s_win.play()
    btn = Button("MAIN MENU", 280, 360, 240, 50)
    
    while True:
        screen.fill((20, 40, 20))

        text = font.render("         Congratulations !", True, (255, 255, 255))
        screen.blit(text, (WIDTH//2 - 150, 200))

        btn.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn.is_clicked(event.pos):
                    s_click.play()
                    pygame.mixer.music.stop()
                    release_camera()
                    return  # quay về menu
       
        pygame.display.flip()
def game_over_screen():
    btn = Button("MAIN MENU", 280, 360, 240, 50)

    while True:
        screen.fill((80, 20, 20))

        text = font.render("YOU ARE CHICKEN !", True, (255, 255, 255))
        screen.blit(text, (WIDTH//2 - 100, 200))

        btn.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn.is_clicked(event.pos):
                    s_click.play()
                    pygame.mixer.music.stop()
                    release_camera()
                    return  # quay về menu

        pygame.display.flip()

main_menu()
