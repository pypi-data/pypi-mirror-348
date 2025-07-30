# contsys

Python library simplifying system script management with handy functions like clearing the console, setting the window title, and detecting the operating system (Windows, Linux, macOS).

## Features

Clear the console screen with `CMD.clear()`

Change the terminal window title with `CMD.title([NAME])`

Detect the operating system:  
   - `system.iswin32()` return **True** if the current OS is Windows, and return **False** if the current OS is not Windows.
   - `system.linux()` return **True** if the current OS is *Linux Based*, and return **False** if the current OS is not *Linux Based*.
   - `system.isdarwin()` return **True** if the current OS is MacOS, and return **False** if the current OS is not MacOS.

## Installation

You can install contsys using pip:

```bash
pip install contsys
```

## License

This project is under the MIT License.

## Contact

if you have any trouble or you want to suggest an amelioration you can contact me at [G-Azon782345@protonmail.com](mailto:G-Azon782345@protonmail.com)