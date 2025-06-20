# Pomodoro Timer

A simple Pomodoro timer desktop application built with Python, [Tkinter](https://docs.python.org/3/library/tkinter.html), and [ttkbootstrap](https://ttkbootstrap.readthedocs.io/). This app helps you manage your work and break intervals using the Pomodoro Technique.

## Features

- Customizable work, short break, and long break durations
- Minimalist always-on-top window
- Visual and audio cues for work/break transitions
- Pause and resume functionality
- Custom font support (Poppins, Roboto)

## Requirements

- Python 3.x
- [ttkbootstrap](https://pypi.org/project/ttkbootstrap/)
- [requests](https://pypi.org/project/requests/)
- Windows (uses `winsound` for audio cues)

## Installation

1. Clone or download this repository.
2. Install dependencies:
    ```sh
    pip install ttkbootstrap requests
    ```
3. Make sure `Poppins-Regular.ttf` and `Roboto-Regular.ttf` are in the project directory.

## Usage

Run the script:

```sh
python script.py
```

You will be prompted to enter the durations (in minutes) for:
- Work session
- Short break
- Long break

The timer window will appear and start counting down. Use the Pause and Resume buttons as needed.

## Customization

- To change fonts, replace the `.ttf` files and update the `family` parameter in the script.
- To enable phone focus mode integration, uncomment the `trigger_focus_mode` function and related lines.

## License

This project is licensed under the MIT License.

---

*Inspired by the Pomodoro Technique for productivity.*
