from tkinter import Tk

from pynput.keyboard import KeyCode, Key, Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener, Button, Controller as MouseController

from pywebostv.controls import WebOSControlBase


class BlockingWindow(Tk):
    def __init__(self, mouse: MouseController):
        super().__init__()
        self.mouse = mouse
        self.update_idletasks()
        self.attributes('-fullscreen', True)
        self.state('iconic')
        geometry = self.winfo_geometry()
        resolution, self.offset_x, self.offset_y = tuple(x if 'x' in x else int(x) for x in geometry.split('+'))
        self.display_width, self.display_height = tuple(int(x) for x in resolution.split('x'))
        self.initial_x = self.display_width / 2 + self.offset_x
        self.initial_y = self.display_height / 2 + self.offset_y
        self.current_x = self.initial_x
        self.current_y = self.initial_y
        mouse.position = (self.initial_x, self.initial_y)

    def _does_exceed_left_boundary(self, x):
        offset_x = self.offset_x

        return x < offset_x

    def _does_exceen_lower_boundary(self, y):
        offset_y = self.offset_y
        return y < offset_y

    def _does_exceed_right_boundary(self, x):
        display_width = self.display_width
        offset_x = self.offset_x

        return x > display_width + offset_x

    def _does_exceed_upper_boundary(self, y):
        display_height = self.display_height
        offset_y = self.offset_y

        return y > display_height + offset_y

    def enforce_boundary(self, x, y):
        mouse = self.mouse
        display_width = self.display_width
        display_height = self.display_height
        offset_x = self.offset_x
        offset_y = self.offset_y
        current_x = self.current_x
        current_y = self.current_y

        if self._does_exceed_left_boundary(x):
            current_x = offset_x
        if self._does_exceed_right_boundary(x):
            current_x = display_width + offset_x
        if self._does_exceen_lower_boundary(y):
            current_y = offset_y
        if self._does_exceed_upper_boundary(y):
            current_y = display_height + offset_y

        mouse.position = (current_x, current_y)
        self.current_x = current_x
        self.current_y = current_y

    def is_out_of_bounds(self, x, y):
        display_width = self.display_width
        display_height = self.display_height
        offset_x = self.offset_x
        offset_y = self.offset_y
        
        return x < offset_x or x > display_width + offset_x or y < offset_y or y > display_height + offset_y


class MouseAgent:
    def __init__(self, input_control: WebOSControlBase, blocking_window: BlockingWindow):
        self._input_control = input_control
        self._blocking_window = blocking_window

    def listen(self):
        blocking_window = self._blocking_window
        input_control = self._input_control

        with self._create_listener() as listener:
            input_control.connect_input()
            input_control.move(0, 0, block=True)
            listener.join()
            input_control.disconnect_input()

        blocking_window.destroy()

    def on_click(self, x, y, button, pressed):
        input_control = self._input_control

        if button == Button.right:
            return False
        pressed and input_control.click(block=True)

    def on_move(self, x, y):
        blocking_window = self._blocking_window

        if blocking_window.is_out_of_bounds(x, y):
            blocking_window.enforce_boundary(x, y)
        else:
            self._move_mouse(x, y)

    def _create_listener(self):
        return MouseListener(on_move=self.on_move, on_click=self.on_click)

    def _move_mouse(self, x, y):
        blocking_window = self._blocking_window
        input_control = self._input_control
        current_x = blocking_window.current_x
        current_y = blocking_window.current_y

        relative_x = x - current_x
        relative_y = y - current_y

        input_control.move(relative_x, relative_y, block=True)
        blocking_window.current_x = x
        blocking_window.current_y = y


class KeyboardAgent:
    def __init__(self, input_control: WebOSControlBase, blocking_window: BlockingWindow):
        self._input_control = input_control
        self._blocking_window = blocking_window

    def listen(self):
        mouse_listener = self._create_mouse_listener()
        blocking_window = self._blocking_window

        mouse_listener.start()
        with self._create_keyboard_listener() as keyboard_listener:
            keyboard_listener.join()
        mouse_listener.stop()
        blocking_window.destroy()

    def on_mouse_move(self, x, y):
        blocking_window = self._blocking_window

        if blocking_window.is_out_of_bounds(x, y):
            blocking_window.enforce_boundary(x, y)

    def on_press(self, key):
        input_control = self._input_control

        if isinstance(key, KeyCode):
            input_control.type(key.char, block=True)
        elif key == Key.backspace:
            input_control.delete(1, block=True)
        elif key == Key.space:
            input_control.type(' ', block=True)
        elif key == Key.enter:
            input_control.enter(block=True)
        elif key == Key.esc:
            return False

    def _create_keyboard_listener(self):
        return KeyboardListener(on_press=self.on_press)

    def _create_mouse_listener(self):
        return MouseListener(on_move=self.on_mouse_move)
