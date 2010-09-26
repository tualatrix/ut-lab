#!/usr/bin/env python
# - coding: utf-8 -
import gtk
import pango
import cairo
from lib import graphics
from lib.pytweener import Easing

class Menu(graphics.Sprite):
    def __init__(self, text, icon=None, **kwargs):
        graphics.Sprite.__init__(self, interactive=True, **kwargs)

        self._style = gtk.MenuItem().rc_get_style()

        self.font_desc = pango.FontDescription(gtk.Style().font_desc.to_string())
        self.font_desc.set_size(12 * pango.SCALE)

        self.fill = self._style.bg[gtk.STATE_NORMAL]
        self.over = self._style.bg[gtk.STATE_SELECTED]
        self.out = self._style.bg[gtk.STATE_NORMAL]
        self.text_color = self._style.text[gtk.STATE_NORMAL]
        self.width = 120
        self.height = 24

        self.icon_sprite = graphics.Icon(icon)
        self.add_child(self.icon_sprite)

        self.label_sprite = graphics.Label(text, color=self.text_color, x=26)
        self.add_child(self.label_sprite)
        self._over = False
        self._clicked = False

        self.connect("on-mouse-over", self.on_mouse_over)
        self.connect("on-mouse-out", self.on_mouse_out)
        self.connect('on-click', self.on_button_press_event)
        self.connect("on-render", self.on_render)

    def on_render(self, sprite):
        if self._over or self._clicked:
            pat = cairo.LinearGradient (0, 0,  0, self.height)
            pat.add_color_stop_rgba (0, 0, 0, 0, 0)
            pat.add_color_stop_rgba (1, self.over.red_float, self.over.green_float, self.over.blue_float, 0.5)

            self.graphics.rectangle(0, 0, self.width, self.height, 3)
            self.graphics.set_source(pat)
            self.graphics.fill()
        else:
            self.graphics.rectangle(0, 0, self.width, self.height, 3)
            self.graphics.fill(self.out)

    def on_button_press_event(self, widget, event):
        self._clicked = not self._clicked

    def on_mouse_over(self, sprite):
        self.fill = self.over # set to red on hover
        self._over = True
        self.label_sprite.color = self._style.text[gtk.STATE_SELECTED]

    def on_mouse_out(self, sprite):
        self.fill = self.out # set back the color once the mouse leaves area
        self._over = False
        self.label_sprite.color = self._style.text[gtk.STATE_NORMAL]

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
        menu1 = Menu('Overview', icon='gnome-app-install', x=70, y=40)
        self.add_child(menu1)

        menu2 = Menu('Application', icon='ubuntu-tweak', x=200, y=40)
        self.add_child(menu2)

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
