import datetime
import re
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk


class Graph():
  """
  A class used to represent the graph  
  """

  def __init__(self):
    self.hours = None
    self.temps = None

  '''
  Method: Sets hourly data used later in plotting
  Paramter: list[]
  Returns: none
  '''

  def set_hours(self, hours_l):
    self.hours = hours_l

  '''
  Method: Sets temperature data used later in plotting
  Paramter: list[]
  Returns: none
  '''

  def set_temps(self, temp_l):
    self.temps = temp_l

  '''
  Method:Takes data set by setter methods and plots
         the data into a graph using matplotlib  
  Params: None
  Returns: Matplotlib.figure that contains the graph
  '''

  def return_plt(self):
    fig = Figure(figsize=(8, 2), dpi=100)
    plot_fig = fig.add_subplot(111)
    temp = [min(self.temps)] * 8
    plot_fig.plot(self.hours, self.temps, color='#dbc85a', marker='_')
    plot_fig.fill_between(self.hours,
                          temp,
                          self.temps,
                          color='yellow',
                          alpha=0.2)  #marker='o'
    return fig


class Clock():
  """
  A class used to represent a clock, implementing 
  datetime python libary to do different conversions on data.
  """

  def __init__(self):
    self.dt = datetime.datetime.now()
    self.pst_hour = None
    self.pst_hourly = None
    self.pst_compl = None
    self.pst_round = None
    self.get_pst_time()  # 00:00
    #                      00:00 pm/am

  '''
  Method: it calculates the current time, in replit using datetime and now() method returns 
  the current time in unix time so I built this method to conver that to 12-hour pst time
  Paramter: None
  Return: None 
  '''

  def get_pst_time(self):
    period = self.dt.strftime("%p")
    str_utc = self.dt.strftime('%I:%M')
    str_hour = self.dt.strftime('%I')[0:2]
    time = int(str_hour) - 7
    self.pst_hour = '0' + str(time) if time > 0 else str(12 + time)
    if len(self.pst_hour) < 2:
      self.pst_hour = '0' + self.pst_hour
    if period == 'PM' and time <= 0:
      period = 'AM'
    elif period == 'AM' and time <= 0:
      period = "PM"
    self.pst_hourly = re.sub('^\d{2}', self.pst_hour, str_utc)  #this is string
    self.pst_compl = self.pst_hourly + ' ' + period
    self.pst_round = self.pst_hourly[:2] + ":00 " + period 

  '''
  Method: Getter function, returns pst_compl which is the current time in pacific time
  Params: None
  Return: self.pst_compl
  '''

  def get_pst_compl(self):
    return self.pst_compl

  '''
  Method: Returns the hourly time in pst time
  Params: None
  Return: self.pst_hourly
  '''

  def get_pst_hourly(self):
    return self.pst_hourly

  '''
  Method: Returns the hour in pst time
  Paramter: None
  Return: self.pst_hour
  '''

  def get_pst_hour(self):
    return self.pst_hour

  '''
  Method: Converts the datetimes to Hour:Minutes am/pm
  Params: list[]
  Return: list[]
  '''

  def convert_times(self, temp):
    return [
      self.dt.now().strptime(temp[x][11:16], "%H:%M").strftime("%I:%M %p")
      for x in range(len(temp))
    ]

  '''
  Method: Returns a subset of the data that is later used in plotting
  Paramter: list_temperatures[], list_times[]
  Return: subset list_temperatures[], list_times[]
  '''

  def return_list(self, temp, time):
    start = time.index(self.pst_round) + 1
    temp_x = []
    time_y = []
    for x in range(8):
      temp_x.append(temp[start + (x * 3)])
      time_y.append(time[start + (x * 3)])
    return temp_x, time_y

  '''
  Method: Returns the datetime in its abbreviated form yyyy-mm-dd -> mon,tues,wed,etc.
  Paramter: list[]
  Return: list[] of abbreviated datetimes
  '''

  def return_abbreviated_names(self, datetime):
    return [
      self.dt.strptime(date, '%Y-%M-%d').strftime('%a') for date in datetime
    ]


