import configparser
import hashlib
import pathlib
import time
import tkinter as tk

import keyboard

cf = pathlib.Path("./snote.ini")
cf.touch(exist_ok=True)
with cf.open("r+") as f:
    config = configparser.ConfigParser()
    config.read(cf)
    print(config.sections())
    if "Default" not in config:
        config["Default"] = {
            "font.name": "Jetbrains Mono",
            "font.size": 12,
            "notes.hotkey": "windows+`",
            "notes.encoding": "utf-8"
        }
        config.write(f)

hot_key = config["Default"]["notes.hotkey"]
font = config["Default"]["font.name"], config["Default"]["font.size"]
coding = config["Default"]["notes.encoding"]

pathlib.Path("./notes").mkdir(parents=True, exist_ok=True)


class Note(tk.Tk):
    menubar: tk.Menu
    text: tk.Text
    s: tk.Scrollbar
    is_showing: bool

    def __init__(self):
        super().__init__()
        self.title("SNote v1.0")
        self.attributes("-topmost", True)

        self.menubar = tk.Menu(self)
        self.menubar.add_command(label="Fast save and New", command=self.fast_save)
        self.config(menu=self.menubar)

        self.s = tk.Scrollbar(self)
        self.text = tk.Text(self, font=font, yscrollcommand=self.s.set)
        self.s.config(command=self.text.yview)

        self.s.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.pack()
        keyboard.add_hotkey(hot_key, self.switch)
        self.is_showing = True

    def switch(self):
        print(1)
        if self.is_showing:
            self.hide()
        else:
            self.show()
        self.is_showing = not self.is_showing
        while keyboard.is_pressed(hot_key):
            pass

    def show(self):
        self.wm_deiconify()

    def hide(self):
        self.withdraw()

    def fast_save(self):
        content = self.text.get("1.0", tk.END).encode(encoding=coding)

        path = pathlib.Path("./notes/snote_{}.txt".format(time.strftime("%Y_%m_%d_%H_%M_%S")))

        path.touch(exist_ok=True)
        with path.open("wb") as f:
            f.write(content)
            f.close()
        with path.open("rb") as f:
            if hashlib.md5(f.read()).hexdigest() == hashlib.md5(content).hexdigest():
                print("1")
                self.text.delete("1.0", tk.END)

    def on_close(self):
        self.fast_save()
        exit(0)


Note().mainloop()
