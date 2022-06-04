# UI
import time
from tkinter.ttk import Style
from tkinter import *

# system info and serial communication
import serial
import sys
import glob

window_width = 800
window_height = 400

root = Tk()
root.configure(background='snow')
root.title("Prusa Nylock Leveling Assistant")
root.geometry(f"{window_width}x{window_height}")

style = Style()

text_area = Frame(root, bg='#cacaca', width=400, height=400)
text_area.place(x=400, y=0)

dataLabel = Label(text_area, text='System Info', bg='#cacaca', fg='red',
                  font=('nunito sans', 14, 'bold'),
                  compound='center', highlightthickness=0, bd=0)

dataLabel.place(x=0, y=0)

bed_point = [
    Label(text_area, text='point 1', bg='snow', fg='black',
          font=('nunito sans', 14, 'bold'),
          compound='center', highlightthickness=0, bd=0),
    Label(text_area, text='point 2', bg='snow', fg='black',
          font=('nunito sans', 14, 'bold'),
          compound='center', highlightthickness=0, bd=0),
    Label(text_area, text='point 3', bg='snow', fg='black',
          font=('nunito sans', 14, 'bold'),
          compound='center', highlightthickness=0, bd=0),
    Label(text_area, text='point 4', bg='snow', fg='black',
          font=('nunito sans', 14, 'bold'),
          compound='center', highlightthickness=0, bd=0),
    Label(text_area, text='point 6', bg='snow', fg='black',
          font=('nunito sans', 14, 'bold'),
          compound='center', highlightthickness=0, bd=0),
    Label(text_area, text='point 7', bg='snow', fg='black',
          font=('nunito sans', 14, 'bold'),
          compound='center', highlightthickness=0, bd=0),
    Label(text_area, text='point 8', bg='snow', fg='black',
          font=('nunito sans', 14, 'bold'),
          compound='center', highlightthickness=0, bd=0),
    Label(text_area, text='point 9', bg='snow', fg='black',
          font=('nunito sans', 14, 'bold'),
          compound='center', highlightthickness=0, bd=0),

    Label(text_area, text='center', bg='snow', fg='black',
          font=('nunito sans', 14, 'bold'),
          compound='center', highlightthickness=0, bd=0),
]
bed_point[0].place(x=50, y=50)
bed_point[1].place(x=150, y=50)
bed_point[2].place(x=250, y=50)
bed_point[3].place(x=50, y=150)

bed_point[4].place(x=250, y=150)
bed_point[5].place(x=50, y=250)
bed_point[6].place(x=150, y=250)
bed_point[7].place(x=250, y=250)


Label(root, text="Nozzle temp").place(x=100, y=30)
Label(root, text="Bed temp").place(x=200, y=30)
nozzle_temp_input = Entry(root)
bed_temp_input = Entry(root)

nozzle_temp_input.insert(10, "230")
bed_temp_input.insert(10, "80")

nozzle_temp_input.place(x=100, y=50)
bed_temp_input.place(x=200, y=50)


def draw_degree_matrix(degrees):
    for i in range(8):
        bed_point[i].config(text=degrees[i])


printer = serial.Serial()


def list_serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


# port dropdown value

options = list_serial_ports()
print(options)
variable = StringVar(root)
variable.set(options[0])  # default value

port_options = OptionMenu(root, variable, *options)
port_options.place(x=100, y=0)


def connect():  # initialize the serial connection\
    global port_options
    printer.baudrate = 115200
    printer.port = variable.get()
    printer.timeout = 5
    printer.open()
    print("Connected to: ", printer.name)
    Label(root, text=printer.name, fg='grey').place(x=100, y=0)


def set_temp():

    bed = f'M140 S{bed_temp_input.get()}\n'
    nozzle = f'M104 S{nozzle_temp_input.get()}\n'

    printer.write(bed.encode('utf-8'))
    printer.write(nozzle.encode('utf-8'))


def cooldown():
    printer.write(b'M104 S0\n')
    printer.write(b'M140 S0\n')


def move():
    printer.write(b'G1 Z200 Y200 F5000\n')


def read_serial():
    serial_text = printer.readline(100).decode("utf-8")
    print(serial_text)
    dataLabel.config(text=serial_text)


def measure_bed():
    printer.write(b'G80\n')

    time.sleep(55)

    printer.readall()
    printer.reset_input_buffer()
    printer.write(b'G81\n')
    serial_text = printer.read_until(b'ok').decode("utf-8")

    number_start = serial_text.find('0.')
    number_end = serial_text.find('ok')
    serial_text = serial_text[number_start:number_end].replace("\n  ", '\n')
    print(serial_text)

    # serial_text = "0.12400  0.14250  0.13450  0.13450  0.12150  0.09300  0.11750\n\
    # 0.10050  0.13000  0.12500  0.08850  0.09050  0.11600  0.12300\n\
    # 0.12900  0.17650  0.16200  0.12275  0.11350  0.12900  0.12150\n\
    # 0.11450  0.16050  0.13050  0.12700  0.13350  0.12050  0.12600\n\
    # 0.16100  0.21200  0.19600  0.16800  0.17300  0.18200  0.13600\n\
    # 0.16550  0.20700  0.22250  0.17600  0.18200  0.18250  0.13900\n\
    # 0.13450  0.13350  0.13950  0.12800  0.13700  0.12850  0.13450"

    dataLabel.config(text="Bed Leveling Degree Corrections")
    distance = get_distance(serial_text)
    degrees = to_degrees(distance)
    draw_degree_matrix(degree_matrix_string(degrees))


def get_distance(ab_matrix):
    abs_points = ab_matrix.replace('\n', '  ').split('  ')
    rel_points = [0, 3, 6, 21, 27, 42, 45, 48]
    a = [0, 3, 6, 21, 27, 42, 45, 48]

    center = float(abs_points[24])
    for i in range(8):
        rel_points[i] = round((float(abs_points[ a[i] ]) - center), 2)

    print(f'rel_points:\n{rel_points} ')
    return rel_points


def to_degrees(distances):
    for i in range(8):
        screw_pitch = 0.5
        distances[i] = round((distances[i] / screw_pitch * 360),2)

    return distances


def degree_matrix_string(degrees):
    for i in range(8):
        postfix = 'CW' if degrees[i] > 0 else 'CCW'
        degrees[i] = f'{abs(degrees[i])}° {postfix if abs(degrees[i]) != 0.0 else ""}'
    print(f'degree:\n{degrees} ')
    return degrees

Button(root, text='Connect', font=('nunito', 16, 'bold'),
       compound='center', foreground="blue", highlightthickness=0, bd=0, bg="grey",
       command=lambda: connect()).place(x=0, y=0)

Button(root, text='Set Temp', font=('nunito', 16, 'bold'),
       compound='center', foreground="blue", highlightthickness=0, bd=0, bg="white",
       command=lambda: set_temp()).place(x=0, y=50)

Button(root, text='Measure', font=('nunito', 30, 'bold'),
       compound='center', foreground="blue", highlightthickness=0, bd=0, bg="white",
       command=lambda: measure_bed()).place(x=0, y=100)

Button(root, text='Move', font=('nunito', 30, 'bold'),
       compound='center', foreground="blue", highlightthickness=0, bd=0, bg="white",
       command=lambda: move()).place(x=200, y=100)

root.mainloop()