class WeatherAPI():

  def __init__(self):
    # Every key has reached its query limit <--
    #other api key: ZAX69FAMNDL292ME2JFVHFVYA
    #2nd api key:   325VLCKM959NXR9SGXLCYAPNR
    #og key:        PK44XXYLALVRT4LUY2WVUTEZZ
    #3rd key: DJGHTGDNSCPANG58M7GJQH4C8
    self.API_KEY = 'PK44XXYLALVRT4LUY2WVUTEZZ'
    self.clock = Clock()
    self.graph = Graph()
    self.current_weather = None
    self.zip = None
    self.current_data = []
    self.temps = None
    self.time = None
    self.daily_time = None
    self.daily_temp = None
    self.daily_icon = None

  '''
  Method: Resets the class variables, used when requesting forecast for a different zip_code
  Paramter: None
  Return: None
  '''

  def reset(self):
    self.current_weather = None
    self.zip = None
    self.current_data = []
    self.temps = None
    self.time = None
    self.daily_time = None
    self.daily_temp = None
    self.daily_icon = None

  '''
  Method: Setter function for class variable zip
  Params: int
  Return: None
  '''

  def set_zip(self, zip):
    self.zip = zip

  '''
  Method: Getter function for daily time
  Params: None
  Returns:  str self.daily_time 
  '''

  def get_daily_time(self):
    return self.daily_time

  '''
  Method: Getter function that returns the daily temp
  Params: None
  Returns: self.daily_temp
  '''

  def get_daily_temp(self):
    return self.daily_temp

  '''
  Method: Getter function that returns daily icon(description of forecast)
  Params: None
  Returns: str self.daily_icon
  '''

  def get_daily_icon(self):
    return self.daily_icon

  '''
  Method: Getter function
  Params: None
  Returns: returns self.zip
  '''

  def get_zip(self):
    return self.zip

  '''
  Method: Getter that returns self.time 
  Params: None
  Returns: str self.time
  '''

  def get_time(self):
    return self.time

  '''
  Method:  Getter function for self.temp
  Params: None
  Returns: int self.temp
  '''

  def get_temps(self):
    return self.temp

  '''
  Method: Getter function that returns current_data
  Params: None
  Returns: list[]
  '''

  def get_current_data(self):
    return self.current_data

  '''
  Method: Sends get request, returns object into a pd dataframe, data
          later gets divided into various list which gets used when plotting.
  Params: str zip 
  Returns: None
  ''' 
  def send_request(self, zip):
    url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{zip}/2022-10-13/2022-10-18?unitGroup=us&elements=datetime%2Cname%2Ctemp&include=hours&key={self.API_KEY}&contentType=csv'
    df = pd.read_csv(url)
    list_rows = df.to_numpy()
    time = [row[1] for row in list_rows]
    temp = [row[2] for row in list_rows]
    time = self.clock.convert_times(time)
    #print(time)
    self.temp, self.time = self.clock.return_list(temp, time)

  '''
  Method: Sends a get request for current data, parses data into various lists for later 
  use(graphing)
  Paramter: str zip
  Return: None
  ''' 
  def set_current_data(self, zip):
    url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{zip}?unitGroup=us&elements=resolvedAddress%2Ctemp%2Cdescription%2Cicon&include=current&key={self.API_KEY}&contentType=csv'
    df = pd.read_csv(url)
    list_rows = df.to_numpy()
    #print(list_rows)
    self.current_data.append([row[0] for row in list_rows])
    self.current_data.append([row[1] for row in list_rows][0])
    self.current_data.append([row[2] for row in list_rows][0])
    #print(self.current_data)

  '''
  Method: Sends a get request for daily data, parsed data into various lists for later use
  Paramter: str zip
  Return: None
  ''' 
  def send_request_daily(self, zip):
    url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{zip}/2022-10-13/2022-10-20?unitGroup=us&elements=datetime%2Ctemp%2Cicon&include=days&key={self.API_KEY}&contentType=csv'
    df = pd.read_csv(url)  #4
    list_rows = df.to_numpy()
    self.daily_time = [row[0] for row in list_rows]
    self.daily_temp = [row[1] for row in list_rows]
    self.daily_icon = [row[2] for row in list_rows]

    self.daily_time = self.clock.return_abbreviated_names(self.daily_time)

  '''
  Method: returns the graph from graph obj
  Paramter: None
  Return: Graph object
  ''' 
  def return_plot(self):
    return self.graph.return_plt()


