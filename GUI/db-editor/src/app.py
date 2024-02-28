import customtkinter as ctk
import tkinter.ttk as ttk

from typing import Any, Dict, Tuple
class App(ctk.CTk):
    def __init__(self, configuration: Dict[str, Any]):
        super().__init__()
        self.config: Dict[str, Any] = configuration
        self.center_window()
    def get_scrn_size(self) -> Tuple[int, int]:
        width: int = self.winfo_screenwidth()
        height: int = self.winfo_screenheight()
        return (width, height)
    def center_window(self) -> None:
        scrn_w: int
        scrn_h: int
        scrn_w, scrn_h= self.get_scrn_size()
        # self.update()
        w_width: int = self.config["width"]
        w_height: int = self.config["height"]
        x: int = ((scrn_w // 2) - (w_width // 2))
        y: int = ((scrn_h // 2) - (w_height // 2))
        self.geometry(f"{w_width}x{w_height}+{x}+{y}")
