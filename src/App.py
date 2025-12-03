import sys
import os

# Agrega la carpeta raíz (LibreriaUTP) al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.vistas.login import LoginView

if __name__ == "__main__":
    app = LoginView()
    ## app.mainloop()