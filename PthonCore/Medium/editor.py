# write your code here
available_format = ['plain', 'bold', 'italic', 'header', 'link', 'inline-code', 'ordered-list', 'unordered-list',
                    'new-line', '!help', '!done']
# available_format = ['plain', 'bold', 'italic', 'header', 'link', 'inline-code',
#                     'new-line', '!help', '!done']
full_text = ""


def plain():
    global full_text
    full_text += input("Text:")


def bold():
    global full_text
    full_text += "**" + input("Text:") + "**"


def italic():
    global full_text
    full_text += "*" + input("Text:") + "*"


def header():
    global full_text
    while True:
        try:
            num = int(input("Level:"))
            if num not in [1, 2, 3, 4, 5, 6]:
                print("The level should be within the range of 1 to 6")
            elif full_text == "":
                full_text += '#' * num + ' ' + input("Text:") + '\n'
                break
            else:
                full_text += '\n' + '#'*num + ' ' + input("Text:") + '\n'
                break
        except ValueError:
            print("The level should be within the range of 1 to 6")


def link():
    global full_text
    label = input("Label:")
    url = input("URL:")
    full_text += f"[{label}]({url})"


def inline_code():
    global full_text
    full_text += "`" + input("Text:") + "`"


def new_line():
    global full_text
    full_text += '\n'


def lists(mode='ordered-list'):
    global full_text
    while True:
        try:
            rows = int(input("Number of rows:"))
            if rows < 1:
                print("The number of rows should be greater than zero")
            else:
                if full_text != "":
                    full_text += '\n'
                for i in range(1, rows+1):
                    r_text = input(f"Row #{i}:")
                    pref = f'{i}. ' if mode == 'ordered-list' else '* '
                    full_text += pref + r_text + '\n'
                break
        except ValueError:
            print("The number of rows should be greater than zero")


def save_file():
    global full_text
    with open("output.md", 'w') as f:
        f.write(full_text)


while True:
    ans = input("Choose a formatter:")
    if ans not in available_format:
        print('Unknown formatting type or command')
    elif ans == '!help':
        print('Available formatters: plain bold italic header link inline-code ordered-list unordered-list new-line\n\
        Special commands: !help !done')
    elif ans == '!done':
        save_file()
        break
    else:
        if ans == 'plain':
            plain()
        elif ans == 'bold':
            bold()
        elif ans == 'italic':
            italic()
        elif ans == 'header':
            header()
        elif ans == 'link':
            link()
        elif ans == 'inline-code':
            inline_code()
        elif ans == 'new-line':
            new_line()
        elif ans in ['ordered-list', 'unordered-list']:
            lists(ans)
        print(full_text)
