

from .cli import main

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        from .utils import console
        console.print("[red]\nInterrupted by user")
