import pygame, os
from random import randint

pygame.init()
WINDOW = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Plane Shooter")
FPS = 30

GRAY = (128, 128, 128)
GREEN = (0, 128, 0)
DARKRED = (139, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HEALTHPOINTFONT = pygame.font.SysFont("couriernew", 13, True)
SCOREFONT = pygame.font.SysFont("couriernew", 20, True)
ASSETSPATH = os.path.abspath(os.getcwd()) + "/Assets/" #"B:/HuangJiaQi/Python/Plane Shooter Pygame/Assets/"

class Buttons:
  def __init__(self, imagePath, x, y, scale):
    self.rawPicture = pygame.image.load(imagePath)
    self.picture = pygame.transform.scale(self.rawPicture, (int(self.rawPicture.get_width() * scale), int(self.rawPicture.get_height() * scale)))
    self.hitBox = self.picture.get_rect()
    self.hitBox.center = (x, y)
    self.clicked = False

  def drawButton(self):
    WINDOW.blit(self.picture, (self.hitBox.x, self.hitBox.y))

  def isClicked(self, mouse):
    mousePosition = pygame.mouse.get_pos()
    if self.hitBox.collidepoint(mousePosition):
      if mouse[0] and not self.clicked:
        self.clicked = True
        return True
    if not mouse[0]: self.clicked = False

class PlayerFighter:
  def __init__(self, speed, fireRate):
    self.speed = speed
    self.fireRate = int(FPS * (1 / fireRate)) #frames per round
    self.fireCoolDown = self.fireRate
    self.RPS = fireRate #rounds per second
    self.rawPicture = pygame.image.load(f"{ASSETSPATH}fighter_player.png")
    self.picture = pygame.transform.scale(self.rawPicture, (self.rawPicture.get_width() * 0.25, self.rawPicture.get_height() * 0.25))
    self.x = WINDOW.get_width() / 2 - self.picture.get_width() / 2
    self.y = WINDOW.get_height() - self.picture.get_height() - 10
    self.width = self.picture.get_width()
    self.height = self.picture.get_height()
    self.hitpoints = 20
    self.healthDeductionCD = 30
    self.draw()

  def draw(self):
    WINDOW.blit(self.picture, (self.x, self.y))
  
  def showHealthPoint(self):
    healthPointText = HEALTHPOINTFONT.render(str(self.hitpoints), 1, GREEN)
    WINDOW.blit(healthPointText, (self.x, self.y))

  def shoot(self, bullets):
    if self.fireCoolDown <= 0:
      ball = PlayerBullet(self.x + self.picture.get_width() / 2, self.y)
      bullets.append(ball)
      self.fireCoolDown = self.fireRate
      
  def checkCollision(self, tl, tr, bl, br, coord):
    return coord[0] >= tl[0] and coord[0] <= tr[0] and coord[1] >= tl[1] and coord[1] <= bl[1]

  def move(self, dx, dy):
    if dy < 0:
      self.y = max(0, self.y + dy * self.speed)
    else:
      self.y = min(WINDOW.get_height() - self.picture.get_height(), self.y + dy * self.speed)
    if dx < 0:
      self.x = max(0, self.x + dx * self.speed)
    else:
      self.x = min(WINDOW.get_width() - self.picture.get_width(), self.x + dx * self.speed)
  
  def speedUp(self, increase = 1):
    self.speed += increase
  
  def increaseFireRate(self, increase = 1):
    self.RPS += increase
    self.fireRate = int(FPS * (1 / self.RPS)) #frames per round
    self.fireCoolDown = self.fireRate
  
  def displayHealthDeduction(self, damage):
    if self.healthDeductionCD >= 0:
      healthDeductionText = HEALTHPOINTFONT.render(f"-{damage}", 1, GREEN)
      WINDOW.blit(healthDeductionText, (self.x + self.width, self.y))

  def executeBehaviour(self, keys, mouse, bullets):
    self.fireCoolDown -= 1
    if keys[pygame.K_w] or keys[pygame.K_UP]: self.move(0, -1)
    if keys[pygame.K_s] or keys[pygame.K_DOWN]: self.move(0, 1)
    if keys[pygame.K_a] or keys[pygame.K_LEFT]: self.move(-1, 0)
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]: self.move(1, 0)
    if mouse[0]: self.shoot(bullets)
    self.draw()
    self.showHealthPoint()
    
