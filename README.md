# WP Format List Generator

This canvas contains the files ready to copy-paste into a GitHub repo. Files included below are separated by headings — copy each into the appropriately named file in your repository.

---

A tiny Python 3 utility that converts lines in the format

```
https://site.com -> user:pass
site.com -> user:pass
www.site.com -> user:pass
```

into URLs useful for quick checks:

```
https://site.com/wp-login.php#user@pass
site.com/wp-login.php#user@pass
www.site.com/wp-login.php#user@pass
```

---

## README.md

````markdown
# WP Format List Converter

A small, dependency-free Python 3 script to convert `site -> user:pass` lines into `site/wp-login.php#user@pass` lines. Useful for transforming bruteforce success lists into clickable targets or for quick text processing.

## Features

- Preserves the left-hand host exactly as provided (keeps `http://`, `https://`, `www.` when present).
- Removes trailing slashes before appending `/wp-login.php`.
- Converts credential `user:pass` into `user@pass`.
- Ignores blank lines and lines that start with `#` (comments).
- Works with stdin or file input, and can write to stdout or an output file.

## Installation

This project requires Python 3.6+.

Clone the repo and use the script directly:

```bash
git clone <your-repo-url>
cd WP Format List Converter
python3 main.py -i input.txt -o output.txt
````

Or run via a pipe:

```bash
cat input.txt | python3 main.py > output.txt
```

## Usage

```text
usage: main.py [-h] [-i INPUT] [-o OUTPUT] [-s SEPARATOR]

Convert site -> user:pass into site/wp-login.php#user@pass

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input file (default: stdin)
  -o OUTPUT, --output OUTPUT
                        Output file (default: stdout)
  -s SEPARATOR, --separator SEPARATOR
                        Separator between site and creds (default: '->')
```

### Examples

From file to file:

```bash
python3 main.py -i input.txt -o output.txt
```

From stdin to stdout:

```bash
cat input.txt | python3 main.py > output.txt
```

Change separator (if your file uses a different token):

```bash
python3 main.py -s ":" -i input.txt -o output.txt
```

## Contributing

PRs and issues are welcome. Keep the project small and dependency-free. Add tests if you change parsing logic.
