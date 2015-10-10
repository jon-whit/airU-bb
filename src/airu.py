import argparse


if __name__ == '__main__':
    """
    Main entry point for the AirU software layer for the Raspberry Pi.
    """

    # Create the command-line interface for this application
    parser = argparse.ArgumentParser(description='The airU main application.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enables verbose output to stdout.')
    parser.add_argument('-c', '--config', default='.', help='A directory containing the app configurations.')
    parser.add_argument('-l', '--log', help='The directory where logs should be written to.')

    args = parser.parse_args()
