# FlyAlert — Custom Animated Alerts for PyQt5

**FlyAlert** is a customizable alert/dialog window component for PyQt5 applications.  
It provides a sleek, animated, frameless UI with optional shadow effects, buttons, and icon types.  
It also includes a compact version (`MinimalFlyAlert`) for quick notifications that disappear automatically.

---

## 🚀 Features

- 🔘 Modal alert with fade-in/out animation
- ✅ Supports multiple icon types: success, error, warning, info, question
- 🎨 Customizable title, message, and buttons (Confirm / Cancel / Info)
- 🧭 Flexible positioning (center, top-left, top-right, bottom-left, bottom-right)
- 🪟 Frameless and translucent window with drop shadow
- ⏱ `MinimalFlyAlert` supports auto-close timer and close button

---

## 📦 Requirements

- Python 3.6+
- PyQt5

Install with pip:

```bash
pip install PyQt5
```

---

## Installation

## 🧪 Example Usage

```python
from PyQt5.QtWidgets import QApplication
from flyalert import FlyAlert, MinimalFlyAlert  # Save the classes as flyalert.py

app = QApplication([])

# Full alert
alert = FlyAlert({
    'icon': 'success',
    'title': 'Success!',
    'message': 'Your action was completed successfully.',
    'ConfirmButton': True,
    'ConfirmButtonText': 'Okay',
    'ConfirmButtonColor': '#4CAF50',
    'ConfirmButtonClicked': lambda: print('Confirmed!')
})
alert.show()

# Compact alert
# alert = MinimalFlyAlert({
#     'icon': 'info',
#     'message': 'This will disappear in 5 seconds.',
#     'position': 'top-right',
#     'auto_close_time': 5000
# })
# alert.show()

app.exec_()
```

---

## ⚙️ Configuration Options

| Key                    | Type     | Description                                             | Default           |
|------------------------|----------|---------------------------------------------------------|-------------------|
| `icon`                 | str      | Icon type: success, error, warning, info, question      | "info"            |
| `title`                | str      | Dialog title text                                       | "Default Title"   |
| `message`              | str      | Dialog message text                                     | "Default Message" |
| `position`             | str      | Window position: top-left, top-right, bottom-left, etc. | "center"          |
| `ConfirmButton`        | bool     | Show confirm button                                     | True              |
| `ConfirmButtonText`    | str      | Text of confirm button                                  | "Confirm Button"  |
| `ConfirmButtonColor`   | str      | Background color of confirm button                      | "green"           |
| `ConfirmButtonClicked` | function | Callback function when confirm is clicked               | `self.accept()`   |
| `CancelButton`         | bool     | Show cancel button                                      | False             |
| `CancelButtonText`     | str      | Text of cancel button                                   | "Cancel Button"   |
| `CancelButtonColor`    | str      | Background color of cancel button                       | "red"             |
| `CancelButtonClicked`  | function | Callback function when cancel is clicked                | `self.reject()`   |
| `InfoButton`           | bool     | Show info button                                        | False             |
| `InfoButtonText`       | str      | Text of info button                                     | "Info Button"     |
| `InfoButtonColor`      | str      | Background color of info button                         | "blue"            |
| `InfoButtonClicked`    | function | Callback function when info is clicked                  | `self.accept()`   |
| `timer`                | int      | (MinimalFlyAlert only) milliseconds before auto-close   | 5000              |
| `rtl`                  | bool     | RTL (right-to-left) buttons layout                      | False             |