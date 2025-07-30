# Kindle Clippings CLI

Kindle Clippings CLI enables you to convert your Kindle Clippings from raw text file to another format.

## Features
* Written in Python.
* No installation necessary - just use the [binary](https://github.com/MateDawid/Kindle-Clippings-CLI#installation).
* Converts `My Clippings.txt` to formats:
  * `.json`
  * `.xlsx`
* Easy to use.
* Works on Windows, Mac and Linux. 

## Installation

### Option 1: Binary
`Kindle Clippings CLI` is available for Windows, OSX (macOS) and Linux.

Download the latest binary from the [Releases page](https://github.com/MateDawid/Kindle-Clippings-CLI/releases).

Make sure to add the location of the binary to your `$PATH`.

### Option 2: PyPi
Kindle Clippings CLI is available as a Python package in PyPi.

```shell
pip install clippings
```

### Option 3: From source
To install Kindle Clippings CLI from source you need to have Python installed (version 12 at least).

* **Windows**
```shell
git clone https://github.com/MateDawid/Kindle-Clippings-CLI.git
cd Kindle-Clippings-CLI
python -m venv venv
.\venv\Scripts\activate
python -m pip install -U pip setuptools
python -m pip install poetry
poetry install --without dev
```
* **OSX (macOS) and Linux**
```shell
git clone https://github.com/MateDawid/Kindle-Clippings-CLI.git
cd Kindle-Clippings-CLI
python -m venv venv
source venv/bin/activate
python -m pip install -U pip setuptools
python -m pip install poetry
poetry install --without dev
```

## Usage

### Commands
```
convert  Convert Clippings file to one of supported formats.
```
### Convert command options
```
Usage: clippings [OPTIONS] COMMAND [ARGS]...

Options:
  -i, --input_path    Path to Clippings file (full or relative).
  -o, --output_path   Path to output file (full or relative).
  -f, --format        Output format. [json|excel]  [required]
```

### Converting `My Clippings.txt` to `.json`

* `My Clippings.txt` and output in current directory
  ```shell
  clippings convert --format json
  ```
  ```shell
  clippings convert -f json
  ```
* `My Clippings.txt` in other directory
  ```shell
  clippings convert -f json --input_path [PATH]/My Clippings.txt
  ```
  ```shell
  clippings convert -f json -i [PATH]/My Clippings.txt
  ```
* Output in other directory
  ```shell
  clippings convert -f json --output_path [PATH]/My Clippings.json
  ```
  ```shell
  clippings convert -f json -o [PATH]/My Clippings.json
  ```

### Converting `My Clippings.txt` to `.xlsx`

* `My Clippings.txt` and output in current directory
  ```shell
  clippings convert --format excel
  ```
  ```shell
  clippings convert -f excel
  ```
* `My Clippings.txt` in other directory
  ```shell
  clippings convert -f excel --input_path [PATH]/My Clippings.txt
  ```
  ```shell
  clippings convert -f excel -i [PATH]/My Clippings.txt
  ```
* Output in other directory
  ```shell
  clippings convert -f excel --output_path [PATH]/My Clippings.xlsx
  ```
  ```shell
  clippings convert -f excel -o [PATH]/My Clippings.xlsx
  ```

## Bug Reports & Feature Requests

Please use the [issue tracker](https://github.com/MateDawid/Kindle-Clippings-CLI/issues) to report any bugs or feature requests.

## Contact

Created by [@matedawid](https://linkedin.com/in/matedawid) - if you have any questions, just contact me!