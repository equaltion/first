import json
import os

def load_language(lang_code='zh'):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    lang_file = os.path.join(base_dir,'config','locales', f'{lang_code}.json')
    
    try:
        with open(lang_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        fallback_file = os.path.join(base_dir, 'locales', 'en.json')
        with open(fallback_file, 'r', encoding='utf-8') as f:
            return json.load(f)


class Settings:
    def __init__(self):
        self.language='zh'
        self.lang = load_language('zh')
        self.extension = {'.cpp', '.h', '.py','.json','.txt','.m'}


class global_value:
    def __init__(self):
        self.worklist = []
        self.workstate ="path_input"
        self.running = 1



def command(user_input,set,work):
    match (work.workstate, user_input):
        case ("command", "1"):
            work.workstate="path_input"
            print(set.lang["cometopathinput"])
        case ("command", "2"):
            merge(set.lang,work.worklist)
        case ("command", "0"):
            work.workstate = "exit"
        case _:
            print(set.lang['cammandwrong'])
    if(work.workstate=="exit"):
        get=input(set.lang["exit"]+"\n"+set.lang[">>>"])
        if(get=="0"):
            work.running=0
        else :
            work.workstate="command"

def path_input(user_input,set,work):
    if (user_input=='1'):
       work.workstate="command"
       print(set.lang['backing'])
       return 
    if(os.path.isfile(user_input)):
        root, ext = os.path.splitext(user_input)
        if ext in set.extension:
            work.worklist.append(user_input)
            print(set.lang["pathaddsuccess"])
        else :
            print(set.lang['notallowed'])
    else:
        print(set.lang["notfile"])

def merge(lang,worklist): 
    if not worklist:
        print(lang["voidpathlist"])
        return
    with open(r"E:\gitproject\first\output.txt", 'w', encoding='utf-8') as out: 
        for _ in worklist:
            with open(_, 'r', encoding='utf-8') as f:
                content = f.read()
                out.write(f"\n{'='*10}\n{_}\n{'='*10}\n\n")
                out.write(content)




def main():
    set=Settings()
    work=global_value()
    print(set.lang["welcome"])
    while work.running != 0:
        user_input=input(set.lang[">>>"])
        if(work.workstate=="command"):
            command(user_input,set,work)
        elif(work.workstate=="path_input"):
            path_input(user_input,set,work)
if __name__ == "__main__":
    main()
