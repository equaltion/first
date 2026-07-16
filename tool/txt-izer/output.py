import json
import os

def load_language(lang_code='zh'):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    lang_file = os.path.join(base_dir, 'locales', f'{lang_code}.json')
    
    try:
        with open(lang_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        fallback_file = os.path.join(base_dir, 'locales', 'en.json')
        with open(fallback_file, 'r', encoding='utf-8') as f:
            return json.load(f)

lan = None
running = 1
workstate = "command"
worklist = [] 
extension = {'.cpp', '.h', '.py','.json','.txt'}
def initializer(language):
    global lan
    global running
    global worklist
    global workstate
    lan = load_language('zh')
    print(lan["welcome"])


def command(user_input):
    global workstate
    global lan
    match (workstate, user_input):
        case ("command", "1"):
            workstate="path_input"
            print(lan["cometopathinput"])
        case ("command", "2"):
            merge()
        case ("command", "0"):
            workstate = "exit"
        case _:
            print('cammandwrong')

def path_input(user_input):
    global lan
    global workstate
    global worklist
    if (user_input=='1'):
       workstate="command"
       print('backing')
       return 
    if(os.path.isfile(user_input)):
        global extension
        root, ext = os.path.splitext(user_input)
        if ext in extension:
            worklist.append(user_input)
            print(lan["pathaddsuccess"])
        else :
            print('notallowed')
    else:
        print('notfile')

def merge():
    global lan
    global worklist
    if not worklist:
        print(lan["voidpathlist"])
        return
    with open(r"E:\gitproject\first\output.txt", 'w', encoding='utf-8') as out: 
        for _ in worklist:
            with open(_, 'r', encoding='utf-8') as f:
                content = f.read()
                out.write(f"\n{'='*10}\n{_}\n{'='*10}\n\n")
                out.write(content)

def exit_part(lan):
    if(workstate=="exit"):
        get=input(lan["exit"]+"\n"+lan[">>>"])
        if(get=="0"):
            return 0 
        else :
            return 1
    else:
        return 1

def main():
    initializer('zh')
    global lan
    global running
    global worklist
    while running != 0:
        user_input=input(lan[">>>"])
        if(workstate=="command"):
            command(user_input)
        elif(workstate=="path_input"):
            path_input(user_input)
        running=exit_part(lan)

if __name__ == "__main__":
    main()
