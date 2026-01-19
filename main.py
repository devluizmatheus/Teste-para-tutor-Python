import pgzrun
import random
from room import Room, Portal, Enemy
from player import Wizard, Fireball

WIDTH = 780 
HEIGHT = 600
TILE_SIZE = 32 

MAX_WAVES = 5
wave = 0
vitoria = False
fireballs = []
enemies = []
portals = []

sala_atual = Room(20, 15)
OFFSET_X = (WIDTH - (sala_atual.width * TILE_SIZE)) // 2
OFFSET_Y = (HEIGHT - (sala_atual.height * TILE_SIZE)) // 2

mago = Wizard(((4 * TILE_SIZE) + OFFSET_X, (3 * TILE_SIZE) + OFFSET_Y))

def start_wave():
    """Gerencia a transição de ondas e dificuldade."""
    global wave, vitoria
    
    if wave < MAX_WAVES:
        wave += 1
        for pos in sala_atual.spawners:
            portals.append(Portal(pos))

        clock.schedule_unique(spawn_enemies, 2.0)
    else:
        if not enemies and not portals:
            vitoria = True

def spawn_enemies():
    """Cria os inimigos com base na onda atual."""
    for p in portals:
        quantidade = 1 + (wave // 2) 
        
        for _ in range(quantidade):

            spawn_pos = (p.x + random.randint(-15, 15), p.y + random.randint(-15, 15))
            inimigo = Enemy(spawn_pos)
            
            inimigo.speed = 0.4 + (wave * 0.5) 
            enemies.append(inimigo)
            
    portals.clear()

def draw():
    screen.clear()
    sala_atual.draw(screen)
    
    for p in portals: p.draw()
    for f in fireballs: f.draw()
    for e in enemies: e.draw()
    mago.draw()
    
    screen.draw.text(f"ONDA: {wave} / {MAX_WAVES}", (20, 20), fontsize=30, shadow=(1,1))
    
    if vitoria:
        screen.draw.text("DUNGEON CONQUISTADA!", center=(WIDTH//2, HEIGHT//2), fontsize=60, color="gold")
        screen.draw.text("Pressione R para jogar novamente", center=(WIDTH//2, HEIGHT//2 + 60), fontsize=30)
    
    if mago.is_dead:
        screen.draw.text("FIM DE JOGO", center=(WIDTH//2, HEIGHT//2), fontsize=60, color="red")
        screen.draw.text("Pressione R para tentar de novo", center=(WIDTH//2, HEIGHT//2 + 60), fontsize=30)

def update():
    global vitoria

    if vitoria or mago.is_dead:
        mago.update_animation()
        if keyboard.r:
            reiniciar_jogo()
        return

    if not enemies and not portals:
        start_wave()

    mago.move(keyboard) 
    mago.update_animation()
    
    if keyboard.j:
        mago.attack()


    if mago.state == "attack" and mago.frame == 2 and mago.anim_timer == 0:
        f = Fireball(mago.pos, mago.look_dir) 
        fireballs.append(f)

    for f in fireballs[:]:
        f.update()
        
        if f.x < 0 or f.x > WIDTH or f.y < 0 or f.y > HEIGHT:
            fireballs.remove(f)
            continue

        for e in enemies[:]:
            if f.colliderect(e):
                enemies.remove(e)
                if f in fireballs: fireballs.remove(f)
                break

    for e in enemies:
        e.update(mago.pos)
        if e.colliderect(mago):
            mago.morrer()

def reiniciar_jogo():
    global fireballs, enemies, portals, wave, vitoria
    wave = 0
    vitoria = False
    enemies.clear()
    portals.clear()
    fireballs.clear()
    
    mago.is_dead = False
    mago.is_attacking = False 
    mago.is_hurting = False  
    mago.state = "idle"
    mago.frame = 0
    mago.anim_timer = 0
    mago.pos = ((4 * TILE_SIZE) + OFFSET_X, (3 * TILE_SIZE) + OFFSET_Y)

    mago.look_dir = "right"

pgzrun.go()