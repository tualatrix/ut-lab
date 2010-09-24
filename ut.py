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

        self.text = text
        self.image_data = None
        self.theme = gtk.icon_theme_get_default()
        self.icon_name = icon

        self._surface = None
        self._style = gtk.MenuItem().rc_get_style()

        self.font_desc = pango.FontDescription(gtk.Style().font_desc.to_string())
        self.font_desc.set_size(12 * pango.SCALE)

        self.fill = self._style.bg[gtk.STATE_NORMAL]
        self.over = self._style.bg[gtk.STATE_SELECTED]
        self.out = self._style.bg[gtk.STATE_NORMAL]
        self.text_color = self._style.text[gtk.STATE_NORMAL]
        self.width = 100
        self.height = 20
        self.connect("on-mouse-over", self.on_mouse_over)
        self.connect("on-mouse-out", self.on_mouse_out)
        self.connect("on-render", self.on_render)

    def on_render(self, sprite):
        print 'on_render'
        self.graphics.rectangle(0, 0, self.width, self.height, 3)
        self.graphics.fill(self.fill)

        self.graphics.set_color(self.text_color)
        self.graphics.show_layout(self.text, self.font_desc, 24)

    def __setattr__(self, name, val):
        graphics.Sprite.__setattr__(self, name, val)
        if name == 'icon_name':
            if self.__dict__.get('icon_name'):
                self.image_data = self.theme.load_icon(self.icon_name, 24, 0)
            else:
                self.image_data = None

    def _draw(self, context, opacity = 1):
        if self.image_data is None or self.width is None or self.height is None:
            return

        if not self._surface:
            # caching image on surface similar to the target
            self._surface = context.get_target().create_similar(cairo.CONTENT_COLOR_ALPHA,
                                                               self.image_data.get_width(),
                                                               self.image_data.get_height())


            local_context = gtk.gdk.CairoContext(cairo.Context(self._surface))
            if isinstance(self.image_data, gtk.gdk.Pixbuf):
                local_context.set_source_pixbuf(self.image_data, 0, 0)
            else:
                local_context.set_source_surface(self.image_data)
            local_context.paint()

            # add instructions with the resulting surface
            self.graphics.set_source_surface(self._surface)
            self.graphics.paint()
            self.graphics.rectangle(0, 0, self.width, self.height)

        graphics.Sprite._draw(self,  context, opacity)

    def on_mouse_over(self, sprite):
        self.fill = self.over # set to red on hover
        self.text_color = self._style.text[gtk.STATE_SELECTED]

    def on_mouse_out(self, sprite):
        self.fill = self.out # set back the color once the mouse leaves area
        self.text_color = self._style.text[gtk.STATE_NORMAL]

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

        menu2 = Menu('Application', x=160, y=40)
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
