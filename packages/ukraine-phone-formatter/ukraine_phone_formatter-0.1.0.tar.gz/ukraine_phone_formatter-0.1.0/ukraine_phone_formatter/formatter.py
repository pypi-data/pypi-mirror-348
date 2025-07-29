import re

def format_ukrainian_phone(phone_number):
    cleaned_number = re.sub(r'[^0-9]', '', phone_number)

    if len(cleaned_number) == 10:
        return f"+38 ({cleaned_number[:3]}) {cleaned_number[3:6]}-{cleaned_number[6:8]}-{cleaned_number[8:]}"
    elif len(cleaned_number) == 12 and cleaned_number.startswith('38'):
        return f"+38 ({cleaned_number[2:5]}) {cleaned_number[5:8]}-{cleaned_number[8:10]}-{cleaned_number[10:]}"
    else:
        return phone_number

if __name__ == '__main__':
    print(format_ukrainian_phone("0501234567"))
    print(format_ukrainian_phone("380679876543"))
    print(format_ukrainian_phone("+380995554433"))
    print(format_ukrainian_phone("(093) 112-23-34"))
    print(format_ukrainian_phone("invalid"))