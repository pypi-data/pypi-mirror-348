# Ukraine Phone Formatter (python)

Ukraine Phone Formatter is a simple Python library that formats Ukrainian phone numbers into a readable and standardized format

## Installation
```bash
pip install ukraine-phone-formatter
```

## Usage
```python
from ukraine_phone_formatter import format_ukrainian_phone

phone_number = "0501234567"
formatted_number = format_ukrainian_phone(phone_number)
print(formatted_number)  # Output: +38 (050) 123-45-67

phone_number_with_code = "380679876543"
formatted_number_with_code = format_ukrainian_phone(phone_number_with_code)
print(formatted_number_with_code)  # Output: +38 (067) 987-65-43
```

## License
This project is licensed under the [MIT License](LICENSE)

## Author
- [PyPi](https://pypi.org/user/stkossman/)
- [Github](https://github.com/stkossman)
- [Library as Ruby Gem](https://github.com/stkossman/ukraine_phone_formatter)