class PlayerBullet:
  speed = 5
  def __init__(self, x, y, damage = 1):
    self.rawPicture = pygame.image.load(f"{ASSETSPATH}red_circle.png")
    self.picture = pygame.transform.scale(self.rawPicture, (self.rawPicture.get_width() * 0.1, self.rawPicture.get_height() * 0.1))
    self.x = x - self.picture.get_width() / 2
    self.y = y
    self.width = self.picture.get_width()
    self.height = self.picture.get_height()
    self.alive = True
    self.damage = damage
    self.draw()
    
  def draw(self):
    WINDOW.blit(self.picture, (self.x, self.y))

  def executeBehaviour(self):
    self.y -= self.speed
    self.draw()

class Enemy:
  def __init__(self, x, speed = 1, hitpoints = 2, scale = 0.5):
    self.rawPicture = pygame.image.load(f"{ASSETSPATH}fighter_enemy_p51.png")
    self.picture = pygame.transform.scale(self.rawPicture, (self.rawPicture.get_width() * scale, self.rawPicture.get_height() * scale))
    self.width = self.picture.get_width()
    self.height = self.picture.get_height()
    if x >= WINDOW.get_width() - self.picture.get_width():
      self.x = WINDOW.get_width() - self.picture.get_width()
    else:
      self.x = x
    self.y = 0 - self.height
    self.hitpoints = hitpoints
    self.speed = speed
    self.healthDeductionCD = 30
    self.alive = True
    self.draw()

  def draw(self):
    WINDOW.blit(self.picture, (self.x, self.y))
  
  def showHealthPoint(self):
    healthPointText = HEALTHPOINTFONT.render(str(self.hitpoints), 1, DARKRED)
    WINDOW.blit(healthPointText, (self.x, self.y))
  
  def displayHealthDeduction(self, damage):
    if self.healthDeductionCD >= 0:
      healthDeductionText = HEALTHPOINTFONT.render(f"-{damage}", 1, DARKRED)
      WINDOW.blit(healthDeductionText, (self.x + self.width, self.y))

  def executeBehaviour(self):
    self.y += self.speed
    self.draw()
    self.showHealthPoint()

  def isOutOfScreen(self):
    return self.y > WINDOW.get_height()

def whiteBackground():
  WINDOW.fill(WHITE)

def grayBackground():
  WINDOW.fill(GRAY)

def startScreen():
  wallpaper = pygame.image.load(f"{ASSETSPATH}start_screen.png")
  WINDOW.blit(wallpaper, (0, 0))

def checkRun():
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      return False
  return True

def keyPressed(keys):
  return (keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d])

def spawnEnemies(enemies, enemyHealthDeduction):
  if randint(1, 10) == 1:
    en = Enemy(randint(0, WINDOW.get_width()))
    enemies.append(en)
    enemyHealthDeduction[en] = None
  if randint(1, 100) <= 20:
    en = Enemy(randint(0, WINDOW.get_width()), hitpoints = 50)
    enemies.append(en)
    enemyHealthDeduction[en] = None

def rectangleIsColliding(r1, r2):
  tl1, tr1, bl1, br1 = r1
  tl2, tr2, bl2, br2 = r2

  return not (bl1[1] < tl2[1] or tl1[0] > tr2[0] or tl1[1] > bl2[1] or tr1[0] < tl2[0])

def displayScore(score):
  scoreText = SCOREFONT.render(f"Score: {score[0]}", 1, BLACK)
  WINDOW.blit(scoreText, (10, 10))

