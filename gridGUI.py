from Tkinter import Tk, Canvas, Frame, Button
from Tkinter import BOTH, TOP, LEFT, RIGHT
import dp
import monteCarlo
import tdLambda


class PolygonContainer():
    def __init__(self):
        self.polygons = []

    def add_polygon(self, polygon, state, action):
        self.polygons.append([polygon, state, action])

    def get_polygon(self, state, action):
        return [p[0] for p in self.polygons if p[1] == state and p[2] == action][0]


class GridGUI(Frame):
    def __init__(self, parent, dimensions=(3, 5), square_size=50, algorithm=None):
        Frame.__init__(self, parent)
        self.parent = parent
        (self.max_row, self.max_col) = dimensions
        self.board_height = square_size * self.max_row
        self.board_width = square_size * self.max_col
        self.sq_size = square_size
        self.polygons = PolygonContainer()
        self.algorithm = algorithm
        self.algorithm_is_paused = False
        self._init_ui()

    def _init_ui(self):
        self.parent.title("Layout Test")
        self.config(bg='#F0F0F0')
        self.pack(fill=BOTH, expand=1)
        # create canvas
        self.canvas = Canvas(self, width=self.board_width, height=self.board_height, bg='#CCFF99', borderwidth=0,
                             highlightthickness=0)
        for row in range(self.max_row):
            for col in range(self.max_col):
                if self.algorithm.is_terminal_state((row, col)):
                    is_terminal, value = self.algorithm.is_terminal_state((row, col))
                    if value == -100:
                        self.canvas.create_rectangle(col * self.sq_size, row * self.sq_size, (col + 1) * self.sq_size,
                                                     (row + 1) * self.sq_size, outline='gray',
                                                     fill='#FF3300', width=1)
                    else:
                        self.canvas.create_rectangle(col * self.sq_size, row * self.sq_size, (col + 1) * self.sq_size,
                                                     (row + 1) * self.sq_size, outline='gray',
                                                     fill='#0066FF', width=1)
                    continue

                nx0 = col * self.sq_size
                ny0 = row * self.sq_size
                nx1 = nx0 + self.sq_size
                ny1 = ny0
                nx2 = nx0 + self.sq_size / 2
                ny2 = ny0 + self.sq_size / 2
                n_points = [nx0, ny0, nx1, ny1, nx2, ny2]
                n_polygon = self.canvas.create_polygon(n_points, outline='gray', fill='#CCFF99', width=1)
                self.polygons.add_polygon(n_polygon, (row, col), "N")

                ex0 = (col + 1) * self.sq_size
                ey0 = row * self.sq_size
                ex1 = ex0
                ey1 = ey0 + self.sq_size
                ex2 = ex0 - self.sq_size / 2
                ey2 = ey0 + self.sq_size / 2
                e_points = [ex0, ey0, ex1, ey1, ex2, ey2]
                e_polygon = self.canvas.create_polygon(e_points, outline='gray', fill='#CCFF99', width=1)
                self.polygons.add_polygon(e_polygon, (row, col), "E")

                sx0 = col * self.sq_size
                sy0 = (row + 1) * self.sq_size
                sx1 = sx0 + self.sq_size
                sy1 = sy0
                sx2 = sx0 + self.sq_size / 2
                sy2 = sy0 - self.sq_size / 2
                s_points = [sx0, sy0, sx1, sy1, sx2, sy2]
                s_polygon = self.canvas.create_polygon(s_points, outline='gray', fill='#CCFF99', width=1)
                self.polygons.add_polygon(s_polygon, (row, col), "S")

                wx0 = col * self.sq_size
                wy0 = row * self.sq_size
                wx1 = wx0
                wy1 = wy0 + self.sq_size
                wx2 = wx0 + self.sq_size / 2
                wy2 = wy0 + self.sq_size / 2
                w_points = [wx0, wy0, wx1, wy1, wx2, wy2]
                w_polygon = self.canvas.create_polygon(w_points, outline='gray', fill='#CCFF99', width=1)
                self.polygons.add_polygon(w_polygon, (row, col), "W")

        self.canvas.pack(side=TOP, padx=10, pady=10)

        start_button = Button(self, text="Start", command=self.start_algorithm)
        start_button.configure(width=10)
        start_button.pack(side=LEFT)

        pause_button = Button(self, text="Pause", command=self.pause_algorithm)
        pause_button.configure(width=10)
        pause_button.pack(side=RIGHT)

    def start_algorithm(self):
        self.algorithm_is_paused = False
        self.run_algorithm()

    def run_algorithm(self):
        if not self.algorithm_is_paused:
            canvas = self.canvas
            self.algorithm.learn()
            for row in range(self.max_row):
                for col in range(self.max_col):
                    if self.algorithm.is_terminal_state((row, col)):
                        continue
                    argmax_action = self.algorithm.get_policy((row, col))
                    for action in self.algorithm.gw.actions:
                        canvas.itemconfig(self.polygons.get_polygon((row, col), action), fill="#CCFF99")
                    canvas.itemconfig(self.polygons.get_polygon((row, col), argmax_action), fill="#009900")
            if self.algorithm.is_online():
                self.after(10, self.run_algorithm)

    def pause_algorithm(self):
        self.algorithm_is_paused = True


def main():
    root = Tk()
    grid_dimensions = (4, 5)
    dp_algorithm = dp.DP(dimensions=grid_dimensions)
    mc_algorithm = monteCarlo.MonteCarlo(dimensions=grid_dimensions)
    td_lambda_algorithm = tdLambda.TDLambda(dimensions=grid_dimensions)
    app = GridGUI(root, dimensions=grid_dimensions, algorithm=mc_algorithm)
    app.mainloop()


if __name__ == '__main__':
    main()