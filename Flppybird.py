import pygame as py
import math, random
py.init()
win = py.display.set_mode((300, 500))


class Pipe:
    pipe1img = py.image.load("pipe.png")
    pipe2img = py.transform.flip(pipe1img, False, True)

    def __init__(self, x):
        self.x = x
        self.y1 = random.randrange(140, 360)
        self.y2 = self.y1 - 410
        self.space = 190
        self.stop = False

    def move(self):
        if not self.stop:
            self.x -= 5

    def draw(self):
        win.blit(Pipe.pipe1img, (self.x, self.y1))
        win.blit(Pipe.pipe2img, (self.x, self.y2))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = py.mask.from_surface(self.pipe2img)
        bottom_mask = py.mask.from_surface(self.pipe1img)
        top_offset = (self.x - bird.x, self.y2 - round(bird.y) - 10)
        bottom_offset = (self.x - bird.x, self.y1 - round(bird.y) + 10)
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)
        if b_point or t_point:
            return True

        return False


class Bird:
    birdimgs = [py.image.load("bird1.png"), py.image.load("bird2.png"), py.image.load("bird3.png")]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.jumpspd = 10
        self.timecount = 0
        self.tilt = 0
        self.start = False
        self.img = self.birdimgs[0]
        self.hit = False
        self.stop = False

    def draw(self):
        self.timecount += 1
        if self.timecount < 3:
            self.img = self.birdimgs[0]
        elif self.timecount < 6:
            self.img = self.birdimgs[1]
        elif self.timecount < 9:
            self.img = self.birdimgs[2]
        elif self.timecount == 9:
            self.img = self.birdimgs[0]
            self.timecount = 0
        if self.tilt <= -80:
                self.img = self.birdimgs[1]
                self.timecount = 3
        rotated_image = py.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)

        win.blit(rotated_image, new_rect.topleft)

    def move(self):
        if
        self.y -= (self.jumpspd * 5+5 + abs(self.jumpspd)) * 0.2
        self.jumpspd -= 2
        if not self.hit:
            if py.mouse.get_pressed() == (1, 0, 0):
                self.jumpspd = 10
        if self.jumpspd > -15:
            self.tilt = 25
        else:
            if self.tilt > -90:
                self.tilt -= 15

    def get_mask(self):
        return py.mask.from_surface(self.img)


class Base:
    img = py.image.load("base.png")
    Width = img.get_width()

    def __init__(self, y):
        self.ximg1 = 0
        self.y = y
        self.ximg2 = 336
        self.vel = 5
        self.stop = False

    def draw(self):
        win.blit(Base.img, (self.ximg1, self.y))
        win.blit(Base.img, (self.ximg2, self.y))

    def move(self):
        if not self.stop:
            self.ximg1 -= self.vel
            self.ximg2 -= self.vel
            if self.ximg1 + 336 <0:
                self.ximg1 = self.ximg2 + 336
            if self.ximg2 + 336 < 0:
                self.ximg2 = self.ximg1 + 336


def setting(FPS, title):
    py.display.set_caption(title)
    Fps = py.time.Clock()
    Fps.tick(FPS)


def text(text, size, color, pos):
    font = py.font.SysFont("comicsans", size, True)
    display = font.render(text, 10, color)
    win.blit(display, pos)


def main():
    base = Base(400)
    bird = Bird(100, 240)
    pipe = Pipe(400)
    pipeloop = [pipe]
    gamerun = True
    score = 0
    bg = py.image.load("bg.png")
    bg = py.transform.scale(bg, (300, 500))
    while gamerun:
        setting(30, "Flappy bird")
        for event in py.event.get():
            if event.type == py.QUIT:
                gamerun = False
            if py.mouse.get_pressed() == (1, 0, 0):
                bird.start = True
        win.blit(bg, (0, 0))
        if bird.start:
            for i in pipeloop:
                i.draw()
                text(f"{score}", 35, (255, 253, 235), (145, 100))
                if 303>i.x + i.space >= 300 :
                    pipeloop.append(Pipe(i.x + i.space))
                if bird.y  <0:
                    bird.y = 0
                    bird.jumpspd = 0
                if bird.x +20 == i.x and not bird.hit:
                    score += 1
                if i.collide(bird):
                    bird.hit = True
                if bird.hit or bird.y > 390:

                    base.stop = True
                    if bird.y > 390:
                        h = 0
                        while h < 100:
                            py.time.delay(10)
                            h += 1
                        pipeloop.clear()
                        pipeloop.append(pipe)
                        pipe.x = 500
                        bird.y = 230
                        bird.tilt = 0
                        score = 0
                        base.stop = False
                        bird.hit = False
                        bird.start = False
                else:
                    i.move()
            bird.draw()
            base.draw()
            base.move()
            bird.move()
        else:
            text("click to start", 35, (255, 110, 20), (60, 150))
            bird.draw()
            base.draw()
            base.move()
        py.display.update()


main()