def gameBehaviour(keys, mouse, player, bullets, enemies, spawnCoolDown, score, collisionCoolDown, enemyHealthDeduction, playerHealthDeduction):
  bulletPops, enPops = [], []
  spawnCoolDown[0] -= 1
  collisionCoolDown[0] -= 1
  if spawnCoolDown[0] < 0:
    spawnEnemies(enemies, enemyHealthDeduction)
    spawnCoolDown[0] = 20
  player.executeBehaviour(keys, mouse, bullets)
  playerVertices = ((player.x, player.y), (player.x + player.width, player.y), (player.x, player.y + player.height),(player.x + player.width, player.y + player.height))

  for index, bullet in enumerate(bullets):
    if bullet.y + bullet.picture.get_height() < 0 and bullet.alive:
      bullet.alive = False
      bulletPops.append(index)
    else:
      bullet.executeBehaviour()
      for index2, enemy in enumerate(enemies):
        enemyVertices = ((enemy.x, enemy.y), (enemy.x + enemy.width, enemy.y), (enemy.x, enemy.y + enemy.height), (enemy.x + enemy.width, enemy.y + enemy.height))
        bulletVertices = ((bullet.x, bullet.y), (bullet.x + bullet.width, bullet.y), (bullet.x, bullet.y + bullet.height), (bullet.x + bullet.width, bullet.y + bullet.height))
        if rectangleIsColliding(enemyVertices, bulletVertices):
          if bullet.alive:
            bullet.alive = False
            bulletPops.append(index)
          enemy.hitpoints -= bullet.damage
          enemyHealthDeduction[enemy] = bullet.damage
          if enemy.alive and enemy.hitpoints <= 0:
            enemy.alive = False
            enemyHealthDeduction.pop(enemy)
            enPops.append(index2)
  
  bulletTermination = [bullets[i] for i in bulletPops]
  for i in range(len(bulletTermination)):
    tmp = bulletTermination[i]
    bullets.remove(tmp)
    del tmp
  
  enemyTermination = [enemies[i] for i in enPops]
  for i in range(len(enemyTermination)):
    score[0] += 50
    tmp = enemyTermination[i]
    enemies.remove(tmp)
    del tmp
  
  bulletPops, enPops = [], []
  for index, enemy in enumerate(enemies):
    enemy.executeBehaviour()
    enemyVertices = ((enemy.x, enemy.y), (enemy.x + enemy.width, enemy.y), (enemy.x, enemy.y + enemy.height), (enemy.x + enemy.width, enemy.y + enemy.height))
    if rectangleIsColliding(playerVertices, enemyVertices):
      if collisionCoolDown[0] < 0:
        enemy.hitpoints -= 10
        player.hitpoints -= 10
        enemyHealthDeduction[enemy] = 10
        playerHealthDeduction[0] = 10
        collisionCoolDown[0] = 30
    if enemy.isOutOfScreen() or enemy.hitpoints <= 0:
      enemy.alive = False
      enemyHealthDeduction.pop(enemy)
      enPops.append(index)
  
  enemyTermination = [enemies[i] for i in enPops]
  for i in range(len(enemyTermination)):
    score[0] += 10
    tmp = enemyTermination[i]
    enemies.remove(tmp)
    del tmp
  
  for en, damage in enemyHealthDeduction.items():
    if damage is not None:
      if en.healthDeductionCD > 0:
        en.healthDeductionCD -= 1
        en.displayHealthDeduction(damage)
      else:
        en.healthDeductionCD = 30
        enemyHealthDeduction[en] = None
  
  if playerHealthDeduction[0] is not None:
    if player.healthDeductionCD > 0:
      player.healthDeductionCD -= 1
      player.displayHealthDeduction(playerHealthDeduction[0])
    else:
      player.healthDeductionCD = 30
      playerHealthDeduction[0] = None

  displayScore(score)
  
  if player.hitpoints <= 0:
    return "start screen"
  else:
    return "game"

PLAYBUTTON = Buttons(f"{ASSETSPATH}play.png", WINDOW.get_width() / 2, 100, 0.6)

def main():
  fps = pygame.time.Clock()
  game = "start screen"
  run = True
  spawnCoolDown, collisionCoolDown = [20], [30]
  
  while run:
    fps.tick(FPS)
    run = checkRun()
    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()

    if game == "start screen":
      startScreen()
      PLAYBUTTON.drawButton()
      if PLAYBUTTON.isClicked(mouse):
        grayBackground()
        player = PlayerFighter(4, 10)
        bullets, enemies, score, enemyHealthDeduction, playerHealthDeduction = [], [Enemy(WINDOW.get_width() / 2)], [0], {}, [None]
        game = "game"
      
    if game == "game":
      grayBackground()
      game = gameBehaviour(keys, mouse, player, bullets, enemies, spawnCoolDown, score, collisionCoolDown, enemyHealthDeduction, playerHealthDeduction)
      if keys[pygame.K_ESCAPE]: game = "start screen"
    
    pygame.display.flip()
  pygame.quit()

if __name__ == "__main__":
  main()