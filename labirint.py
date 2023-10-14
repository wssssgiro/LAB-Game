from pygame import *
#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
   # конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
       # Вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)
       # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
  
       # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
   # метод, отрисовывающий героя на окне
    def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
   #метод, в котором реализовано управление спрайтом по кнопкам стрелочкам клавиатуры
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed,player_y_speed):
       # Вызываем конструктор класса (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y,size_x, size_y)
  
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed
    def update(self):
        ''' перемещает персонажа, применяя текущую горизонтальную и вертикальную скорость'''
       # сначала движение по горизонтали
        if packman.rect.x <= win_width - 80 and packman.x_speed > 0 or packman.rect.x >= 0 and packman.x_speed < 0:
            self.rect.x += self.x_speed 
        # елси зашли за стенку то встанем плотно к ней
        platform_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for p in platform_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in platform_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        if packman.rect.y <= win_height - 80 and packman.y_speed > 0 or packman.rect.y >= 0 and packman.y_speed < 0:       
            self.rect.y += self.y_speed
        platform_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:
            for p in platform_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.y_speed < 0:
            for p in platform_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)
    def fire(self):
        bullet = Bullet('weapon.png', self.rect.right, self.rect.centery, 30, 25, 15)
        bullets.add(bullet)
class Enemy(GameSprite):
    side = 'left'
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed

    def update(self):
        if self.rect.x <= 420:
            self.side = 'right'
        if self.rect.x >= win_width - 85:
            self.side = 'left'
        if self.side == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
class Bullet(GameSprite):
    side = 'left'
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > win_width+10:
            self.kill()
#Создаем окошко
win_width = 700
win_height = 500
display.set_caption("sdf")
window = display.set_mode((win_width, win_height))
back = (89, 1, 8)#задаем цвет согласно цветовой схеме RGB
#сОЗДАНИЕ ГРУППЫ СТЕН
barriers = sprite.Group()
#ГРУПЫ ПУЛЬ
bullets = sprite.Group()
#ГРУППЫ МОНСТРОВ
monsters = sprite.Group()
#создаем стены картинки
w1 = GameSprite('platform_h.png', 100, win_height / 2, 500, 50)
w2 = GameSprite('platform_v.png', 370, 100, 50, 400)
w3 = GameSprite('platform_h.png', -60, 100, 300, 50)
w4 = GameSprite('platform_h.png', 500, 100, 300, 50)
#добавление стенны в группу
barriers.add(w1)
barriers.add(w2)
barriers.add(w3)
barriers.add(w4)
#создаем спрайты
packman = Player('sf.png', 5, win_height - 80, 80, 80, 0, 0)
monster1 = Enemy('antimage.png', 0, 0, 50, 80, 2)
monster2 = Enemy('antimage.png', win_width - 80, 300, 80, 80, 5)
final_spite = GameSprite('enemy2.png', 430, win_height - 100, 80, 80)

monsters.add(monster1)
monsters.add(monster2)
#оканчаение игры
finish = False
#игровой цикл   
run = True
while run:
   #цикл срабатывает каждую 0.05 секунд
    time.delay(35)
  
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                packman.x_speed = -5
            elif e.key == K_RIGHT:
                packman.x_speed = 5
            elif e.key == K_UP:
                packman.y_speed = -5
            elif e.key == K_DOWN:
                packman.y_speed = 5
            elif e.key == K_SPACE:
                packman.fire()
        elif e.type == KEYUP:
            if e.key == K_LEFT:
                packman.x_speed = 0
            elif e.key == K_RIGHT:
                packman.x_speed = 0
            elif e.key == K_UP:
                packman.y_speed = 0
            elif e.key == K_DOWN:
                packman.y_speed = 0
    if not finish:
        window.fill(back)
        #ДВИЖЕНИЕ
        packman.update()
        bullets.update()
        #рисуем объекты
        w1.reset()
        w2.reset()
        w3.reset()
        w4.reset()
        barriers.draw(window)
        bullets.draw(window)
        final_spite.reset()
        packman.reset()

        sprite.groupcollide(monsters, bullets, True, True)
        monsters.update()
        monsters.draw(window)
        sprite.groupcollide(bullets, barriers, True, False)

        if sprite.spritecollide(packman, monsters, False):
            finish = True
            img = image.load('game-over_1.jpg')
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (700, win_height)), (0, 0))
        if sprite.collide_rect(packman, final_spite):
            finish = True
            img = image.load('thumb.jpg')
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_width, win_height)), (0, 0))
    display.update()