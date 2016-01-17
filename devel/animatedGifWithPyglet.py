# load and show an animated gif file using module pyglet
# download module pyglet from: http://www.pyglet.org/download.html
# the animated dinosaur-07.gif file is in the public domain
# download from http://www.gifanimations.com
# tested with Python2.5 and pyglet1.1a2  by  vegaseat   22apr2008
from tkFileDialog import askopenfilename,askopenfile
import os
import pyglet

# pick an animated gif file you have in the working directory
basedir = ".."
imagedir = os.path.join(basedir, "images")
animdir = os.path.join(imagedir, "animated_gifs","girls")

options = {}
options['defaultextension'] = '.gif'
#options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
options['filetypes'] = [('gif files', '.gif')]
options['initialdir'] = animdir
#options['parent'] = self
options['title'] = "Open a gif file"
ag_file = askopenfile(mode='rb', **options)
#print str(ag_file.name)

if ag_file:
    animation = pyglet.image.load_animation(ag_file.name)
    sprite = pyglet.sprite.Sprite(animation)
    # create a window and set it to the image size
    win = pyglet.window.Window(width=sprite.width, height=sprite.height)
    # set window background color = r, g, b, alpha
    # each value goes from 0.0 to 1.0
    green = 0, 1, 0, 1
    pyglet.gl.glClearColor(*green)
    @win.event

    def on_draw():
        win.clear()
        sprite.draw()

    pyglet.app.run()