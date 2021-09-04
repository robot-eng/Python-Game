
import cocos
import pyglet
from pyaudio import PyAudio, paInt16
import time
from cocos.sprite import Sprite
import struct
from player import Player
from block import Block


class TitleMenu(cocos.menu.Menu):
    def __init__(self):
        super(TitleMenu, self).__init__('2D GAME!')
        self.font_title['font_name'] = 'Bauhaus 93'
        self.font_title['font_size'] = 60
        self.font_title['color'] = (255, 120, 120, 255)
        self.font_item['font_name'] = 'Nordic Alternative'
        self.font_item['font_size'] = 37
        self.font_item['color'] = (0, 0, 0, 150)
        self.font_item_selected['font_name'] = 'Bauhaus 93'
        self.font_item_selected['font_size'] = 40
        self.font_item_selected['color'] = (0, 0, 0, 255)
        item1 = cocos.menu.MenuItem('New Game', self.on_new_game)
        item2 = cocos.menu.MenuItem('Option', self.on_option)
        item3 = cocos.menu.MenuItem('Quit', self.on_quit)
        self.create_menu([item1, item2, item3],
                         layout_strategy=cocos.menu.fixedPositionMenuLayout(
                             [(320, 175), (320, 125), (320, 75)]
        ))

    def on_new_game(self):
        self.parent.switch_to(2)

    def on_option(self):
        self.parent.switch_to(1)

    def on_quit(self):

        pyglet.app.exit()


class new_game(cocos.menu.Menu):
    def __init__(self):
        super(new_game, self).__init__('Choose Game')

        self.font_title['font_name'] = 'ONE DAY'
        self.font_title['font_size'] = 60
        self.font_title['color'] = (255, 120, 120, 255)
        self.font_item['font_name'] = 'Bauhaus 93'
        self.font_item['font_size'] = 37
        self.font_item['color'] = (0, 0, 0, 150)
        self.font_item_selected['font_name'] = 'ONE DAY'
        self.font_item_selected['font_size'] = 40
        self.font_item_selected['color'] = (0, 0, 0, 255)
        item1 = cocos.menu.MenuItem('Game2D use voice', self.twod_Game)
        item3 = cocos.menu.MenuItem('Back', self.on_back)
        self.create_menu([item1, item3], layout_strategy=cocos.menu.fixedPositionMenuLayout(
            [(320, 125), (320, 75)]))

    def twod_Game(self):
        cocos.director.director.run(cocos.scene.Scene(VoiceGame()))

    def on_back(self):
        self.parent.switch_to(0)


class OptionMenu(cocos.menu.Menu):
    def __init__(self):
        super(OptionMenu, self).__init__('Windows')
        self.font_title['font_name'] = 'Bauhaus 93'
        self.font_title['font_size'] = 60
        self.font_title['color'] = (255, 120, 120, 255)
        self.font_item['font_name'] = 'Bauhaus 93'
        self.font_item['font_size'] = 37
        self.font_item['color'] = (0, 0, 0, 150)
        self.font_item_selected['font_name'] = 'Bauhaus 93'
        self.font_item_selected['font_size'] = 40
        self.font_item_selected['color'] = (0, 0, 0, 255)
        item1 = cocos.menu.MenuItem('Full Screen', self.on_full_screen)
        item2 = cocos.menu.MenuItem('Back', self.on_back)
        self.create_menu([item1, item2], layout_strategy=cocos.menu.fixedPositionMenuLayout(
            [(320, 125), (320, 75)]))

    def on_full_screen(self):
        cocos.director.director.window.set_fullscreen(
            not cocos.director.director.window.fullscreen
        )

    def on_back(self):
        self.parent.switch_to(0)


class TitleBackGround(cocos.layer.ColorLayer):
    def __init__(self):
        super(TitleBackGround, self).__init__(255, 255, 255, 255)


