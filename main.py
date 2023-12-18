from blessed import Terminal
import random, threading, time
from sys import argv,quit

exit = quit

if argv[0] == 'uninstall':
    from os import system
    print('Are you sure you want to uninstall? (Y/n)',end='')
    u = input()
    if u == 'Y' or u == '':
        system('sudo rm -rf /etc/monkeytype-cli')
        system('sudo rm /bin/monkeytype-cli')

def termtoosmall(width,height):
    print(term.clear,end='')
    print("Terminal Is Too Small.")
    print(f"Terminal Is {term.width}x{term.height}")
    print(f"Minimum Is {width}x{height}")

def getwords(n):
    words = []
    g = 0
    nochars = ['[', ']', '{', '}', '(', ')', '*', '&', '^', '%', '$', '#', '@', '!', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '`', '~', '?', '>', '<', ':', ';', '\\', '|', '-', '_', '=', '+', '/']
    with open('words.txt') as f:
        f = f.read()
        for char in nochars:
            f = f.strip(char)
        f = f.split('\n')
        while g < n:
            i = random.randint(0, len(f) - 1)
            words.append(f[i].lower())
            g += 1
            continue
        return words

def spaceout(value,length,space=' '):
    return space * ((length - len(value)) // 2) + str(value) + space * ((length - len(value) + 1) // 2)

global MIVars
MIVars = {}

class menuInput:
    def __init__(self,varname):
        self.input = ""
        self.varname = varname
        self.type = type
        MIVars[str(varname)] = self.input
    def handle(self, key, ismax):
        if not ismax == True:
            if key.isalpha() or key == ' ' or key.isdigit():
                self.input += key
        if key.code == 263:
            self.input = self.input[:-1]
        MIVars[str(self.varname)] = self.input
    def get(self):
        return self.input
def menuloop(title, tabs, selectable=True):
    try:
        default = term.inkey(0)
        key = default
        pos = 0
        tab = 0
        inputs = []
        while 1:
            if key.code == 261:
                tab += 1
                key = default
            elif key.code == 260:
                tab -= 1
                key = default
            tab = tab % (len(list(tabs.keys())))
            options = list(tabs.values())[tab]
            if key.code == 258:
                pos += 1
                key = default
            elif key.code == 259:
                pos -= 1
                key = default
            if selectable:
                if key.code == 343 or key == ' ':
                    if not isinstance(list(options.values())[pos], menuInput):
                        cmd = list(options.values())[pos]
                        if type(cmd) != (str):
                            cmd()
                        else:
                            if cmd == 'break':
                                break
                            elif cmd[:5] == 'return':
                                return eval(cmd[5:])
            elif key.code == 361:
                break
            pos = pos % len(options.keys())
            keys = list(options.keys())
            vals = list(options.values())
            print(term.clear)
            long = len(max(options.keys(), key = len))
            if len(title) > long:
                long = len(title)
            if len(' '.join(list(tabs.keys()))) > long:
                long = len(' '.join(list(tabs.keys())))
            long += 16
            if term.width < long+2 or term.height < 3 + len(options.keys()):
                termtoosmall(long+2,3 + len(options.keys()))
                time.sleep(0.1)
                continue

            print("\n" * ((term.height // 2) - (3 + len(options.keys())  )))

            #╭╮┬

            toptabs = list(tabs.keys())
            toptabs[tab] = term.black_on_white + toptabs[tab] + term.normal

            print(spaceout(f"╭{        spaceout(term.bold + title + term.normal,long + len(term.bold) + len(term.normal),'─')          }╮",term.width + len(term.bold) + len(term.normal)))

            if len(list(tabs.keys())) > 1:
                print(spaceout(f"├{        spaceout(' '.join(toptabs),long + len(term.black_on_white+term.normal),'─')          }┤",term.width + len(term.black_on_white+term.normal)))

            # print(spaceout(f"│{ + spaceout(title,long) + term.normal}│",term.width + len(term.bold) + len(term.normal)))

            optvals = list(options.values())
            for i in range(len(optvals)):
                if pos == i and selectable:
                    col = term.black_on_white + term.bold
                else:
                    col = term.normal
                if isinstance(optvals[i], menuInput):
                        maxlen = len(optvals[i].input) >= long - (len(list(options.keys())[i] + ': '))
                        if pos == i:
                            optvals[pos].handle(key,maxlen)
                        #key = default
                        print(spaceout(f"│{col + spaceout(keys[i] + ': ' + term.underline + optvals[i].get() + term.no_underline,long+len(term.underline+term.no_underline)) + term.normal}│",term.width + len(col) + len(term.normal) +len(term.underline+term.no_underline)))
                        #print(spaceout(f"│{col + spaceout(keys[i] + ': ' + term.underline + optvals[i].get() + term.no_underline,long+len(term.underline+term.no_underline)) + term.normal}│",term.width + len(col) + len(term.normal) +len(term.underline+term.no_underline)))
                else:
                    print(spaceout(f"│{col + spaceout(keys[i],long) + term.normal}│",term.width + len(col) + len(term.normal)))

            print(spaceout(f"╰{'─' * long}╯",term.width))
            key = term.inkey(0.2)
            continue
    except Exception as e:
        print(term.clear,term.home,'Exception In Menu Loop Call.')
        from sys import exc_info
        from os import path
        from traceback import format_tb
        print(f"{term.red}<ERROR> GOT {type(e).__name__}:\n{e}{term.normal}")
        print(f"{term.green}<INFO> Arguments for menu {term.bold}{title}:{term.normal}")
        try:
            k = list(options.keys())
            v = list(options.values())
            for tab in range(len(list(tabs.keys()))):
                print(f"Tab {tab}:")
                for i in range(len(k)):
                    print(f"{k[i]}: {v[i]}")
        except (TypeError,AttributeError) as e:
            print(f"{term.red}<ERROR> {type(e).__name__} occured while printing arguments. assuming incorrect tab formatting.{term.normal}")
            print(f"{term.red}<ERROR> Message: {term.white_on_black}{term.bold}{e}{term.normal}")
            print(f"{term.green}<INFO> Unformatted arguments:\n{tabs}{term.normal}")
        exc_type, exc_obj, exc_tb = exc_info()
        fname = path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        tb = format_tb(exc_tb)
        for line in tb:
            line = line.split('\n')[:-1]
            code = line[1]
            try:
                wrong = line[2]
            except ValueError:
                pass
            final = []
            for i in range(len(code)):
                try:
                    if wrong[i] == '^':
                        final.append(term.on_red + code[i] + term.normal)
                    else:
                        final.append(code[i])
                except:
                    final.append(code[i])
            final = ''.join(final)
            print(f"{line[0]}\n{final}")
        print(f"{term.blue}<SUGGESTION> Fix the code yourself and make a pull request on {term.link('https://github.com/Spelis/monkeytype-cli/','GitHub')}")
        print(f"{term.blue}<SUGGESTION> Report this error on {term.link('https://github.com/Spelis/monkeytype-cli/issues/new?assignees=&labels=bug&projects=&template=bug_report.md&title=','GitHub')}.{term.normal}")

        print("Press any key to quit.")
        term.inkey()
        exit(1)

def starttest():
    w = ' '.join(getwords(500))
    e = ''
    err = 0
    for b in range(30*10):
        key = term.inkey(0)
        if key.code == 361:
            g = menuloop('Quit?',{"1":{"No ":"break","Yes":mainmenu}})
            if g == "1":
                break
        if key.isalpha():
            try:
                if w[len(e)-1] != e[len(e)-1]:
                    err += 1
            except Exception:
                pass
            e += key.lower()
        if key == ' ':
            e += ' '
        if key.code == 263:
            e = e[:-1]
        offset = len(e) - 10
        if offset < 0:
            offset = 0
        printed = []
        for i in range(len(w)-1):
            if i < len(e):
                if e[i] == w[i]:
                    printed.append(term.normal + w[i] + term.normal)
                else:
                    printed.append(term.red + term.underline + w[i] + term.normal)
            else:
                if w[i] == len(e):
                    printed.append(term.black + term.underline + w[i] + term.normal)
                else:
                    printed.append(term.black + w[i] + term.normal)
        print(term.clear + ''.join(printed[offset:offset+50]) + '\n' + term.red + str(err) + term.normal + " " + str(round(b * 10) / 100))
        time.sleep(0.1)
    while 1:
        wpm = (len(e) / 30) * 30
        accuracy = len(e) / (len(e) + err) * 100
        menuloop("Test Completed!", {
        "Results": {
            f"WPM: {round(wpm)}": print,
            f"Accuracy: {round(accuracy, 2)}%": print, 
            "Redo Test": starttest,
            "Main Menu": mainmenu
        }
        })

def settings():
    menuloop("Settings",{"1:Settings File":{"No Options Here Yet.":print,"Back":"break"}})

def gogithub():
    import webbrowser
    webbrowser.open('http://github.com/Spelis/monkeytype-cli')

def mainmenu():
    menuloop("Main Menu",{"Main Menu": {"GitHub": gogithub, "Fun Input":menuInput('input'), "Settings":settings, "Exit":exit},"Start Test": {'Start Test': starttest}})

term = Terminal()
with term.fullscreen(), term.cbreak(),term.hidden_cursor():
    mainmenu()
