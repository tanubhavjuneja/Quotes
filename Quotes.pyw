import sys
import time
import customtkinter as ctk
import os
import tkfilebrowser
import requests
from PyQt5.QtWidgets import QApplication, QLabel, QFrame
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt
time.sleep(5)
def read_file_location():
    global mfl
    try:
        file=open('file_location.txt', 'r')
        mfl = file.read().strip()
        file.close()
        if not os.path.isfile(os.path.join(mfl, 'icon.ico')):
            get_file_location()
    except FileNotFoundError:
        get_file_location()
def get_file_location():
    global main
    main=ctk.CTk()
    main.geometry("200x50+860+420")
    main.attributes('-topmost', True)
    main.attributes("-alpha",100.0)
    main.lift()
    file_button = ctk.CTkButton(main, text="Select File Location",command=select_file_location,width=1)
    file_button.pack(pady=10)
    main.mainloop()
def select_file_location():
    global main
    mfl = str(tkfilebrowser.askopendirname())+"/"
    mfl = mfl.replace('\\', '/')
    file=open('file_location.txt', 'w')
    file.write(mfl)
    file.close()
    main.destroy()
    read_file_location()
class QuoteWidget:
    def __init__(self):
        global mfl
        self.app = QApplication(sys.argv)
        self.window = QLabel()
        self.app.setWindowIcon(QIcon(mfl+"icon.ico"))
        self.window.setWindowFlags(Qt.FramelessWindowHint)
        self.window.setAttribute(Qt.WA_TranslucentBackground)
        self.window.setPixmap(QPixmap(mfl+"paper.png").scaled(500, 500))
        self.window.resize(self.window.pixmap().size())
        self.window.move(1450, 1)  
        self.frame = QFrame(self.window)
        self.frame.setGeometry(96, 64, 300, 380) 
        self.frame.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.frame.setFixedWidth(300)
        self.quote_label = QLabel(self.frame)
        self.author_label = QLabel(self.frame)
        close_button = QLabel(self.window)
        close_button.setPixmap(QPixmap(mfl+"close.png").scaled(40, 40)) 
        close_button.setAlignment(Qt.AlignCenter)
        close_button.setStyleSheet("background-color: transparent;")
        close_button.move(self.window.width() - close_button.width() - 40, 60)
        close_button.mousePressEvent = lambda event: sys.exit()
        self.window.show()
        self.update_quote()
        self.frame.mousePressEvent = self.update_quote
    def update_quote(self, event=None):
        response = requests.get("https://api.quotable.io/random")
        quote_data = response.json()
        quote = quote_data["content"]
        author = quote_data["author"]
        self.quote_label.setText(quote)
        self.quote_label.setFont(QFont("Arial", 16))
        self.quote_label.setWordWrap(True)
        self.quote_label.setAlignment(Qt.AlignCenter)
        self.quote_label.setFixedWidth(self.frame.width() - 20)
        self.quote_label.setStyleSheet("background-color: transparent; color: black;")
        self.author_label.setText("- " + author)
        self.author_label.setFont(QFont("Arial", 12))
        self.author_label.setAlignment(Qt.AlignRight)
        self.author_label.setStyleSheet("background-color: transparent; color: black;")
        self.quote_label.setGeometry(10, 20, self.frame.width() - 20, 300)
        self.author_label.setGeometry(10, 330, self.frame.width() - 20, 60)
    def run(self):
        sys.exit(self.app.exec_())
if __name__ == "__main__":
    read_file_location()
    widget = QuoteWidget()
    widget.window.setWindowFlags(Qt.Window | Qt.Tool | Qt.FramelessWindowHint)
    widget.window.show()
    widget.run()
