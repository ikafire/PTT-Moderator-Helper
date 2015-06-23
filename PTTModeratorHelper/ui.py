# -*- coding: utf-8 -*-

import tkinter
from tkinter import ttk

import PTTCrawlerV2
import rulechecker

class PttModeratorHelperGui(ttk.Frame):

    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)

        # setup binding variable for entry box
        self.result = tkinter.StringVar(value="result will be shown here.")
        self._setup_widgets()

    def _setup_widgets(self):
        # setup crawl button
        self.process = ttk.Button(self, text="Process", command=self._crawl)
        self.process.pack()

        # setup entry box
        self.resultBox = ttk.Label(self, textvar=self.result)
        self.resultBox.config(
                width=50, wraplength=400, justify="left")
        self.resultBox.pack(side="bottom", fill="both", expand=1)

        # setup check button
        self.check = ttk.Button(self, text="Check", command=self._check)
        self.check.pack()

        # setup send button
        self.send = ttk.Button(self, text="Send Email", command=self._send)
        self.send.pack()

    def _execute_crawl_and_check(self):
        self._crawl()
        self._check()

    def _crawl(self):
        PTTCrawlerV2.executeCrawl()

    def _check(self):
        result = rulechecker.checkRules()
        self.result.set(result)

    def _send(self):
        print("send")

def main():
    root = tkinter.Tk()
    app = PttModeratorHelperGui(root)
    app.pack()
    app.mainloop()


if __name__ == "__main__":
    main()
