from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.properties import BooleanProperty, NumericProperty, StringProperty
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.gridlayout import GridLayout
import os
from datetime import datetime

# Проверка существования папки для данных
if not os.path.exists('data'):
    os.makedirs('data')


def save_login_state(state):
    with open('data/login_state.txt', 'w') as f:
        f.write(str(state))


def load_login_state():
    try:
        with open('data/login_state.txt', 'r') as f:
            return f.read() == 'True'
    except:
        return False


class CustomCalendar(BoxLayout):
    current_date = StringProperty(datetime.now().strftime('%B %Y'))

    def __init__(self, **kwargs):
        super(CustomCalendar, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = dp(10)
        self.padding = dp(10)
        self.update_calendar()

    def update_calendar(self, month=None, year=None):
        # Очищаем предыдущий календарь
        self.clear_widgets()

        # Добавляем заголовок с месяцем и годом
        header = BoxLayout(size_hint_y=None, height=dp(40))
        prev_btn = Button(text='<', size_hint_x=None, width=dp(40))
        next_btn = Button(text='>', size_hint_x=None, width=dp(40))
        month_label = Label(text=self.current_date, font_size=dp(20))

        header.add_widget(prev_btn)
        header.add_widget(month_label)
        header.add_widget(next_btn)
        self.add_widget(header)

        # Добавляем дни недели
        weekdays = BoxLayout(size_hint_y=None, height=dp(30))
        for day in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']:
            weekdays.add_widget(Label(text=day))
        self.add_widget(weekdays)

        # Добавляем дни месяца
        grid = GridLayout(cols=7, spacing=dp(2))
        now = datetime.now()
        first_day = datetime(now.year, now.month, 1)
        offset = first_day.weekday()  # 0-6 (понедельник-воскресенье)

        # Пустые ячейки для выравнивания
        for _ in range(offset):
            grid.add_widget(Label(text=''))

        # Добавляем дни месяца
        for day in range(1, 32):
            try:
                date = datetime(now.year, now.month, day)
                btn = Button(text=str(day), size_hint_y=None, height=dp(40))
                grid.add_widget(btn)
            except:
                break

        self.add_widget(grid)


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        with self.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            self.rect = Rectangle(size=Window.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

        layout = FloatLayout()

        # Логотип
        self.logo = Image(
            source='logo.png',
            size_hint=(None, None),
            size=(dp(128), dp(128)),
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )
        layout.add_widget(self.logo)

        # Поля ввода
        fields = [
            ('email', 'Email', 0.55),
            ('password', 'Password', 0.45),
            ('confirm_password', 'Confirm Password', 0.35),
            ('nickname', 'Nickname', 0.25)
        ]

        for field_name, hint_text, pos_y in fields:
            setattr(self, field_name, TextInput(
                size_hint=(None, None),
                size=(dp(250), dp(40)),
                pos_hint={'center_x': 0.5, 'center_y': pos_y},
                hint_text=hint_text,
                multiline=False,
                password=(field_name in ['password', 'confirm_password'])
            ))
            layout.add_widget(getattr(self, field_name))

        # Кнопка входа
        self.login_btn = Button(
            text='Login',
            size_hint=(None, None),
            size=(dp(250), dp(40)),
            pos_hint={'center_x': 0.5, 'center_y': 0.15},
            background_normal='',
            background_color=(0.2, 0.6, 1, 1)
        )
        self.login_btn.bind(on_press=self.try_login)
        layout.add_widget(self.login_btn)

        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def try_login(self, instance):
        if (self.email.text and self.password.text and
                self.confirm_password.text and self.nickname.text and
                self.password.text == self.confirm_password.text):
            save_login_state(True)
            self.manager.current = 'main'


class MainScreen(Screen):
    menu_open = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        with self.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            self.rect = Rectangle(size=Window.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        self.layout = FloatLayout()

        # Кнопка меню
        self.menu_btn = Button(
            size_hint=(None, None),
            size=(dp(64), dp(64)),
            pos_hint={'x': 0, 'top': 1},
            background_normal='menu.png',
            background_down='menu.png'
        )
        self.menu_btn.bind(on_press=self.toggle_menu)
        self.layout.add_widget(self.menu_btn)

        # Меню
        self.menu = FloatLayout(size_hint=(None, None), size=(dp(64), dp(64 * 4)))
        self.menu.pos_hint = {'x': 0, 'top': 1 - dp(64) / Window.size[1]}
        self.menu.opacity = 0

        # Кнопки меню
        menu_buttons = [
            ('calendar_btn', 'calendar.png', self.open_calendar, 2),
            ('settings_btn', 'settings.png', None, 3),
            ('logout_btn', 'logout.png', self.logout, 4)
        ]

        for btn_name, icon, callback, position in menu_buttons:
            btn = Button(
                size_hint=(None, None),
                size=(dp(64), dp(64)),
                pos_hint={'x': 0, 'top': 1 - dp(64 * position) / Window.size[1]},
                background_normal=icon,
                background_down=icon
            )
            if callback:
                btn.bind(on_press=callback)
            setattr(self, btn_name, btn)
            self.menu.add_widget(btn)

        self.layout.add_widget(self.menu)
        self.add_widget(self.layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def toggle_menu(self, instance):
        if self.menu_open:
            anim = Animation(opacity=0, duration=0.2)
            anim.bind(on_complete=lambda *args: setattr(self.menu_btn, 'background_normal', 'menu.png'))
        else:
            self.menu_btn.background_normal = 'close.png'
            anim = Animation(opacity=1, duration=0.2)

        # Блокируем кнопки во время анимации
        for btn in [self.calendar_btn, self.settings_btn, self.logout_btn]:
            btn.disabled = True

        anim.bind(on_complete=lambda *args: [setattr(btn, 'disabled', False)
                                             for btn in [self.calendar_btn, self.settings_btn, self.logout_btn]])
        anim.start(self.menu)
        self.menu_open = not self.menu_open

    def open_calendar(self, instance):
        self.manager.current = 'calendar'

    def logout(self, instance):
        save_login_state(False)
        self.manager.current = 'login'
        self.manager.transition = SlideTransition(direction='right')


class CalendarScreen(Screen):
    def __init__(self, **kwargs):
        super(CalendarScreen, self).__init__(**kwargs)

        with self.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            self.rect = Rectangle(size=Window.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        layout = FloatLayout()

        # Кнопка меню
        menu_btn = Button(
            size_hint=(None, None),
            size=(dp(64), dp(64)),
            pos_hint={'x': 0, 'top': 1},
            background_normal='menu.png',
            background_down='menu.png'
        )
        menu_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'main'))
        layout.add_widget(menu_btn)

        # Календарь
        calendar = CustomCalendar(
            size_hint=(0.9, 0.8),
            pos_hint={'center_x': 0.5, 'center_y': 0.45}
        )
        layout.add_widget(calendar)

        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class MyApp(App):
    def build(self):
        sm = ScreenManager()

        if load_login_state():
            sm.add_widget(MainScreen(name='main'))
            sm.add_widget(CalendarScreen(name='calendar'))
            sm.current = 'main'
        else:
            sm.add_widget(LoginScreen(name='login'))
            sm.add_widget(MainScreen(name='main'))
            sm.add_widget(CalendarScreen(name='calendar'))
            sm.current = 'login'

        return sm


if __name__ == '__main__':
    MyApp().run()