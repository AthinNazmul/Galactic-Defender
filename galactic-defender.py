import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Enhanced Space Invaders')

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)

# Player settings
player_width = 50
player_height = 60
player_speed = 5

# Enemy settings
enemy_width = 50
enemy_height = 50
enemy_speed = 2

# Bullet settings
bullet_width = 5
bullet_height = 10
bullet_speed = 7

# Initialize clock
clock = pygame.time.Clock()
FPS = 30

# Font for displaying score and health
font = pygame.font.Font(None, 36)

# Player class
class Player:
    def __init__(self):
        self.rect = pygame.Rect(screen_width // 2 - player_width // 2, screen_height - player_height - 10, player_width, player_height)
        self.color = green
        self.speed = player_speed
        self.bullets = []
        self.lives = 3
        self.score = 0

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        for bullet in self.bullets:
            pygame.draw.rect(screen, self.color, bullet)

    def move(self, dx):
        self.rect.x += dx * self.speed
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width

    def shoot(self):
        bullet = pygame.Rect(self.rect.centerx - bullet_width // 2, self.rect.y, bullet_width, bullet_height)
        self.bullets.append(bullet)

    def take_damage(self):
        self.lives -= 1
        if self.lives <= 0:
            return True
        return False

# Enemy class
class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, enemy_width, enemy_height)
        self.color = red
        self.speed = enemy_speed

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

    def move(self):
        self.rect.y += self.speed

def game_loop():
    player = Player()
    enemies = [Enemy(random.randint(0, screen_width - enemy_width), random.randint(-1500, -100)) for _ in range(10)]
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-1)
        if keys[pygame.K_RIGHT]:
            player.move(1)
        if keys[pygame.K_SPACE]:
            player.shoot()

        # Update bullet positions
        for bullet in player.bullets:
            bullet.y -= bullet_speed
            if bullet.y < 0:
                player.bullets.remove(bullet)

        # Update enemy positions
        for enemy in enemies:
            enemy.move()
            if enemy.rect.y > screen_height:
                enemies.remove(enemy)
                enemies.append(Enemy(random.randint(0, screen_width - enemy_width), random.randint(-1500, -100)))

        # Check for collisions
        for bullet in player.bullets:
            for enemy in enemies:
                if enemy.rect.colliderect(bullet):
                    player.bullets.remove(bullet)
                    enemies.remove(enemy)
                    player.score += 10
                    enemies.append(Enemy(random.randint(0, screen_width - enemy_width), random.randint(-1500, -100)))
                    break

        # Check for game over
        for enemy in enemies:
            if enemy.rect.colliderect(player.rect):
                if player.take_damage():
                    game_over = True
                    print(f"Game Over! Your score: {player.score}")
                enemies.remove(enemy)
                enemies.append(Enemy(random.randint(0, screen_width - enemy_width), random.randint(-1500, -100)))

        # Drawing
        screen.fill(black)
        player.draw()
        for enemy in enemies:
            enemy.draw()

        # Draw score and lives
        score_text = font.render(f"Score: {player.score}", True, white)
        screen.blit(score_text, (10, 10))
        lives_text = font.render(f"Lives: {player.lives}", True, white)
        screen.blit(lives_text, (10, 50))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

game_loop()
