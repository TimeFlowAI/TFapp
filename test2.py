from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.animation import Animation
from kivy.properties import BooleanProperty, NumericProperty
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.clock import Clock

Window.size = (430, 932)
Window.clearcolor = (28/255, 86/255, 170/255, 1)#(140/255, 184/255, 227/255, 1)#(28/255, 86/255, 170/255, 1)





class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        main_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        main_layout.add_widget(BoxLayout(size_hint=(1, 0.2)))

        self.logo = Image(
            source='logo.png',
            size_hint=(None, None),
            size=(dp(256), dp(256)),
            pos_hint={'center_x': 0.5}
        )
        main_layout.add_widget(self.logo)
        main_layout.add_widget(Label(size_hint=(1, 0.05)))

        input_layout = BoxLayout(orientation='vertical', spacing=dp(10))
        self.inputs = []

        for hint, is_password in [('Email', False), ('Никнейм', False),
                                  ('Пароль', True), ('Подтверждение пароля', True)]:
            input_field = TextInput(
                hint_text=hint,
                size_hint=(1, None),
                height=dp(50),
                multiline=False,
                password=is_password
            )
            input_layout.add_widget(input_field)
            self.inputs.append(input_field)

        self.login_button = Button(
            text='ВОЙТИ',
            size_hint=(1, None),
            height=dp(50),
            background_color=(0.2, 0.6, 1, 1),
            disabled=True
        )
        self.login_button.bind(on_press=self.attempt_login)

        main_layout.add_widget(input_layout)
        main_layout.add_widget(self.login_button)

        for input_field in self.inputs:
            input_field.bind(text=self.validate_form)

        self.add_widget(main_layout)

    def validate_form(self, *args):
        all_filled = all(field.text.strip() for field in self.inputs)
        passwords_match = (self.inputs[2].text == self.inputs[3].text)
        self.login_button.disabled = not (all_filled and passwords_match)

    def attempt_login(self, instance):
        self.manager.current = 'main'


class MenuButton(Button):
    def __init__(self, **kwargs):
        super(MenuButton, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(64), dp(64))
        self.pos_hint = {'top': 1, 'left': 1}
        self.background_normal = 'menu_icon.png'
        self.background_down = 'menu_icon.png'
        self.last_press_time = 0

    def on_touch_down(self, touch):
        current_time = Clock.get_time()
        if self.collide_point(*touch.pos) and (current_time - self.last_press_time) > 0.3:
            self.last_press_time = current_time
            return super(MenuButton, self).on_touch_down(touch)
        return False


