## About Timol 

Timol is a molecular visualiser inside of the terminal. It relies on [ASE](https://wiki.fysik.dtu.dk/ase/) to read a molecular file (e.g. xyz) and displays it within a [Textual](https://github.com/textualize/textual/) app. 
![Timol_example](https://github.com/user-attachments/assets/7a90b016-a5ff-4bf6-8fdd-d2106261f61c)

## Installation

Timol is installable via pip (see [PyPI page](https://pypi.org/project/timol)) using `pip install timol`. The minimum python version is 3.9. 

## Usage

In order to visualise a file of interest, simply call `timol <file_path>`. An optional argument (`-i`) can be provided to index the file in case only specific frames are of interest (note that this can also be done from within the app using the `i` hotkey). This is particularly recommended for large (xyz) files to prevent excessive loading times.

In order to test the app without a molecular file at hand, use `timol test`. 

Note that the first time timol is launched, longer loading times are expected to initialise the package. 

## Functionalities

Timol provides a set of tools to conveniently manipulate the camera and more:
- **Help**: Press `h` to view available hotkeys from within the app
- **Rotate/tilt**: Drag the mouse or press `a/d` and `w/s`
- **Spin**: Press `z/x`
- **Pan**: Hold shift/alt and drag the mouse or press `shift+a/d`
- **Zoom**: Scroll or press `q/e`
- **Change index/frame**: Press `sift+q/e` or `left/right` (`up/down`) to go to the previous/next (or first/last) frame, press `g` to manually input the index

## MacOS Disclaimer

The default MacOS terminal app does not play nice with Textual apps and might make the rendering choppy. For more information and a solution to _some_ of the issues, see the [Textual FAQ](https://textual.textualize.io/FAQ/#why-doesnt-textual-look-good-on-macos)
