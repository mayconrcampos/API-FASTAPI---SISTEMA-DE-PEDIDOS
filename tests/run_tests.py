import argparse
import subprocess


def main():
    parser = argparse.ArgumentParser(description='Run tests')
    parser.add_argument('--one', type=str, help='Run a single test')
    args = parser.parse_args()

    if args.one:
        cmd = f'pytest {args.one}'
    else:
        cmd = 'pytest -W ignore::DeprecationWarning'

    subprocess.run(cmd, shell=True)


if __name__ == '__main__':
    main()