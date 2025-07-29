import argparse
from colorama import Fore, init

def show_bird():
    print(Fore.CYAN + r"""
             \
             (o>
         \\_//)
          \_/_)
           _|_
        ___|___
       /       \__
      /  |      (@>
     /   \__/--._/
    /  _    \   \
   /__/ \   /___/
        (_(
    """ + Fore.YELLOW + """
    A beautiful bird in flight
    by Ankur
    """ + Fore.RESET)

def show_logo():
    print(Fore.GREEN + r"""
 █████╗ ███╗   ██╗██╗  ██╗██╗   ██╗██████╗ 
██╔══██╗████╗  ██║██║ ██╔╝██║   ██║██╔══██╗
███████║██╔██╗ ██║█████╔╝ ██║   ██║██████╔╝
██╔══██║██║╚██╗██║██╔═██╗ ██║   ██║██╔═\══╝ 
██║  ██║██║ ╚████║██║  ██╗╚██████╔╝██║  \\   
╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚═╝   \\
    """ + Fore.BLUE + """
        The official logo of ANKUR!
    """ + Fore.RESET)

def main():
    init()  # Initialize colorama
    parser = argparse.ArgumentParser(
        description="Ankur's Awesome CLI Tool",
        epilog="Example: ankur --bird --logo"
    )
    
    parser.add_argument('--bird', action='store_true', help="Show a beautiful ASCII bird")
    parser.add_argument('--logo', action='store_true', help="Show the ASCII logo of ANKUR")
    parser.add_argument('--all', action='store_true', help="Show both bird and logo")
    
    args = parser.parse_args()
    
    if args.all:
        show_logo()
        show_bird()
    elif args.bird:
        show_bird()
    elif args.logo:
        show_logo()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()