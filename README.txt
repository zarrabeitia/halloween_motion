This is motion-activated video player I hacked together for Halloween.

It plays a filler video in a loop. When a motion event is detected, the
filler video is replace by some "action" video.

Requirements:
  - Linux
  - Motion: http://www.lavrsen.dk/foswiki/bin/view/Motion/WebHome
  - python-pyglet
  - avbin (required to play the videos in pyglet, package libavbin0 in ubuntu)

Usage:
1. Place your videos in the videos/ directory. The filler video /must/ be 
   named "filler.<extension>". The rest are the action videos. Do not put
   anything else here. Hidden files (starting with ".") will be ignored,
   the rest will be used.
2. Start motion with the provided configuration file (you may need to edit it
   to point to your camera), then start the play.py script. Or run 
   the halloween.sh helper script.
3. During playback, press ESC to finish, "A" to simulate a motion event
   (useful for debugging).

Details:

The play.py program doesn't directly detect motion. Instead, it looks for a
trigger file (/tmp/motion_event), if it exists, activates the action
event. After the action event is done, it deletes the trigger file and
waits for it again. The provided motion.conf file configures Motion to 
create the trigger.

This means that you don't need "Motion" to trigger it. Any program that
can "touch /tmp/motion_event" can serve as a trigger.

I don't own the copyright for the videos I used, you may be able to find
nice clips on youtube or purchase them elsewhere. 
https://www.youtube.com/user/AtmosfearFX seems to have a nice 
(but not free) collection.

There is a lot of room for improvement. I couldn't spend more than an
hour writing this code before trick-or-treating began, and that included
learning to use pyglet and cutting up the clips.

* The filler clip is stopped, and the action clip is started, immediately
  after the trigger is fired. If you need finish playing the filler clip
  (e.g., to ensure a smooth transition), you can move the trigger check
  from the main loop to the idle_player.event on_eos.

* I didn't want to worry about looping the filler sound, so I muted the filler
  clip. Change the volume if you wish (from 0.0 -- muted, to 1.0 -- full volume)


