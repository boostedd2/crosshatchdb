from cx_Freeze import setup, Executable

setup(
    name = "crosshAtchDB",
    version = "0.1",
    description = "This string describes my application.",
    executables = [Executable(script = "crosshatchbeta.py", base = "console")])
