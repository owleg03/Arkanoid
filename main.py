import tkinter as tk
from PIL import ImageTk as itk

WIDTH = 720
HEIGHT = 512 + 50
WINDOW_GEOMETRY = f'{WIDTH}x{HEIGHT}+{WIDTH // 2}+{HEIGHT // 2}'
RUNNER_WINDOW_SIZE = '200x50'


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

        self.main_frame = None
        self.current_window = None
        self.open_previous_window = None
        # self.bg = None

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
        self.update_window(title='Main Menu')

        # self.bg_image = itk.PhotoImage(file='./images/main_menu_bg.png')
        # self.bg = tk.Label(self.current_window, image=self.bg_image)
        # self.bg.place()

        play_button = tk.Button(self.current_window, image=self.play_button_image, command=self.open_level)
        help_button = tk.Button(self.current_window, image=self.help_button_image0, command=self.open_help)
        play_button.place(relx=0.5, rely=0.45, anchor="center")
        help_button.place(relx=0.5, rely=0.7, anchor="center")

    def open_level(self):
        self.close_window()
        self.current_window = tk.Toplevel(self)
        self.open_previous_window = self.open_level
        self.update_window(title='Level')

        help_button = tk.Button(self.current_window, image=self.help_button_image1, command=self.open_help)
        main_menu_button = tk.Button(self.current_window, image=self.main_menu_button_image, command=self.open_main_menu)
        help_button.place(relx=0.6, rely=0.9, anchor="center")
        main_menu_button.place(relx=0.85, rely=0.9, anchor="center")

    def open_help(self):
        self.close_window()
        self.current_window = tk.Toplevel(self)
        self.update_window(title='Documentation')

        back_button = tk.Button(self.current_window, image=self.back_button_image, command=self.open_previous_window)
        back_button.place(relx=0.2, rely=0.8, anchor="center")

    def open_game_over(self):
        self.close_window()
        self.current_window = tk.Toplevel(self)
        self.open_previous_window = self.open_game_over
        self.update_window(title='Game Over')

        retry_button = tk.Button(self.current_window, image=self.retry_button_image, command=self.open_level)
        help_button = tk.Button(self.current_window, image=self.help_button_image0, command=self.open_help)
        retry_button.place(relx=0.25, rely=0.6, anchor="center")
        help_button.place(relx=0.25, rely=0.8, anchor="center")

    def close_window(self):
        if self.current_window:
            self.current_window.destroy()
            self.current_window = None

    def update_window(self, title):
        if self.current_window:
            self.current_window.title(title)
            self.current_window.geometry(WINDOW_GEOMETRY)


if __name__ == '__main__':
    app = MultiWindowApp()
    app.mainloop()
