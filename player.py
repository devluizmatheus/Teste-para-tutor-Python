from pgzero.actor import Actor

class Wizard(Actor):
    def __init__(self, pos): 
        self.base_name = "mage"
        super().__init__(f'{self.base_name}_idle0', pos)
        
        self.frame = 0
        self.anim_timer = 0
        self.speed = 3
        self.state = "idle"
        self.is_hurting = False
        self.is_attacking = False
        self.look_dir = (1, 0) # Direção padrão (direita)
        self.is_dead = False

    def attack(self):
        if not self.is_attacking and not self.is_hurting:
            self.is_attacking = True
            self.state = "attack"
            self.frame = 0
            self.anim_timer = 0
            return True
        return False

    def move(self, keyboard):
        if self.is_hurting or self.is_attacking:
            return

        moving = False
        dx, dy = 0, 0

        if keyboard.a: 
            dx = -1; moving = True
            self.look_dir = "left"   # Define como texto
        elif keyboard.d: 
            dx = 1; moving = True
            self.look_dir = "right"  # Define como texto
        elif keyboard.w: 
            dy = -1; moving = True
            self.look_dir = "up"     # Define como texto
        elif keyboard.s: 
            dy = 1; moving = True
            self.look_dir = "down"   # Define como texto

        if moving:
            self.x += dx * self.speed
            self.y += dy * self.speed

    def take_damage(self):
        if not self.is_dead:
            self.hp -= 1
            if self.hp <= 0:
                self.die()
            else:
                self.is_hurting = True
                self.state = "hurt"
                self.frame = 0

    def die(self):
        self.is_dead = True
        self.state = "death"
        self.frame = 0
        self.anim_timer = 0

    def update_animation(self):
        self.anim_timer += 1
        
        # Define a velocidade baseada no estado
        if self.state == "attack":
            limit = 4
        elif self.state == "death":
            limit = 12
        else:
            limit = 10
            
        if self.anim_timer >= limit:
            self.anim_timer = 0
            
            if self.state == "death":
                if self.frame < 2: # Trava no último frame da morte
                    self.frame += 1
            elif self.state == "attack":
                self.frame += 1
                if self.frame > 3: 
                    self.is_attacking = False
                    self.state = "idle"
                    self.frame = 0
            elif self.state == "hurt":
                self.frame += 1
                if self.frame > 1:
                    self.is_hurting = False
                    self.state = "idle"
                    self.frame = 0
            else:
                self.frame = (self.frame + 1) % 4
            
            self.image = f'{self.base_name}_{self.state}{self.frame}'

    def morrer(self):
        if not self.is_dead:
            self.is_dead = True
            self.state = "death"
            self.frame = 0
            self.anim_timer = 0
            
class Fireball(Actor):
    def __init__(self, pos, direcao):
        super().__init__('fireball', pos)
        self.direcao = direcao
        self.speed = 8

    def update(self):
        if self.direcao == "left":
            self.x -= self.speed
        elif self.direcao == "right":
            self.x += self.speed
        elif self.direcao == "up":
            self.y -= self.speed
        elif self.direcao == "down":
            self.y += self.speed
        else:
            # Caso o mago atire sem ter se movido ainda, vai para a direita por padrão
            self.x += self.speed