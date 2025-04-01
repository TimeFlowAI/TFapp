from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import BooleanProperty, NumericProperty, StringProperty
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

# Установим размер окна для разработки
Window.size = (360, 640)


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        # Главный контейнер
        main_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))

        # Отступ сверху
        main_layout.add_widget(BoxLayout(size_hint=(1, 0.2)))

        # Логотип
        self.logo = Image(
            source='logo.png',
            size_hint=(None, None),
            size=(dp(128), dp(128)),
            pos_hint={'center_x': 0.5}
        )
        main_layout.add_widget(self.logo)

        # Отступ
        main_layout.add_widget(Label(size_hint=(1, 0.05)))

        # Контейнер для полей ввода
        input_layout = BoxLayout(orientation='vertical', spacing=dp(10))

        # Поля ввода
        self.email_input = TextInput(
            hint_text='Email',
            size_hint=(1, None),
            height=dp(50),
            multiline=False
        )

        self.nickname_input = TextInput(
            hint_text='Никнейм',
            size_hint=(1, None),
            height=dp(50),
            multiline=False
        )

        self.password_input = TextInput(
            hint_text='Пароль',
            size_hint=(1, None),
            height=dp(50),
            multiline=False,
            password=True
        )

        self.confirm_password_input = TextInput(
            hint_text='Подтвердите пароль',
            size_hint=(1, None),
            height=dp(50),
            multiline=False,
            password=True
        )

        # Добавляем поля ввода
        input_layout.add_widget(self.email_input)
        input_layout.add_widget(self.nickname_input)
        input_layout.add_widget(self.password_input)
        input_layout.add_widget(self.confirm_password_input)

        # Кнопка входа
        self.login_button = Button(
            text='ВОЙТИ',
            size_hint=(1, None),
            height=dp(50),
            background_color=(0.2, 0.6, 1, 1),
            disabled=True
        )
        self.login_button.bind(on_press=self.attempt_login)

        # Добавляем виджеты в основной layout
        main_layout.add_widget(input_layout)
        main_layout.add_widget(self.login_button)

        # Привязываем изменения в полях ввода к проверке формы
        inputs = [
            self.email_input,
            self.nickname_input,
            self.password_input,
            self.confirm_password_input
        ]
        for input_field in inputs:
            input_field.bind(text=self.validate_form)

        self.add_widget(main_layout)

    def validate_form(self, *args):
        """Активирует кнопку входа только когда все поля заполнены и пароли совпадают"""
        all_filled = all([
            self.email_input.text.strip(),
            self.nickname_input.text.strip(),
            self.password_input.text.strip(),
            self.confirm_password_input.text.strip()
        ])

        passwords_match = (self.password_input.text == self.confirm_password_input.text)

        self.login_button.disabled = not (all_filled and passwords_match)

    def attempt_login(self, instance):
        """Обработка входа"""
        # Здесь должна быть проверка учетных данных
        # Пока просто переходим на главный экран
        self.manager.current = 'main'


