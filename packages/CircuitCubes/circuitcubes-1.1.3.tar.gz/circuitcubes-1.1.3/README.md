# CircuitCubes (Version 1.1.3)

*CircuitCubes* is a package for easily controlling Bluetooth Circuit Cubes with Python. 

This package makes it as simple as possible to start interacting with your Circuit Cube, **requiring only two lines of code to initialize** the Circuit Cube. 
```
from CircuitCubes import Cube
cube = Cube()
```

This package is verbose by default, but the keyword argument `verbose=False` can be passed to the `Cube` class. 

## Motor commands

To turn on a single motor, use `Cube.run_motor` method. 
* It takes the arguments `letter` ('A', 'B', or 'C'), `velocity` (-100 to 100) and `time`. 
* The keyword argument `smooth` if set to true will keep the motor running after the time is done. 

To run multiple motors, use the `Cube.run_motors` method. 
* This method is very similar to the previous, except its first two arguments take the lists `letters` and `velocities`. 

To stop all motors, use the `Cube.halt` method. 

To disconnect the Circuit Cube, use the `Cube.disconnect` method. 

## Other functionality

The `Cube.information` method prints details about the connected Circuit Cube to the terminal. 
* Device name (should always be Tenka). 
* BLE appearance code. 
* Serial number. 
* Firmware version. 
* Hardware version. 
* Software version. 
* Battery voltage. 

The CircuitCubes.Cube() class has three keyword arguments. These are not necessary to input when first initializing the Circuit Cube. 
* `verbose` (boolean) when true will output details to the terminal
* `address` (string in format 'aa:bb:cc:dd:ee:ff) allows providing the Bluetooth hardware address of your Circuit Cube. 
* `jupyter` (boolean) allows specifying whether the package is in an interactive environment. 

The `Cube.help` method prints a link to the project GitHub repository in the terminal.

The `Cube.battery` method returns the Circuit Cube battery voltage. 

## Technicalities 

This package is made up of two classes `Cube` and `Constants`. 
* Most users should not need to interact with the constants class. 
* The constants class contains all of the Bluetooth Circuit Cube's BLE GATT characteristics, descriptors, and handles. 
* These constants can be printed to the terminal using the `cube.get_constant' method, which takes an integer from 0 to 28 as input. 
* The input integers correspond to indices of a list (for example 2 corresponds to the BLE transmission GATT characteristic). 

This package contains lots of **a**synchronous code, but conveniently makes it appear synchronous to the user. Therefore, using the *CircuitCubes* with asynchronous python code is not recommended. 

On computers running macOS, Bluetooth addresses are in a 128-bit UUID because of the operating system's Core Bluetooth framework. Also because of this, running in a non-interactive Python environment may not work properly. However, running in a Jupyter notebook will work properly. 

## Planned development 

* More advanced motor control methods. 
* Support for using more than one CircuitCube at the same time. 
* Functionality based on battery level. 

## Links 

[Project GitHub Repository](https://github.com/simon-code-git/CircuitCubes)

[simonwong.site](https://www.simonwong.site)