class VoiceGame(cocos.layer.ColorLayer):
    is_event_handler = True

    def __init__(self):
        super(VoiceGame, self).__init__(255, 255, 255, 255, 800, 600)

        # init voice
        self.NUM_SAMPLES = 1000
        self.LEVEL = 1000
        self.init_time = time.time()
        self.highest_score = 0
        self.score = 0
        self.txt_score = cocos.text.Label(
            u'score：0', font_name="-Layiji Lenroonrang", font_size=20, color=(255, 0, 255, 255))
        self.txt_score.position = 400, 440
        self.add(self.txt_score, 99999)

        self.highest_score = 0
        self.txt_highest_score = cocos.text.Label(
            u'High Score：0', font_name="-Layiji Lenroonrang", font_size=20, color=(255, 0, 0, 255))
        self.txt_highest_score.position = 200, 440
        self.add(self.txt_highest_score, 99999)
        self.voicebar = Sprite('block.png', color=(0, 255, 0))
        self.voicebar.position = 20, 450
        self.voicebar.scale_y = 0.1
        self.voicebar.image_anchor = 0, 0
        self.add(self.voicebar)

        self.player = Player()
        self.add(self.player)

        self.floor = cocos.cocosnode.CocosNode()
        self.add(self.floor)
        pos = 0, 100
        for i in range(100):
            b = Block(pos)
            self.floor.add(b)
            pos = b.x + b.width, b.height

        pa = PyAudio()
        SAMPLING_RATE = int(pa.get_device_info_by_index(0)
                            ['defaultSampleRate'])
        self.stream = pa.open(format=paInt16, channels=1, rate=SAMPLING_RATE, input=True,
                              frames_per_buffer=self.NUM_SAMPLES)

        self.schedule(self.update)

    def on_mouse_press(self, x, y, buttons, modifiers):
        pass

    def update(self, dt):
        # read voice simple
        string_audio_data = self.stream.read(self.NUM_SAMPLES)
        time_temp = time.time() - self.init_time
        self.init_time = time.time()
        self.score += time_temp / 10
        self.txt_score.element.text = u'score：%d' % self.score
        k = max(struct.unpack('1000h', string_audio_data))
        self.voicebar.scale_x = k / 10000.0
        if k > 3000:
            self.floor.x -= min((k / 20.0), 150) * dt
            self.txt_score.element.text = u'score：%d' % self.score
            self.score += 1 / 10
        if k > 8000:
            self.player.jump((k - 8000) / 1000.0)
            self.score += 1 / 10
            self.txt_score.element.text = u'score：%d' % self.score
        self.collide()

    def collide(self):
        px = self.player.x - self.floor.x
        for b in self.floor.get_children():
            if b.x <= px + self.player.width * 0.8 and px + self.player.width * 0.2 <= b.x + b.width:
                if self.player.y < b.height:
                    self.player.land(b.height)
                    break

    def reset(self):
        self.floor.x = 0
        time.sleep(1.2)
        a = cocos.scene.Scene()
        a.add(resett(), z=3)
        a.add(TitleBackGround(), z=0)
        cocos.director.director.run(a)
        if self.score > self.highest_score:
            self.highest_score = self.score
        self.txt_highest_score.element.text = u'High score：%d' % self.highest_score
        self.score = 0
        self.txt_score.element.text = u'score: 0'


class resett(cocos.menu.Menu):
    def __init__(self):
        super(resett, self).__init__('ReseT')
        self.font_title['font_name'] = 'Bauhaus 93'
        self.font_title['font_size'] = 60
        self.font_title['color'] = (255, 120, 120, 255)

        self.font_item['font_name'] = 'Bauhaus 93'
        self.font_item['font_size'] = 37
        self.font_item['color'] = (0, 0, 0, 150)
        self.font_item_selected['font_name'] = 'Bauhaus 93'
        self.font_item_selected['font_size'] = 40
        self.font_item_selected['color'] = (0, 0, 0, 255)
        item1 = cocos.menu.MenuItem('RESET', self.resettt)
        item2 = cocos.menu.MenuItem('Back', self.on_back)
        self.create_menu([item1, item2], layout_strategy=cocos.menu.fixedPositionMenuLayout(
            [(320, 125), (320, 75)]))

    def resettt(self):
        cocos.director.director.run(cocos.scene.Scene(VoiceGame()))

    def on_back(self):
        cocos.director.director.run(s)


class BackGround(cocos.layer.ScrollableLayer):
    def __init__(self):
        super().__init__()
        bg = cocos.sprite.Sprite("52.png")
        self.add(bg)


if __name__ == '__main__':
    pyglet.font.add_directory('resource')
    cocos.director.director.init(caption="Game2D start")
    s = cocos.scene.Scene()
    s.add(cocos.layer.MultiplexLayer(TitleMenu(), OptionMenu(), new_game()), z=1)
    s.add(TitleBackGround(), z=0)
    cocos.director.director.run(s)
