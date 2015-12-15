import pyglet_example

game_window = pyglet_example.window.Window()

@game_window.event
def on_draw():
    game_window.clear()

def update(dt):
    pass

if __name__ == '__main__':
    pyglet_example.clock.schedule_interval(update, 0.5)
    pyglet_example.app.run()

