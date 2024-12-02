# FILE: settings.py

# Initialize the default theme
theme = "Pacman"

def set_theme(new_theme):
    global theme
    theme = new_theme

def get_theme():
    return theme