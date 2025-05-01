import tkinter as tk
import os
from menu import MenuPrincipal

if __name__ == "__main__":
    # Check if running in container
    if os.environ.get('DISPLAY', '') == '':
        print("No display available. If running in Docker, make sure X11 forwarding is configured.")
        exit(1)
    try:
        root = tk.Tk()
        app = MenuPrincipal(root)
        root.mainloop()
    except Exception as e:
        print("Error al iniciar la aplicación:", e)
        import traceback
        traceback.print_exc()