class DropDownMenu(BoxLayout):
    is_open = BooleanProperty(False)
    menu_height = NumericProperty(0)

    def __init__(self, **kwargs):
        super(DropDownMenu, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (None, None)
        self.width = dp(64)
        self.pos_hint = {'top': 1, 'left': 1}
        self.spacing = dp(10)
        self.padding = [dp(10), dp(10), dp(10), dp(10)]

        # Кнопка календаря
        self.calendar_btn = Button(
            size_hint=(None, None),
            size=(dp(64), dp(64)),
            background_normal='calendar_icon.png',
            background_down='calendar_icon.png'
        )

        # Кнопка настроек
        self.settings_btn = Button(
            size_hint=(None, None),
            size=(dp(64), dp(64)),
            background_normal='settings_icon.png',
            background_down='settings_icon.png'
        )

        # Кнопка выхода
        self.logout_btn = Button(
            size_hint=(None, None),
            size=(dp(64), dp(64)),
            background_normal='logout_icon.png',
            background_down='logout_icon.png'
        )

        # Добавляем кнопки
        self.add_widget(self.calendar_btn)
        self.add_widget(self.settings_btn)
        self.add_widget(self.logout_btn)

        # Начальное состояние - закрыто
        self.height = 0
        self.opacity = 0

    def toggle_menu(self):
        """Анимация открытия/закрытия меню"""
        if self.is_open:
            anim = Animation(height=0, opacity=0, duration=0.2)
        else:
            anim = Animation(height=dp(220), opacity=1, duration=0.2)

        anim.start(self)
        self.is_open = not self.is_open


class MenuButton(Button):
    def __init__(self, **kwargs):
        super(MenuButton, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(64), dp(64))
        self.pos_hint = {'top': 1, 'left': 1}
        self.background_normal = 'menu_icon.png'
        self.background_down = 'menu_icon.png'


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        # Основной layout
        layout = FloatLayout()

        # Кнопка меню
        self.menu_button = MenuButton()
        self.menu_button.bind(on_press=self.toggle_menu)
        layout.add_widget(self.menu_button)

        # Выпадающее меню
        self.dropdown_menu = DropDownMenu()
        layout.add_widget(self.dropdown_menu)

        # Привязываем кнопки меню
        self.dropdown_menu.calendar_btn.bind(on_press=self.open_calendar)
        self.dropdown_menu.settings_btn.bind(on_press=self.open_settings)
        self.dropdown_menu.logout_btn.bind(on_press=self.logout)

        # Текст приветствия
        self.welcome_label = Label(
            text='Добро пожаловать!',
            font_size=24,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        layout.add_widget(self.welcome_label)

        self.add_widget(layout)

    def toggle_menu(self, instance):
        """Переключает меню и меняет иконку кнопки"""
        self.dropdown_menu.toggle_menu()

        if self.dropdown_menu.is_open:
            self.menu_button.background_normal = 'close_icon.png'
            self.menu_button.background_down = 'close_icon.png'
        else:
            self.menu_button.background_normal = 'menu_icon.png'
            self.menu_button.background_down = 'menu_icon.png'

    def open_calendar(self, instance):
        """Открывает экран календаря"""
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'calendar'

    def open_settings(self, instance):
        """Открывает экран настроек"""
        pass  # Реализуйте позже

    def logout(self, instance):
        """Выход из аккаунта"""
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'login'


class CalendarScreen(Screen):
    def __init__(self, **kwargs):
        super(CalendarScreen, self).__init__(**kwargs)

        # Основной layout
        layout = FloatLayout()

        # Кнопка меню
        self.menu_button = MenuButton()
        self.menu_button.bind(on_press=self.toggle_menu)
        layout.add_widget(self.menu_button)

        # Выпадающее меню
        self.dropdown_menu = DropDownMenu()
        layout.add_widget(self.dropdown_menu)

        # Привязываем кнопки меню
        self.dropdown_menu.calendar_btn.bind(on_press=self.open_calendar)
        self.dropdown_menu.settings_btn.bind(on_press=self.open_settings)
        self.dropdown_menu.logout_btn.bind(on_press=self.logout)

        # Здесь будет календарь (заглушка)
        calendar_label = Label(
            text='Календарь будет здесь',
            font_size=24,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        layout.add_widget(calendar_label)

        self.add_widget(layout)

    def toggle_menu(self, instance):
        """Переключает меню и меняет иконку кнопки"""
        self.dropdown_menu.toggle_menu()

        if self.dropdown_menu.is_open:
            self.menu_button.background_normal = 'close_icon.png'
            self.menu_button.background_down = 'close_icon.png'
        else:
            self.menu_button.background_normal = 'menu_icon.png'
            self.menu_button.background_down = 'menu_icon.png'

    def open_calendar(self, instance):
        """Уже на экране календаря"""
        self.dropdown_menu.toggle_menu()

    def open_settings(self, instance):
        """Открывает экран настроек"""
        pass  # Реализуйте позже

    def logout(self, instance):
        """Выход из аккаунта"""
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'login'


class MyApp(App):
    logged_in = BooleanProperty(False)

    def build(self):
        # Создаем менеджер экранов
        self.sm = ScreenManager()

        # Добавляем экраны
        self.sm.add_widget(LoginScreen(name='login'))
        self.sm.add_widget(MainScreen(name='main'))
        self.sm.add_widget(CalendarScreen(name='calendar'))

        # Проверяем статус входа
        if not self.logged_in:
            self.sm.current = 'login'
        else:
            self.sm.current = 'main'

        return self.sm


if __name__ == '__main__':
    MyApp().run()