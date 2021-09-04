import cocos
from cocos.sprite import Sprite
from pyaudio import PyAudio, paInt16
import struct
from player import Player
from block import Block
import time
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
        self.txt_score = cocos.text.Label(u'score：0', font_name="-Layiji Lenroonrang",font_size=20,color=(255, 0, 255, 255))
        self.txt_score.position = 400, 440
        self.add(self.txt_score, 99999)

        self.highest_score = 0
        self.txt_highest_score = cocos.text.Label(u'High Score：0',font_name="-Layiji Lenroonrang", font_size=20,color=(255,0, 0, 255))
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
        
        # voice input
        pa = PyAudio()
        SAMPLING_RATE = int(pa.get_device_info_by_index(0)['defaultSampleRate'])
        self.stream = pa.open(format=paInt16, channels=1, rate=SAMPLING_RATE, input=True, frames_per_buffer=self.NUM_SAMPLES)

        self.schedule(self.update)

    def on_mouse_press(self, x, y, buttons, modifiers):
        pass

    def update(self,dt):
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
        if self.score > self.highest_score:
            self.highest_score = self.score
        self.txt_highest_score.element.text = u'High score：%d' % self.highest_score
        self.score = 0
        self.txt_score.element.text = u'score: 0'


cocos.director.director.init(caption="Game start")
cocos.director.director.run(cocos.scene.Scene(VoiceGame()))
