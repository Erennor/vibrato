### Description
Template RFDuino Eclipse project using Eclipse CDT

### Prerequisities
* arm toolchain e.g. : arm toolchain provided in arduino IDE
* linux machine (not tested on Windows)
* Eclipse Luna or Juno (Not tested on Kepler)
* Eclipse "C/C++ GCC Cross Compiler Support" plugin
* wine installed with symbolink ling com1->/dev/ttUSB0 for RFDLoader
* define arm toolchain path in project Settings -> C/C++ build -> Settings -> Tool Settings -> Cross Settings 

### Limitations
* NO source files to build RFduinoSystem, RFduino, RFduinoBLE, RFduinoGZLL

### References
http://www.rfduino.com/
http://key-basher.blogspot.fr/2013/12/rfduino-on-linux.html
