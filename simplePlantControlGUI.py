""" Skeleton code for the GUI downloaded from:
    http://eli.thegreenplace.net/2008/08/01/matplotlib-with-wxpython-guis/
    credit to Eli Bendersky
"""
import os
import sys
import wx
import plant
import rl
import time

import matplotlib

matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas
import numpy as np
import pylab


class FloatSlider(wx.Slider):
    def GetValue(self):
        return (float(wx.Slider.GetValue(self))) / 100


class SliderBox(wx.Panel):
    def __init__(self, parent, ID, label, min_max_init_val):
        wx.Panel.__init__(self, parent, ID)

        self.value = min_max_init_val[2]

        box = wx.StaticBox(self, -1, label)
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)

        self.slider = FloatSlider(self, id=-1, minValue=min_max_init_val[0], maxValue=min_max_init_val[1],
                                  value=min_max_init_val[2],
                                  style=wx.SL_VERTICAL | wx.SL_INVERSE)

        manual_box = wx.BoxSizer(wx.HORIZONTAL)
        manual_box.Add(self.slider, flag=wx.ALIGN_CENTER_VERTICAL)

        sizer.Add(manual_box, 0, wx.ALL, 10)

        self.SetSizer(sizer)
        sizer.Fit(self)

    def get_slider_value(self):
        return self.slider.GetValue()


class BoundControlBox(wx.Panel):
    """ A static box with a couple of radio buttons and a text
        box. Allows to switch between an automatic mode and a 
        manual mode with an associated value.
    """

    def __init__(self, parent, ID, label, initval):
        wx.Panel.__init__(self, parent, ID)

        self.value = initval

        box = wx.StaticBox(self, -1, label)
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)

        self.radio_auto = wx.RadioButton(self, -1,
                                         label="Auto", style=wx.RB_GROUP)
        self.radio_manual = wx.RadioButton(self, -1,
                                           label="Manual")
        self.manual_text = wx.TextCtrl(self, -1,
                                       size=(35, -1),
                                       value=str(initval),
                                       style=wx.TE_PROCESS_ENTER)

        self.Bind(wx.EVT_UPDATE_UI, self.on_update_manual_text, self.manual_text)
        self.Bind(wx.EVT_TEXT_ENTER, self.on_text_enter, self.manual_text)

        manual_box = wx.BoxSizer(wx.HORIZONTAL)
        manual_box.Add(self.radio_manual, flag=wx.ALIGN_CENTER_VERTICAL)
        manual_box.Add(self.manual_text, flag=wx.ALIGN_CENTER_VERTICAL)

        sizer.Add(self.radio_auto, 0, wx.ALL, 10)
        sizer.Add(manual_box, 0, wx.ALL, 10)

        self.SetSizer(sizer)
        sizer.Fit(self)

    def on_update_manual_text(self, event):
        self.manual_text.Enable(self.radio_manual.GetValue())

    def on_text_enter(self, event):
        self.value = self.manual_text.GetValue()

    def is_auto(self):
        return self.radio_auto.GetValue()

    def manual_value(self):
        return self.value