class DropDownMenu(BoxLayout):
    is_open = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(DropDownMenu, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (None, None)
        self.width = dp(64)
        self.pos_hint = {'top': 0.9, 'left': 1}
        self.spacing = dp(10)
        self.padding = [dp(0), dp(10), dp(0), dp(10)]

        # Кнопки меню
        self.calendar_btn = Button(
            size_hint=(None, None),
            size=(dp(64), dp(64)),
            background_normal='calendar_icon.png',
            background_down='calendar_icon.png'
        )

        self.settings_btn = Button(
            size_hint=(None, None),
            size=(dp(64), dp(64)),
            background_normal='settings_icon.png',
            background_down='settings_icon.png'
        )

        self.logout_btn = Button(
            size_hint=(None, None),
            size=(dp(64), dp(64)),
            background_normal='logout_icon.png',
            background_down='logout_icon.png'
        )

        self.add_widget(self.calendar_btn)
        self.add_widget(self.settings_btn)
        self.add_widget(self.logout_btn)

        self.height = 0
        self.opacity = 0

        # Блокируем кнопки при инициализации
        self.set_buttons_state(False)

    def set_buttons_state(self, active):
        """Активирует или деактивирует кнопки меню"""
        for btn in [self.calendar_btn, self.settings_btn, self.logout_btn]:
            btn.disabled = not active

    def toggle(self):
        target_height = dp(220) if not self.is_open else 0
        target_opacity = 1 if not self.is_open else 0

        if not self.is_open:
            # При открытии сначала анимация, потом активация кнопок
            anim = Animation(height=target_height, opacity=target_opacity, duration=0.2)
            anim.bind(on_complete=lambda *x: self.set_buttons_state(True))
        else:
            # При закрытии сначала деактивация кнопок, потом анимация
            self.set_buttons_state(False)
            anim = Animation(height=target_height, opacity=target_opacity, duration=0.2)

        anim.start(self)
        self.is_open = not self.is_open


class BaseScreen(Screen):
    def __init__(self, **kwargs):
        super(BaseScreen, self).__init__(**kwargs)
        self.layout = FloatLayout()

        # Кнопка меню
        self.menu_button = MenuButton()
        self.menu_button.bind(on_press=self.toggle_menu)
        self.layout.add_widget(self.menu_button)

        # Выпадающее меню
        self.dropdown_menu = DropDownMenu()
        self.layout.add_widget(self.dropdown_menu)

        self.add_widget(self.layout)

    def toggle_menu(self, instance):
        self.dropdown_menu.toggle()

        if self.dropdown_menu.is_open:
            self.menu_button.background_normal = 'close_icon.png'
            self.menu_button.background_down = 'close_icon.png'
        else:
            self.menu_button.background_normal = 'menu_icon.png'
            self.menu_button.background_down = 'menu_icon.png'


class MainScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        self.title_label = Label(
            text='Главный экран',
            font_size=24,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.layout.add_widget(self.title_label)

        self.dropdown_menu.calendar_btn.bind(on_press=self.open_calendar)
        self.dropdown_menu.settings_btn.bind(on_press=self.open_settings)
        self.dropdown_menu.logout_btn.bind(on_press=self.logout)

    def open_calendar(self, instance):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'calendar'
        self.toggle_menu(self.menu_button)

    def open_settings(self, instance):
        pass

    def logout(self, instance):
        # Добавляем подтверждение выхода
        from kivy.uix.popup import Popup
        from kivy.uix.boxlayout import BoxLayout

        content = BoxLayout(orientation='vertical', spacing=10)
        content.add_widget(Label(text='Вы уверены, что хотите выйти?'))

        btn_layout = BoxLayout(spacing=10)
        yes_btn = Button(text='Да', size_hint=(0.5, None), height=dp(50))
        no_btn = Button(text='Нет', size_hint=(0.5, None), height=dp(50))

        btn_layout.add_widget(no_btn)
        btn_layout.add_widget(yes_btn)
        content.add_widget(btn_layout)

        popup = Popup(title='Подтверждение выхода',
                      content=content,
                      size_hint=(0.7, 0.4))

        no_btn.bind(on_press=popup.dismiss)
        yes_btn.bind(on_press=lambda x: self.confirm_logout(popup))

        popup.open()

    def confirm_logout(self, popup):
        popup.dismiss()
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'login'
        self.toggle_menu(self.menu_button)


class CalendarScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(CalendarScreen, self).__init__(**kwargs)

        self.title_label = Label(
            text='Календарь',
            font_size=24,
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )
        self.layout.add_widget(self.title_label)

        calendar_placeholder = Label(
            text='Виджет календаря будет здесь',
            font_size=16,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.layout.add_widget(calendar_placeholder)

        self.dropdown_menu.calendar_btn.bind(on_press=self.close_menu)
        self.dropdown_menu.settings_btn.bind(on_press=self.open_settings)
        self.dropdown_menu.logout_btn.bind(on_press=self.logout)

    def close_menu(self, instance):
        self.toggle_menu(self.menu_button)

    def open_settings(self, instance):
        pass

    def logout(self, instance):
        from kivy.uix.popup import Popup
        from kivy.uix.boxlayout import BoxLayout

        content = BoxLayout(orientation='vertical', spacing=10)
        content.add_widget(Label(text='Вы уверены, что хотите выйти?'))

        btn_layout = BoxLayout(spacing=10)
        yes_btn = Button(text='Да', size_hint=(0.5, None), height=dp(50))
        no_btn = Button(text='Нет', size_hint=(0.5, None), height=dp(50))

        btn_layout.add_widget(no_btn)
        btn_layout.add_widget(yes_btn)
        content.add_widget(btn_layout)

        popup = Popup(title='Подтверждение выхода',
                      content=content,
                      size_hint=(0.7, 0.4))

        no_btn.bind(on_press=popup.dismiss)
        yes_btn.bind(on_press=lambda x: self.confirm_logout(popup))

        popup.open()

    def confirm_logout(self, popup):
        popup.dismiss()
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'login'
        self.toggle_menu(self.menu_button)


class MyApp(App):
    logged_in = BooleanProperty(False)

    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(LoginScreen(name='login'))
        self.sm.add_widget(MainScreen(name='main'))
        self.sm.add_widget(CalendarScreen(name='calendar'))
        self.sm.current = 'login' if not self.logged_in else 'main'
        return self.sm


if __name__ == '__main__':
    MyApp().run()