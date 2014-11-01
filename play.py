import pyglet
import random
import os
import sys

VIDEO_DIR = "videos"

MOTION_FILE = "/tmp/motion_event"

FILLER = None
ACTIONS = []

for v in os.listdir(VIDEO_DIR):
    if v.startswith("."): continue
    fname = os.path.join(VIDEO_DIR, v)
    if v.lower().startswith("filler"):
        if FILLER is None:
            FILLER = fname
        else:
            print >>sys.stderr, "There are multiple filler files. I don't know what to do"
            exit(1)
    else:
        ACTIONS.append(fname)

assert FILLER is not None


try:
    os.unlink(MOTION_FILE)
except OSError:
    pass


window = pyglet.window.Window(visible=True, fullscreen=True)
#window = pyglet.window.Window(visible=True)
idle_player = pyglet.media.Player()
# For some reason, EOS_LOOP hangs in my computer.
# Workaround, I'll just add the FILLER twice
# to the idle_player's playlist, and then again
# every time the playlist advances 
# (idle_player.event on_eos)
#idle_player.eos_action = idle_player.EOS_LOOP
idle_player.queue(pyglet.media.load(FILLER))
idle_player.queue(pyglet.media.load(FILLER))
idle_player.volume = 0.0
idle_player.play()


action_player = pyglet.media.Player()
# Add the action videos in random order to the playlist
#random.shuffle(ACTIONS)
for action in ACTIONS:
    action_player.queue(pyglet.media.load(action))
# And then one more. We want to ensure that there is always
# a "next" video in the playlist to avoid delays between
# videos. Actions are added to the playlist as old ones are
# used (idle_player.event on_eos)
action_player.queue(pyglet.media.load(random.choice(ACTIONS)))
action_player.pause()
is_active = False

@window.event
def on_draw():
    # Maybe we could blend the idle and action textures
    # to provide for smoother transitons 
    # (or to have dynamic backgrounds if we have
    # green-screen action videos).
    # Maybe in the future.
    if is_active:
        texture = action_player.get_texture()
    else:
        texture = idle_player.get_texture()
    w,h = window.get_size()
    if texture is not None:
        texture.blit(0, 0, width=w, height=h)

@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.A:
        play_action()
    if symbol == pyglet.window.key.ESCAPE:
        global finished
        finished = True

def play_action():
    action_player.play()
    global is_active
    is_active = True

@idle_player.event
def on_eos():
    idle_player.queue(pyglet.media.load(FILLER))

@action_player.event
def on_eos():
    global is_active
    action_player.queue(pyglet.media.load(random.choice(ACTIONS)))
    action_player.pause()
    try:
        os.unlink(MOTION_FILE)
    except OSError:
        pass
    is_active = False

finished = False

while not finished:
    pyglet.clock.tick()
    if os.path.isfile(MOTION_FILE):
        play_action()

    for window in pyglet.app.windows:
        window.switch_to()
        window.dispatch_events()
        window.dispatch_event('on_draw')
        window.flip()


