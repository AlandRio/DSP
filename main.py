# Library for GUI
import mainmenu as mainmenu
import shared as shared

# causes app to start and enter a while loop while it is on


def main():
    mainmenu.createMain()
    shared.root.mainloop()

main()