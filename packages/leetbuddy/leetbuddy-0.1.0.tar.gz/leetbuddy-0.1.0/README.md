# LeetBuddy CLI

A command-line tool to help you solve LeetCode problems more efficiently.

## Features

- Sign in to LeetCode and save credentials
- Get today's Problem of the Day
- Automatically create workspace with problem statement and solution template
- Submit solutions (coming soon)

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd leetbuddy
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Make the script executable:
```bash
chmod +x leetbuddy.py
```

4. Create a symbolic link to make it available system-wide (optional):
```bash
sudo ln -s $(pwd)/leetbuddy.py /usr/local/bin/leetbuddy
```

Or install it via PyPI (after publishing):
```bash
pip install leetbuddy
```

## Usage

### Sign in to LeetCode
```bash
leetbuddy signin
```
This will prompt you for your LeetCode username and password and save them securely.

### Get Today's Problem
```bash
leetbuddy today
```
This will:
1. Fetch today's Problem of the Day
2. Create a new directory with the problem name
3. Create a README.md with the problem statement
4. Create a solution.cpp file with a basic template
5. Open VS Code in the problem directory

### Submit Solution (Coming Soon)
```bash
leetbuddy submit
```
This will submit your solution to LeetCode and show the results.

## Requirements

- Python 3.7+
- Chrome browser (for Selenium)
- VS Code (for opening the workspace)
- click
- requests
- urllib3

## License
MIT

## Note

Your LeetCode credentials are stored in `~/.leetbuddy_config.json`. Make sure to keep this file secure.