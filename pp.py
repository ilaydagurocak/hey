
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.core.window import Window
from random import randint
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen

class Game(Widget):
    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)
        self.player = Image(source='scared_emoji.png')
        self.add_widget(self.player)

        self.fire1 = Image(source='fire_emoji.png', pos=(randint(0, Window.width - 50), Window.height))
        self.add_widget(self.fire1)

        self.fire2 = Image(source='fire_emoji.png', pos=(randint(0, Window.width - 50), Window.height))
        self.add_widget(self.fire2)

        self.score_label = Label(text='Score: 0', pos=(Window.width * 0.85, Window.height - 100), font_size=60)
        self.add_widget(self.score_label)

        self.score = 0
        self.speed = 10

        self.game_event = Clock.schedule_interval(self.update, 1/60.)

    def on_touch_move(self, touch):
        self.player.x = min(max(touch.x - self.player.width // 2, 0), Window.width - self.player.width)

    def update(self, dt):
        for fire in [self.fire1, self.fire2]:
            fire.y -= self.speed
            if fire.y < 0:
                fire.pos = (randint(0, Window.width - 50), Window.height)
                self.score += 1
                self.score_label.text = f'Score: {self.score}'
                self.speed += 0.2

            if self.player.collide_widget(fire):
                self.game_over()

    def game_over(self):
        self.game_event.cancel()
        restart_button = Button(text='Restart')
        close_button = Button(text='Close')
        box = BoxLayout(orientation='vertical')
        box.add_widget(restart_button)
        box.add_widget(close_button)
        popup = Popup(title='Game Over', 
                      content=box,
                      size_hint=(None, None), size=(400, 200))
        close_button.bind(on_release=App.get_running_app().stop)
        restart_button.bind(on_release=self.restart_game)
        restart_button.bind(on_release=popup.dismiss)
        popup.open()

    def restart_game(self, instance):
        for fire in [self.fire1, self.fire2]:
            fire.pos = (randint(0, Window.width - 50), Window.height)
        self.score = 0
        self.score_label.text = 'Score: 0'
        self.speed = 10
        self.game_event = Clock.schedule_interval(self.update, 1/60.)

class StartScreen(Screen):
    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
        play_button = Button(text='Play', background_color=(1, 0, 0, 1), color=(1,1,1,1), size_hint=(.2, .1), pos_hint={'center_x':.5, 'center_y': .5})
        play_button.bind(on_press=self.start_game)
        self.add_widget(play_button)

    def start_game(self, instance):
        self.manager.current = 'game'

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.game = Game()
        self.add_widget(self.game)

class GameApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(StartScreen(name='start'))
        sm.add_widget(GameScreen(name='game'))
        return sm

if __name__ == '__main__':
    GameApp().run()