class GUI:

  def __init__(self, root):
    self.master = root
    self.master.title("Weather App")
    self._API = WeatherAPI()
    self._GRAPH = Graph()
    self.pattern = re.compile('^\d{5}$')

    self.clear_day = tk.PhotoImage(file='clear_day.png', height=50, width=50)
    self.cloudy = tk.PhotoImage(file='cloudy.png', height=50, width=50)
    self.fog = tk.PhotoImage(file='fog.png', height=50, width=50)
    self.partly_cloudy = tk.PhotoImage(file='partly_cloudy.png',
                                       height=50,
                                       width=50)
    self.refresh = tk.PhotoImage(file='refresh.png', height=30, width=30)
    self.rain = tk.PhotoImage(file='rain.png', height=50, width=50)

    self.pick_image = {
      'clear-day': self.clear_day,
      'partly-cloudy-day': self.partly_cloudy,
      'fog': self.fog,
      'rain': self.rain,
      'cloudy': self.cloudy
    }

    self.master_frame = tk.Frame(self.master, padx=15, pady=25, bg='white')
    self.loading_frame = tk.Frame(self.master_frame, bg='white')
    self.error_label = tk.Label(self.loading_frame,
                                width=15,
                                height=3,
                                text='',
                                bg='white',
                                fg='red')

    self.initial_label = tk.Label(self.loading_frame,
                                  width=15,
                                  height=3,
                                  bg='white',
                                  text=' Enter 5-digit zip ')
    self.initial_entry = tk.Entry(self.loading_frame, width=8)
    #'''
    self.submit_zip = tk.Button(self.loading_frame,
                                width=8,
                                height=1,
                                text='submit',
                                command=self.loading)
    #'''
    self.data_frame = tk.Frame(self.master, bg='white')

    self.frame_1 = tk.Frame(self.data_frame, bg='white')
    self.inner_frame_1 = tk.Frame(self.frame_1, bg='white')

    self.icon = tk.Label(self.frame_1, bg='white', height=35)
    self.icon.grid(row=0, column=0, padx=(25, 0))

    self.temp = tk.Label(self.frame_1, bg='white', font=("Arial", 25))
    self.temp.grid(row=0, column=1)

    self.address = tk.Label(self.inner_frame_1,
                            bg='white',
                            anchor='e',
                            font=('Arial', 20))
    self.address.grid(row=0, sticky='e')

    self.description = tk.Label(self.inner_frame_1,
                                bg='white',
                                height=1,
                                width=25,
                                anchor='e',
                                font=('Arial', 15),
                                fg='#939596')
    self.description.grid(row=2, sticky='e')

    self.time = tk.Label(self.inner_frame_1,
                         bg='white',
                         font=('Arial', 13),
                         fg='#939596')
    self.time.grid(row=1, sticky='e')

    self.clear_button = tk.Button(self.frame_1,
                                  image=self.refresh,
                                  command=self.reset)  #with=5, height=5
    self.clear_button.grid(row=0, column=3, padx=10, pady=10)

    self.frame_2 = tk.Frame(self.data_frame, bg='white')
    self.frame_3 = tk.Frame(self.data_frame, bg='white')

    self.master_frame.grid(row=0, column=0)
    #self.data_frame.grid(row=0)
    self.loading_frame.grid(row=0)

    self.initial_label.grid(row=0, column=0)
    self.initial_entry.grid(row=0, column=1, padx=5)
    self.submit_zip.grid(row=0, column=2)
    self.error_label.grid(row=0, column=3)

    self.frame_1.grid(row=0)
    self.inner_frame_1.grid(row=0, column=2, sticky='e')
    self.frame_2.grid(row=1)
    self.frame_3.grid(row=2)

  '''
  Method: Function that controls the whole process, regex checks the zip, sends the get 
  request for data, uses a loading bar to hide the background proccesses. 
  Paramter: None
  Return: None
  '''

  def loading(self):
    self._API.reset()
    test_input = self.initial_entry.get()
    if not test_input:
      self.show_error(" No zip entered ")
      return
    if not self.check_zip(test_input):
      self.show_error(" Invalid Zip")
      return
    self._API.set_zip(test_input)
    self._API.send_request(self._API.get_zip())
    self.loading_frame.grid_remove()
    self.loading_bar = ttk.Progressbar(self.master_frame,
                                       length=500,
                                       orient='horizontal')
    self.loading_bar.grid(row=0, column=2)

    for x in range(5):
      if x == 1:
        self._API.set_current_data(self._API.get_zip())
        frame_1_data = self._API.get_current_data()
        self.icon.config(image=self.pick_image[frame_1_data[2]])
        #self.icon.config(image=self.cloudy)
        self.temp.config(text=f'{str(frame_1_data[1])[:2]} F')
        self.description.config(text=f'{frame_1_data[2]}')
        self.address.config(text=frame_1_data[0][0])
        self.time.config(text=self._API.clock.get_pst_compl())

      if x == 2:
        self._GRAPH.set_hours(self._API.get_time())
        self._GRAPH.set_temps(self._API.get_temps())
        fig = self._GRAPH.return_plt()
        canvas = FigureCanvasTkAgg(fig, master=self.frame_2)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, pady=(0, 15))

      if x == 4:
        self._API.send_request_daily(self._API.get_zip())
        date = self._API.get_daily_time()
        temp = self._API.get_daily_temp()
        icon = self._API.get_daily_icon()
        self.create_weekly_forecast(date, temp, icon, self.frame_3)

      self.loading_bar['value'] += 20
      self.master.update_idletasks()
      self.master.after(350)

    self.loading_bar.grid_remove()
    self.data_frame.grid(row=0)

  '''
  Method: Resets the UI back to loading_frame where it asks for user input
  Paramter: None
  Return: None
  '''

  def reset(self):
    self.data_frame.grid_remove()
    self.loading_frame.grid()

  '''
  Method: Creates the layout for frame_3(bottom row)
  Paramter: date[], temp[], icon[], tkinter.Frame.object
  Return: None
  '''

  def create_weekly_forecast(self, date, temp, icon, frame):
    for x in range(len(date)):
      new_frame = tk.Frame(frame, bg='white')
      new_frame.grid(column=x, row=0)

      date_label = tk.Label(new_frame, text=date[x], bg='white')
      date_label.grid(row=0, column=0)

      icon_label = tk.Label(new_frame,
                            image=self.pick_image[icon[x]],
                            width=76,
                            bg='white')
      icon_label.grid(row=1, column=0)

      temp_label = tk.Label(new_frame, text=temp[x], bg='white')
      temp_label.grid(row=2, column=0)
    frame.grid(row=2)

  '''
  Method: Regex checks the zip
  Paramter: str zip
  Return: Returns boolean
  '''

  def check_zip(self, zip):
    return True if re.match(self.pattern, zip) else False

  '''
  Method: Shows error when user inputs an unaccepted zip
  Paramter: tkinter.Label
  Return: None
  '''

  def show_error(self, error_message):
    self.error_label.config(text=error_message)


if __name__ == '__main__':
  root = tk.Tk()
  api = Clock()
  my_gui = GUI(root)
  root.mainloop()
