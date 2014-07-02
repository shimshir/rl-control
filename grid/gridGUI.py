from Tkinter import Tk, Canvas, Frame, Button
from Tkinter import BOTH, TOP


class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.board_size = 250
        self.sq_size = self.board_size // 5
        self.init_ui()

    def init_ui(self):
        self.parent.title("Layout Test")
        self.config(bg='#F0F0F0')
        self.pack(fill=BOTH, expand=1)
        # create canvas
        canvas1 = Canvas(self, width=self.board_size, height=self.board_size, bg='white', borderwidth=0,
                         highlightthickness=0)
        for row in range(5):
            for col in range(5):
                nx0 = row * self.sq_size
                ny0 = col * self.sq_size
                nx1 = nx0 + self.sq_size
                ny1 = ny0
                nx2 = nx0 + self.sq_size / 2
                ny2 = ny0 + self.sq_size / 2
                n_points = [nx0, ny0, nx1, ny1, nx2, ny2]
                canvas1.create_polygon(n_points, outline='gray', fill='blue', width=1)

                ex0 = (row + 1) * self.sq_size
                ey0 = col * self.sq_size
                ex1 = ex0
                ey1 = ey0 + self.sq_size
                ex2 = ex0 - self.sq_size / 2
                ey2 = ey0 + self.sq_size / 2
                e_points = [ex0, ey0, ex1, ey1, ex2, ey2]
                canvas1.create_polygon(e_points, outline='gray', fill='red', width=1)

                sx0 = row * self.sq_size
                sy0 = (col + 1) * self.sq_size
                sx1 = sx0 + self.sq_size
                sy1 = sy0
                sx2 = sx0 + self.sq_size / 2
                sy2 = sy0 - self.sq_size / 2
                s_points = [sx0, sy0, sx1, sy1, sx2, sy2]
                canvas1.create_polygon(s_points, outline='gray', fill='yellow', width=1)

                wx0 = row * self.sq_size
                wy0 = col * self.sq_size
                wx1 = wx0
                wy1 = wy0 + self.sq_size
                wx2 = wx0 + self.sq_size / 2
                wy2 = wy0 + self.sq_size / 2
                w_points = [wx0, wy0, wx1, wy1, wx2, wy2]
                canvas1.create_polygon(w_points, outline='gray', fill='green', width=1)

        canvas1.pack(side=TOP, padx=10, pady=10)
        # add quit button
        button1 = Button(self, text="Quit", command=self.quit)
        button1.configure(width=10)
        # button1_window = canvas1.create_window(10, 10, anchor=NW, window=button1)
        button1.pack(side=TOP)


def task(root):
    print "hello"
    root.after(100, task, root)  # reschedule event in 2 seconds


def main():
    root = Tk()
    app = Example(root)
    app.after(100, task, root)
    app.mainloop()


if __name__ == '__main__':
    main()