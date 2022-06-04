# PrusaNylocAssistant
 A simpler and more intuitive way to calibrate the bed level of a Prusa Mk3 printer that has been outfitted with the [Nylock bed-leveling mod](https://www.reddit.com/r/prusa3d/comments/bp440f/full_guide_to_doing_nylock_mod_if_you_havent_you/).
 
 The application was built to solve a simple problem I had everytime I needed to level the bed of my Nyloc modded Prusa Mk3s+. The problem I experienced was having to use two different applications to perform each leveling cycle. First was a serial communication console such as Repertier Host to send commands and receive back data and then having to use a the [ g81 relative conversion](https://pcboy.github.io/g81_relative/) website to convert the received absolute bed mesh values into their relative correction values on each of the 8 screws for the bed.

The application combines the above two features into a simple to use interface that solves the problem of having to jump between different tools. Built with Python Tkinter for the user inteface and utilizing [PySerial](https://pyserial.readthedocs.io/en/latest/pyserial.html) to establish the serial communication between the software and the printer. The absolute to relative conversion is based on the same mathematical opperations done in [ g81 relative conversion](https://pcboy.github.io/g81_relative/)

## Special Mentions

Thank you to [PySerial](https://pyserial.readthedocs.io/en/latest/pyserial.html) for the amazing serial communication library and the excellent documentation.
Thank you to [pcboy](https://github.com/pcboy/g81_relative) for their great solution that helped make my 3D printer more capable and for open sourcing their software which inspired this application.