class GraphFrame(wx.Frame):
    """ The main frame of the application
    """
    title = 'Demo: dynamic matplotlib graph'

    def __init__(self):
        wx.Frame.__init__(self, None, -1, self.title)
        self.u = []
        for k0 in range(33):
            self.u.append(0.5)

        for k1 in range(33):
            self.u.append(0)

        for k2 in range(34):
            self.u.append(-0.5)

        self.set_point_data = [0.0]
        self.plant_output_data = [0.0]
        self.paused = False

        self.agent = rl.Agent(actions=np.linspace(-1, 1, 5), manual_exploration=False,
                              e_bins=np.linspace(-1.5, 1.5, 20), de_bins=np.linspace(-3, 3, 5),
                              plant=plant.SimpleControlPlant.get_sample_plant(0.03), time_step=0.03)

        self.create_menu()
        self.create_status_bar()
        self._create_main_panel()

        self.redraw_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_redraw_timer, self.redraw_timer)
        self.redraw_timer.Start(1)

        self.is_open = True
        self.timo = time.time()
        self.iter = 0

    def create_menu(self):
        self.menubar = wx.MenuBar()

        menu_file = wx.Menu()
        m_expt = menu_file.Append(-1, "&Save plot\tCtrl-S", "Save plot to file")
        self.Bind(wx.EVT_MENU, self.on_save_plot, m_expt)
        menu_file.AppendSeparator()
        m_exit = menu_file.Append(-1, "E&xit\tCtrl-X", "Exit")
        self.Bind(wx.EVT_MENU, self.on_exit, m_exit)

        self.Bind(wx.EVT_CLOSE, self.on_exit)

        self.menubar.Append(menu_file, "&File")
        self.SetMenuBar(self.menubar)

    def _create_main_panel(self):
        self.panel = wx.Panel(self)

        self.init_plot()
        self.canvas = FigCanvas(self.panel, -1, self.fig)

        self.xmin_control = BoundControlBox(self.panel, -1, "X min", 0)
        self.xmax_control = BoundControlBox(self.panel, -1, "X max", 10)
        self.ymin_control = BoundControlBox(self.panel, -1, "Y min", -1)
        self.ymax_control = BoundControlBox(self.panel, -1, "Y max", 1)

        self.slider_control = SliderBox(self.panel, -1, "Slider", [-50, 50, 0])
        self.slider_chance_control = SliderBox(self.panel, -1, "Exploration rate", [0, 100, 100])

        self.pause_button = wx.Button(self.panel, -1, "Pause")
        self.Bind(wx.EVT_BUTTON, self.on_pause_button, self.pause_button)
        self.Bind(wx.EVT_UPDATE_UI, self.on_update_pause_button, self.pause_button)

        self.cb_grid = wx.CheckBox(self.panel, -1,
                                   "Show Grid",
                                   style=wx.ALIGN_RIGHT)
        self.Bind(wx.EVT_CHECKBOX, self.on_cb_grid, self.cb_grid)
        self.cb_grid.SetValue(True)

        self.cb_xlab = wx.CheckBox(self.panel, -1,
                                   "Show X labels",
                                   style=wx.ALIGN_RIGHT)
        self.Bind(wx.EVT_CHECKBOX, self.on_cb_xlab, self.cb_xlab)
        self.cb_xlab.SetValue(True)

        self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox1.Add(self.pause_button, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.hbox1.AddSpacer(20)
        self.hbox1.Add(self.cb_grid, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.hbox1.AddSpacer(10)
        self.hbox1.Add(self.cb_xlab, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)

        self.hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox2.Add(self.xmin_control, border=5, flag=wx.ALL)
        self.hbox2.Add(self.xmax_control, border=5, flag=wx.ALL)
        self.hbox2.AddSpacer(24)
        self.hbox2.Add(self.ymin_control, border=5, flag=wx.ALL)
        self.hbox2.Add(self.ymax_control, border=5, flag=wx.ALL)
        self.hbox2.AddSpacer(24)
        self.hbox2.Add(self.slider_control, border=5, flag=wx.ALL)
        self.hbox2.Add(self.slider_chance_control, border=5, flag=wx.ALL)

        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.canvas, 1, flag=wx.LEFT | wx.TOP | wx.GROW)
        self.vbox.Add(self.hbox1, 0, flag=wx.ALIGN_LEFT | wx.TOP)
        self.vbox.Add(self.hbox2, 0, flag=wx.ALIGN_LEFT | wx.TOP)

        self.panel.SetSizer(self.vbox)
        self.vbox.Fit(self)

    def create_status_bar(self):
        self.statusbar = self.CreateStatusBar()

    def init_plot(self):
        self.dpi = 100
        self.fig = Figure((3.0, 3.0), dpi=self.dpi)

        self.axes = self.fig.add_subplot(111)
        # self.axes.set_axis_bgcolor('black')
        self.axes.set_title('Real time control', size=12)
        self.axes.set_xlabel('t(s)')
        self.axes.set_ylabel('Odziv')

        pylab.setp(self.axes.get_xticklabels(), fontsize=8)
        pylab.setp(self.axes.get_yticklabels(), fontsize=8)

        # plot the data as a line series, and save the reference 
        # to the plotted line series
        #
        self.plot_data_0 = self.axes.plot(0, 1, 'b-', linewidth=1, )[0]
        self.plot_data_1 = self.axes.plot(0, 1, 'g-', linewidth=1, )[0]

    def draw_plot(self):
        """ Redraws the plot
        """
        if self.xmax_control.is_auto():
            xmax = len(self.set_point_data) * self.agent.time_step if len(
                self.set_point_data) > 20 / self.agent.time_step else 20
        else:
            xmax = float(self.xmax_control.manual_value())

        if self.xmin_control.is_auto():
            xmin = xmax - 20
        else:
            xmin = float(self.xmin_control.manual_value())

        if self.ymin_control.is_auto():
            ymin = float(min(self.set_point_data)) - 1
        else:
            ymin = float(self.ymin_control.manual_value())

        if self.ymax_control.is_auto():
            ymax = round(max(self.set_point_data), 0) + 1
        else:
            ymax = float(self.ymax_control.manual_value())

        self.axes.set_xbound(lower=xmin, upper=xmax)
        self.axes.set_ybound(lower=ymin, upper=ymax)

        if self.cb_grid.IsChecked():
            self.axes.grid(True, color='gray')
        else:
            self.axes.grid(False)

        pylab.setp(self.axes.get_xticklabels(),
                   visible=self.cb_xlab.IsChecked())

        self.plot_data_0.set_xdata(np.arange(len(self.set_point_data)) * self.agent.time_step)
        self.plot_data_0.set_ydata(self.set_point_data)

        self.plot_data_1.set_xdata(np.arange(len(self.set_point_data)) * self.agent.time_step)
        self.plot_data_1.set_ydata(self.plant_output_data)
        self.canvas.draw()

    def on_pause_button(self, event):
        self.paused = not self.paused

    def on_update_pause_button(self, event):
        label = "Resume" if self.paused else "Pause"
        self.pause_button.SetLabel(label)

    def on_cb_grid(self, event):
        self.draw_plot()

    def on_cb_xlab(self, event):
        self.draw_plot()

    def on_save_plot(self, event):
        file_choices = "PNG (*.png)|*.png"

        dlg = wx.FileDialog(
            self,
            message="Save plot as...",
            defaultDir=os.getcwd(),
            defaultFile="plot.png",
            wildcard=file_choices,
            style=wx.SAVE)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.canvas.print_figure(path, dpi=self.dpi)
            self.flash_status_message("Saved to %s" % path)

    def on_redraw_timer(self, event):
        # if paused do not add data, but still redraw the plot
        # (to respond to scale modifications, grid change, etc.)
        #
        if not self.is_open:
            sys.exit(0)
        if not self.paused:
            # self.set_point_data.append(self.slider_control.get_slider_value())
            # self.agent.exploration_rate = self.slider_chance_control.get_slider_value()
            self.set_point_data.append(self.u[self.iter % 100])
            self.agent.update_q_table(self.set_point_data[-1])
            self.plant_output_data.append(self.agent.plant.get_current_output())

            time_to_sleep = 0.03 - (time.time() - self.timo)

            if time_to_sleep > 0:
                time.sleep(time_to_sleep)

            self.timo = time.time()
            self.draw_plot()
            self.iter += 1

    def on_exit(self, event):
        self.Destroy()
        self.is_open = False

    def flash_status_message(self, msg, flash_len_ms=1500):
        self.statusbar.SetStatusText(msg)
        self.timeroff = wx.Timer(self)
        self.Bind(
            wx.EVT_TIMER,
            self.on_flash_status_off,
            self.timeroff)
        self.timeroff.Start(flash_len_ms, oneShot=True)

    def on_flash_status_off(self, event):
        self.statusbar.SetStatusText('')


if __name__ == '__main__':
    app = wx.App()
    app.frame = GraphFrame()
    app.frame.Show()
    app.MainLoop()

