# Colorizator

Colorizator is a Python library that provides a simple way to add color to your terminal text output. This library is a copy of the popular `colorama` library, created for educational purposes to help users understand how terminal text coloring works in Python.

## Installation

You can install Colorizator using pip. Run the following command in your terminal:

```bash
pip install colorizator
```

## Usage

To use Colorizator, simply import it in your Python script and use the provided functions to color your text. Here’s a quick example:

```python
from colorizator import Fore, Back, Style

print(Fore.RED + 'This text is red!')
print(Back.GREEN + 'This background is green!')
print(Style.RESET_ALL + 'Back to normal text.')
```

### Available Colors

#### Foreground Colors
- `Fore.BLACK`
- `Fore.RED`
- `Fore.GREEN`
- `Fore.YELLOW`
- `Fore.BLUE`
- `Fore.MAGENTA`
- `Fore.CYAN`
- `Fore.WHITE`

#### Background Colors
- `Back.BLACK`
- `Back.RED`
- `Back.GREEN`
- `Back.YELLOW`
- `Back.BLUE`
- `Back.MAGENTA`
- `Back.CYAN`
- `Back.WHITE`

#### Styles
- `Style.DIM`
- `Style.NORMAL`
- `Style.BRIGHT`
- `Style.RESET_ALL`

## Example

Here’s a more comprehensive example demonstrating the use of Colorizator:

```python
from colorizator import Fore, Back, Style

print(Fore.GREEN + 'Success: Operation completed successfully!' + Style.RESET_ALL)
print(Back.RED + Fore.WHITE + 'Error: Something went wrong!' + Style.RESET_ALL)
print(Fore.YELLOW + 'Warning: Check your input.' + Style.RESET_ALL)
```

## Compatibility

Colorizator is compatible with Windows, macOS, and Linux. It automatically detects the operating system and applies the appropriate settings for terminal color support.

## Contributing

Contributions are welcome! If you would like to contribute to Colorizator, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Disclaimer

Colorizator is intended for educational purposes only. It is a copy of the `colorama` library and should not be used in production environments. For production use, please refer to the original `colorama` library.

## Acknowledgments

- [Colorama](https://pypi.org/project/colorama/) - The original library that inspired this educational project.