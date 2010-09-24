#!/usr/bin/env python
# - coding: utf-8 -
import gtk
import pango
from lib import graphics
from lib.pytweener import Easing

class HoverSprite(graphics.Sprite):
    def __init__(self):
        graphics.Sprite.__init__(self, x=70, y=40, interactive=True)

        self._style = gtk.MenuItem().rc_get_style()

        self.font_desc = pango.FontDescription(gtk.Style().font_desc.to_string())
        self.font_desc.set_size(12 * pango.SCALE)

        self.fill = self._style.bg[gtk.STATE_NORMAL]
        self.over = self._style.bg[gtk.STATE_SELECTED]
        self.out = self._style.bg[gtk.STATE_NORMAL]
        self.text = self._style.text[gtk.STATE_NORMAL]
        self.width = 100
        self.height = 20
        self.connect("on-mouse-over", self.on_mouse_over)
        self.connect("on-mouse-out", self.on_mouse_out)
        self.connect("on-render", self.on_render)

    def on_render(self, sprite):
        self.graphics.rectangle(0, 0, self.width, self.height, 3)
        self.graphics.fill(self.fill)

        self.graphics.set_color(self.text)
        self.graphics.show_layout('Overview', self.font_desc)

    def on_mouse_over(self, sprite):
        self.fill = self.over # set to red on hover
        self.text = self._style.text[gtk.STATE_SELECTED]

    def on_mouse_out(self, sprite):
        self.fill = self.out # set back the color once the mouse leaves area
        self.text = self._style.text[gtk.STATE_NORMAL]

class Scene(graphics.Scene):
    def __init__(self):
        graphics.Scene.__init__(self)

        icon = graphics.Image("1.png")
        icon.connect('on-click', self.on_icon_click)
        self.add_child(icon) # remember to add sprites to the scene

        icon = graphics.Image("2.png", pivot_x=32, pivot_y=32, interactive=True)
        icon.connect('on-click', self.on_icon_click)
        self.add_child(icon) # remember to add sprites to the scene

        icon = graphics.Image("3.png")
        self.add_child(icon) # remember to add sprites to the scene
        
#        style = self.style
#        base, fg, bg, text = style.base, style.fg, style.bg, style.text
#        color = str(text[gtk.STATE_NORMAL])
#        label = graphics.Label("Ubuntu Tweak", 12, '#fff', x = 70, y = 5, interactive=True)
#        label.connect('on-click', self.on_text_click)
#        self.add_child(label) # remember to add sprites to the scene
        self.add_child(HoverSprite())

    def on_icon_click(self, sprite, event):
        if not sprite: return #ignore blank clicks

        if self.tweener.get_tweens(sprite): #must be busy
            return

        def bring_back(sprite):
            self.animate(sprite, rotation = 0)

        sprite.original_x = sprite.x
        self.animate(sprite, rotation = 8, duration = 1, on_complete = bring_back)

    def on_text_click(self, sprite, event):
        if not sprite: return #ignore blank clicks

        if self.tweener.get_tweens(sprite): #must be busy
            return

        def bring_back(sprite):
            self.animate(sprite, y = 5, scale_x = 1, scale_y = 1, x = sprite.original_x, easing = Easing.Bounce.ease_out)

        sprite.original_x = sprite.x
        self.animate(sprite, y = 150, scale_x = 2, x = sprite.x - 20, scale_y = 2, on_complete = bring_back)

class RightScene(graphics.Scene):
    def __init__(self):
        graphics.Scene.__init__(self)

        icon = graphics.Icon("gnome-desktop-config", 24, x=5, y=40)
        self.add_child(icon) # remember to add sprites to the scene

style = gtk.MenuBar().rc_get_style()
window = gtk.Window(gtk.WINDOW_TOPLEVEL)
window.connect('destroy', lambda *w: gtk.main_quit())
window.set_title("Ubuntu Tweak 0.6")
window.set_default_size(480, 320)

vbox = gtk.VBox(False, 0)
inter_hbox = gtk.HBox(False, 0)
vbox.pack_start(inter_hbox, False, False, 0)

scen = Scene()
scen.set_style(style)
inter_hbox.pack_start(scen, True, True, 0)

right = RightScene()
right.set_style(style)
inter_hbox.pack_start(right, False, False, 0)

window.add(vbox)
#window.set_style(style)

hbox = gtk.HBox(False, 12)
vbox.pack_start(hbox)

button = gtk.Button("Hello")
hbox.pack_start(button, False, False, 0)

label = gtk.Label("label")
hbox.pack_start(label, False, False, 0)

window.show_all()
gtk.main()
