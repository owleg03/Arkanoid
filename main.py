import random
import tkinter as tk
from PIL import ImageTk as itk

WIDTH = 720
HEIGHT = 512
CANVAS_WIDTH = WIDTH - 80
CANVAS_HEIGHT = 50
WINDOW_GEOMETRY = f'{WIDTH}x{HEIGHT}+150+150'
RUNNER_WINDOW_SIZE = '200x50'
BAR_ARROW_MOVEMENT_INCREMENT = 20
FONT_LABEL = ('Bungee', 20)


class MultiWindowApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Images
        self.play_button_image = itk.PhotoImage(file='./images/play_button.png')
        self.help_button_image0 = itk.PhotoImage(file='images/help_button0.png')
        self.help_button_image1 = itk.PhotoImage(file='./images/help_button1.png')
        self.main_menu_button_image = itk.PhotoImage(file='./images/main_menu_button.png')
        self.back_button_image = itk.PhotoImage(file='images/back_button.png')
        self.retry_button_image = itk.PhotoImage(file='images/retry_button.png')
        self.main_menu_bg_image = itk.PhotoImage(file='images/main_menu_bg.png')
        self.help_bg_image = itk.PhotoImage(file='images/help_bg.png')
        self.level_bg_image = itk.PhotoImage(file='images/level_bg.png')
        self.game_over_bg_image = itk.PhotoImage(file='images/game_over_bg.png')
        self.bar_image = itk.PhotoImage(file='images/bar_image.png')

        self.main_frame = None
        self.current_window = None
        self.open_previous_window = None
        self.canvas = None
        self.bar = None
        self.mouse_control_enabled = False
        self.score = 0
        self.score_label = None

        self.create_main_window()
        self.open_main_menu()

        self.title('Arkanoid runner')
        self.geometry(RUNNER_WINDOW_SIZE)

    def create_main_window(self):
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        label = tk.Label(self.main_frame, text='Main Window')
        label.pack(pady=20)

    def open_main_menu(self):
        self.close_window()
        self.current_window = tk.Toplevel(self)
        self.open_previous_window = self.open_main_menu
        self.update_window(title='Main Menu', bg_image=self.main_menu_bg_image)

        play_button = tk.Button(self.current_window, image=self.play_button_image, command=self.open_level)
        help_button = tk.Button(self.current_window, image=self.help_button_image0, command=self.open_help)
        play_button.place(relx=0.5, rely=0.45, anchor='center')
        help_button.place(relx=0.5, rely=0.7, anchor='center')

    def open_level(self):
        self.close_window()
        self.current_window = tk.Toplevel(self)
        self.open_previous_window = self.open_level
        self.update_window(title='Level', bg_image=self.level_bg_image)

        help_button = tk.Button(self.current_window, image=self.help_button_image1, command=self.open_help)
        main_menu_button = tk.Button(self.current_window, image=self.main_menu_button_image, command=self.open_main_menu)
        self.score_label = tk.Label(self.current_window, text=f'SCORE: {self.score}', fg='white', bg='purple', font=FONT_LABEL)
        help_button.place(relx=0.6, rely=0.9, anchor='center')
        main_menu_button.place(relx=0.85, rely=0.9, anchor='center')
        self.score_label.place(relx=0.2, rely=0.9, anchor='center')

        self.canvas = tk.Canvas(self.current_window, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
        self.canvas.place(relx=0.5, rely=0.7, anchor='center')
        self.bar = self.canvas.create_image(CANVAS_WIDTH//2, CANVAS_HEIGHT//2, anchor='center', image=self.bar_image)
        self.current_window.bind('<Left>', self.handle_move_bar_arrows)
        self.current_window.bind('<Right>', self.handle_move_bar_arrows)
        self.current_window.bind('<space>', self.handle_toggle_mouse_control)
        self.current_window.bind('<Escape>', self.handle_open_game_over)

    def open_help(self):
        self.close_window()
        self.current_window = tk.Toplevel(self)
        self.update_window(title='Documentation', bg_image=self.help_bg_image)

        back_button = tk.Button(self.current_window, image=self.back_button_image, command=self.open_previous_window)
        back_button.place(relx=0.2, rely=0.8, anchor='center')

    def open_game_over(self):
        self.close_window()
        self.current_window = tk.Toplevel(self)
        self.open_previous_window = self.open_game_over
        self.update_window(title='Game Over', bg_image=self.game_over_bg_image)

        retry_button = tk.Button(self.current_window, image=self.retry_button_image, command=self.open_level)
        help_button = tk.Button(self.current_window, image=self.help_button_image0, command=self.open_help)
        retry_button.place(relx=0.3, rely=0.6, anchor='center')
        help_button.place(relx=0.65, rely=0.6, anchor='center')
        self.score_label = tk.Label(self.current_window, text=self.score, fg='white', bg='gray', font=FONT_LABEL)
        self.score_label.place(relx=0.45, rely=0.4, anchor='center')

    def close_window(self):
        if self.current_window:
            self.current_window.destroy()
            self.current_window = None

    def update_window(self, title, bg_image):
        if self.current_window:
            self.current_window.title(title)
            self.current_window.geometry(WINDOW_GEOMETRY)
            bg = tk.Label(self.current_window, image=bg_image)
            bg.place(relwidth=1, relheight=1)

    def handle_move_bar_arrows(self, event):
        x = 0
        y = 0
        if event.keysym == 'Left':
            x = -BAR_ARROW_MOVEMENT_INCREMENT
        elif event.keysym == 'Right':
            x = BAR_ARROW_MOVEMENT_INCREMENT

        self.canvas.move(self.bar, x, y)

        # Mock score logic
        if random.choice([True, False]):
            self.score += BAR_ARROW_MOVEMENT_INCREMENT
            self.score_label.config(text=f'SCORE: {self.score}')

    def handle_move_bar_mouse(self, event):
        x = min(event.x, CANVAS_WIDTH)
        x = max(0, x)

        self.canvas.coords(self.bar, x, CANVAS_HEIGHT//2)

    def handle_toggle_mouse_control(self, _):
        if not self.mouse_control_enabled:
            self.current_window.bind('<Motion>', self.handle_move_bar_mouse)
        else:
            self.current_window.unbind('<Motion>')
        self.mouse_control_enabled = not self.mouse_control_enabled

    def handle_open_game_over(self, _):
        self.open_game_over()


if __name__ == '__main__':
    app = MultiWindowApp()
    app.mainloop()
