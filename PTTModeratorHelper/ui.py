# -*- coding: utf-8 -*-

import tkinter
from tkinter import ttk

import PTTCrawler
import mailSender
import rulechecker

class PttModeratorHelperGui(ttk.Frame):

    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)

        self.result = ""
        self._setup_widgets()

    def _setup_widgets(self):
        # setup crawl button
        self.process = ttk.Button(self, text="Crawl", command=self._crawl)
        self.process.pack()

        # setup entry box
        self.resultBox = tkinter.Text(self)
        self.resultBox.config(width=50)
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
        PTTCrawler.executeCrawl()

    def _check(self):
        self.result = rulechecker.checkRules()
        self.resultBox.insert("end", self.result)

    def _send(self):
        mailSender.sendMail(content=self.result)


def main():
    root = tkinter.Tk()
    app = PttModeratorHelperGui(root)
    app.pack()
    app.mainloop()


if __name__ == "__main__":
    main()
