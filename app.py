import wx
import time
from wx.lib.buttons import GenButton


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title='Stopwatch')
        self.timer = wx.Timer(self)
        self.startTime = 0.0 # 按下启动按钮的时间
        self.timePast = 0.0 # 上次计时了多久
        self.recordId = 0 # 计次id
        self._init_ui()
        self._init_event()

    def _init_event(self):
        self.btn_run.Bind(wx.EVT_BUTTON, self._on_btn_run_clicked)
        self.btn_reset.Bind(wx.EVT_BUTTON, self._on_btn_reset_clicked)
        self.Bind(wx.EVT_TIMER, self._update_time, self.timer)

    def _on_btn_run_clicked(self, _):
        if self.timer.IsRunning():
            self.timePast = self.timePast + (time.time() - self.startTime)
            self.timer.Stop()
            self.btn_run.SetLabel('启动')
            self.btn_reset.SetLabel('复位')
        else:
            self.startTime = time.time()
            self.timer.Start(50)
            self.btn_run.SetLabel('停止')
            self.btn_reset.SetLabel('计次')

    def _on_btn_reset_clicked(self, _):
        if self.timer.IsRunning():
            print('记录')
            second = time.time() - self.startTime + self.timePast
            minute = int(second / 60)
            second = second - minute * 60
            self.recordId += 1
            self.listBox.Append('[计次'+ f'{self.recordId:02}' +'] ' + f'{minute:02}:{second:05.2f}')
        else:
            self.timePast = 0
            self.recordId = 0 # 计次id
            self.st_time.SetLabel('00:00.00')
            self.listBox.Clear()
    
    def _update_time(self, _):
        second = time.time() - self.startTime + self.timePast
        minute = int(second / 60)
        second = second - minute * 60
        self.st_time.SetLabel(f'{minute:02}:{second:05.2f}')

    def _init_ui(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.AddStretchSpacer()

        self.st_time = wx.StaticText(self, label='00:00.00')
        self.st_time.SetFont(wx.Font(wx.FontInfo(120)))

        self.btn_run = GenButton(self, label='启动', size=(100,30), style=wx.BORDER_NONE)
        self.btn_reset = GenButton(self, label='复位', size=(100,30), style=wx.BORDER_NONE)


        self.listBox = wx.ListBox(self, -1, size=(300, 120), choices=[], style=wx.LB_SINGLE)

        main_sizer.Add(self.st_time, flag=wx.ALIGN_CENTER_HORIZONTAL)
        main_sizer.AddSpacer(80)

        main_sizer.Add(self.btn_run, flag=wx.ALIGN_CENTER_HORIZONTAL)
        main_sizer.AddSpacer(30)
        main_sizer.Add(self.btn_reset, flag=wx.ALIGN_CENTER_HORIZONTAL)
        main_sizer.AddSpacer(30)
        main_sizer.Add(self.listBox, flag=wx.ALIGN_CENTER_HORIZONTAL)
        

        main_sizer.AddStretchSpacer()
        self.SetSizer(main_sizer)
        self.SetSize(800,600)
        # self.Maximize()

        self.st_time.SetForegroundColour('white')
        self.btn_run.SetBackgroundColour('#00CC99')
        self.btn_run.SetForegroundColour('white')
        self.btn_reset.SetBackgroundColour('#FF6666')
        self.btn_reset.SetForegroundColour('white')
        self.SetBackgroundColour('#444444')


app = wx.App()
MainFrame().Show()
app.MainLoop()  