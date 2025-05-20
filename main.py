from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import unlit_shader
import time, sys

app = Ursina(borderless=True)
window.exit_button.visible = False
window.title = "Minecraft Python"
window.color = color.rgb(135, 206, 235)

textures = {
    "grass": load_texture("grass.png"),
    "stone": load_texture("stone.png"),
    "brick": load_texture("brick.png"),
    "dirt": load_texture("dirt.png")
}
block_types = list(textures.keys())
selected_block = 0

crosshair = Entity(
    parent=camera.ui,
    model='quad',
    color=color.black,
    scale=0.01
)

player = FirstPersonController()
player.gravity = 0.05
player.cursor.visible = False
player.speed = 7

can_fly = False
last_jump_time = 0
inventory_ui = None

def toggle_fly():
    global can_fly
    can_fly = not can_fly
    player.gravity = 0 if can_fly else 0.5
    print("Fly activé" if can_fly else "Fly désactivé")

class Voxel(Button):
    def __init__(self, position=(0,0,0), texture='grass'):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=0.5,
            texture=textures[texture],
            color=color.white,
            scale=1
        )
        self.block_type = texture

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                destroy(self)
            if key == 'right mouse down':
                Voxel(position=self.position + mouse.normal, texture=block_types[selected_block])


for x in range(-30, 31):
    for z in range(-30, 31):
        Voxel(position=(x, 0, z), texture='stone')

def open_inventory():
    global inventory_ui
    if inventory_ui:
        destroy(inventory_ui)
        inventory_ui = None
        mouse.locked = True
        player.enabled = True
        return

    inventory_ui = Entity(parent=camera.ui)
    mouse.locked = False
    player.enabled = False

    for i, block in enumerate(block_types):
        btn = Button(
            parent=inventory_ui,
            model='quad',
            color=color.gray,
            position=Vec3(-0.6 + i * 0.3, 0.4, 0),
            scale=Vec2(0.2, 0.1),
            text=block.upper(),  
            on_click=Func(select_block, i)
        )
        btn.shader = unlit_shader

def select_block(index):
    global selected_block
    selected_block = index
    print(f"Bloc sélectionné : {block_types[selected_block]}")

def input(key):
    global last_jump_time

    if key == 'e':
        open_inventory()
    elif key == 'delete':
        sys.exit()
    elif key == 'space':
        now = time.time()
        if now - last_jump_time < 0.3:
            toggle_fly()
        last_jump_time = now

def update():
    if can_fly:
        if held_keys['space']:
            player.y += 5 * time.dt
        if held_keys['left shift']:
            player.y -= 5 * time.dt

app.run()
