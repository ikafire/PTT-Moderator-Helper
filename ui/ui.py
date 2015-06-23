# -*- coding: utf-8 -*-

import tkinter
from tkinter import ttk

class PttModeratorHelperGui(ttk.Frame):

    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)

        # setup binding variable for entry box
        self.result = tkinter.StringVar(value="result will be shown here.")
        self._setup_widgets()

    def _setup_widgets(self):
        # setup crawl button
        self.process = ttk.Button(self, text="Process", command=self._execute_crawl_and_check)
        self.process.pack()

        # setup entry box
        self.resultBox = ttk.Label(self, textvar=self.result)
        self.resultBox.config(
                width=50, wraplength=400, justify="left")
        self.resultBox.pack(side="bottom", fill="both", expand=1)

        # setup send button
        self.send = ttk.Button(self, text="Send Email", command=self._send)
        self.send.pack()

    def _execute_crawl_and_check(self):


    def _send(self):
        print("send")

def main():
    root = tkinter.Tk()
    app = PttModeratorHelperGui(root)
    app.pack()
    app.mainloop()


if __name__ == "__main__":
    main()
