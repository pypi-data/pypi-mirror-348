import argparse

def main():
    parser = argparse.ArgumentParser(
        prog="wakeword-detector",
        description="CLI for training, detecting, and managing wakeword models"
    )

    # Import version without triggering heavy dependencies
    try:
        from .__version__ import __version__
    except ImportError:
        __version__ = "unknown"

    parser.add_argument("--version", action="store_true", help="Show version and exit")

    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("start", help="Interactive wizard to train a model from scratch")
    subparsers.add_parser("train", help="Train the wakeword model")
    subparsers.add_parser("record", help="Record audio samples")
    subparsers.add_parser("extract", help="Extract features from audio files")
    subparsers.add_parser("browse", help="Browse and play recorded audio")
    subparsers.add_parser("serve", help="Start the wakeword detection WebSocket server")

    args = parser.parse_args()

    # Handle version output early and safely
    if args.version:
        print(f"{parser.prog} v{__version__}")
        return

    elif args.command == "start":
        from .start import main as start_main
        start_main()

    if args.command == "serve":
        from .server import main as server_main
        server_main()

    elif args.command == "train":
        from .train import train_wakeword_model
        train_wakeword_model()

    elif args.command == "record":
        from .record_audio import main as record_main
        record_main()

    elif args.command == "extract":
        from .extract_features import main as extract_main
        extract_main()

    elif args.command == "browse":
        from .browse_audio import main as browse_main
        browse_main()


    else:
        parser.print_help()

if __name__ == "__main__":
    main()
