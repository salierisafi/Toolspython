import sys
import os
import traceback
import re
import tty
import termios

WHITE = "\033[97m"
PURPLE = "\033[95m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

def custerror(msg: str) -> None: # untuk custom error gantikan raise
    stack = traceback.extract_stack() # ngambil semua frame call stack
    call_frame = stack[-3]

    print(f'{WHITE} File "{PURPLE}{call_frame.filename}{WHITE}", {WHITE}line {PURPLE}{call_frame.lineno}{WHITE}, in {call_frame.name}{RESET}', file=sys.stderr)
    if call_frame.line:
        clean_line = call_frame.line.split('#')[0].rstrip()
        print(f' {RED}{clean_line}{RESET}', file=sys.stderr)
    print(f'{PURPLE}{BOLD}ValueError{RESET}: {PURPLE}{msg}{RESET}', file=sys.stderr)

# Menggunakan Input Character khusus Linux 
def inputchar() -> str:
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
        if ch == '\x1b': 
            ch += sys.stdin.read(2)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

# ===================
# Logika Utama
memory = [] # manipulasi memori

def readline(prompt="", input_val="", end_line="", type="string") -> str:
    valid_type = ["string", "integer", "float"]
    if type not in valid_type:
        custerror(f"Invalid data type '{type}'. Choose one of: {valid_type}")
        return

    cursor_position = len(input_val)

    sys.stdout.write(prompt + input_val + end_line)
    if len(end_line) > 0:
        sys.stdout.write("\b" * len(end_line))
    sys.stdout.flush()

    memocount = len(memory)
    temp_memo = ""

    while True:
        char = inputchar()
        
        if char in ['\r', '\n']:
            if cursor_position < len(input_val):
                sys.stdout.write(input_val[cursor_position:] + end_line)
            sys.stdout.write("\n")
            sys.stdout.flush()
            try:
                memo = memory[-1]
            except IndexError:
                memo = ""
            if input_val.strip() not in ["", memo]: 
                memory.append(input_val)
            return input_val
        
        # Backspace
        elif char == '\x7f':
            if cursor_position > 0:
                input_val = input_val[:cursor_position-1] + input_val[cursor_position:]
                cursor_position -= 1
                sisa_kanan = input_val[cursor_position:] + end_line
                
                sys.stdout.write("\b\x1b[P")
                if len(sisa_kanan) > 0:
                    sys.stdout.write(sisa_kanan + "\b" * len(sisa_kanan))
                sys.stdout.flush()

        elif char == '\x1b[A': # Panah atas
            if memocount > 0:
                if memocount == len(memory):
                    temp_memo = input_val
                memocount -= 1
                
                if cursor_position > 0:
                    sys.stdout.write("\b" * cursor_position)
                
                panjang_lama = len(input_val) + len(end_line)
                sys.stdout.write(" " * panjang_lama + "\b" * panjang_lama)
                
                input_val = memory[memocount]
                cursor_position = len(input_val)
                
                sys.stdout.write(input_val + end_line) 
                if len(end_line) > 0: 
                    sys.stdout.write("\b" * len(end_line))
                sys.stdout.flush()

        elif char == '\x1b[B': # Panah bawah
            if memocount < len(memory):
                memocount += 1
                
                if cursor_position > 0:
                    sys.stdout.write("\b" * cursor_position)
                
                panjang_lama = len(input_val) + len(end_line)
                sys.stdout.write(" " * panjang_lama + "\b" * panjang_lama)
                
                if memocount == len(memory): 
                    input_val = temp_memo
                else: 
                    input_val = memory[memocount]
                    
                cursor_position = len(input_val)
                sys.stdout.write(input_val + end_line)
                if len(end_line) > 0: 
                    sys.stdout.write("\b" * len(end_line))
                sys.stdout.flush()
            
        elif char == '\x1b[C': # Kursor ke kanan
            if cursor_position < len(input_val):
                sys.stdout.write(input_val[cursor_position])
                cursor_position += 1
                sys.stdout.flush()

        elif char == '\x1b[D': # Kursor ke kiri
            if cursor_position > 0:
                cursor_position -= 1
                sys.stdout.write("\b")
                sys.stdout.flush()

        elif char == "-" and not input_val: 
            input_val = "-"
            cursor_position = 1
            sys.stdout.write(char + end_line)
            if end_line:
                sys.stdout.write("\b" * len(end_line))                                          
            sys.stdout.flush()

        elif char.isprintable():
            inputable = False
            if type == "integer":
                if char.isdigit(): 
                    inputable = True
            elif type == "float":
                if char.isdigit() or (char == "." and "." not in input_val): 
                    inputable = True
            else:
                inputable = True   
                
            if inputable:
                sisa_kanan = input_val[cursor_position:] + end_line
                input_val = input_val[:cursor_position] + char + input_val[cursor_position:]
                cursor_position += 1
                
                sys.stdout.write(char + sisa_kanan)
                if len(sisa_kanan) > 0:
                    sys.stdout.write("\b" * len(sisa_kanan))
                sys.stdout.flush()

        elif char in ['\x1b[H', '\x01']: # Home
            if cursor_position > 0:
                sys.stdout.write("\b" * cursor_position)
                cursor_position = 0
                sys.stdout.flush()

        elif char in ['\x1b[F', '\x05']: # End
            if cursor_position < len(input_val):
                sisa_teks = input_val[cursor_position:]
                sys.stdout.write(sisa_teks)
                cursor_position = len(input_val)
                sys.stdout.flush()

        # Ctrl C, D, L
        elif char == '\x03':
            sys.stdout.write("^C\n")
            return "^\u200bC"
        elif char == '\x04':
            sys.stdout.write("^D\n")
            return "^\u200bD"
        elif char == '\x0c':
            sys.stdout.write("^L\n")
            return "^\u200bL"

# ==========================================
if not os.path.isdir(".tools"):
    os.system("mkdir .tools && cd .tools")
else: 
    os.system("cd .tools")
    
dir_cd = ".tools/"
dircdx = "tools/"
len_dir = 2
dir_cdx = dircdx

# Tanpa .NET yaitu C# (cs) dan VB (vb)
# Menggunakan penamaan paket bawaan Arch Linux / pacman
lang_map = {
    "c":   {"pkg": "clang", "cmd": "clang"},
    "cpp": {"pkg": "clang", "cmd": "clang++"},
    "js":  {"pkg": "nodejs", "cmd": "node"},
    "ts":  {"pkg": "nodejs", "cmd": "node"},
    "lua": {"pkg": "lua", "cmd": "lua"},
    "rs":  {"pkg": "rust", "cmd": "rustc"},
    "go":  {"pkg": "go", "cmd": "go"},
    "py":  {"pkg": "python", "cmd": "python"},
    "php": {"pkg": "php", "cmd": "php"},
    "asm": {"pkg": "nasm", "cmd": "nasm"}
}

def run(namafile):
    if namafile == "run":
        print("run <file>")
        return
    elif not os.path.isfile(f"{dir_cd}{namafile}"):
        print("File tidak ditemukan")
        return

    nama = ".".join(namafile.split(".")[:-1])
    existensi = namafile.split(".")[-1]
    compile_ext = ["c", "cpp", "rs", "go"]
    
    try:
        cmd = lang_map[existensi]["cmd"]
    except KeyError:
        if existensi not in ["html", "sh"]:
            print("Format file tidak diketahui.")
            return

    if (existensi in ["html", "sh"] or os.system(f"command -v {cmd} > /dev/null 2>&1") == 0):
        if existensi in compile_ext:
            compile_f(namafile, nama, existensi)
        elif existensi == "html":
            if os.system("command -v python > /dev/null 2>&1") == 0:
                filename = namafile
                if namafile == "index.html": 
                    filename = ""
                # Menggunakan xdg-open standar Desktop Linux pengganti termux-open
                os.system(f"cd ./{dir_cd} && python -m http.server 8080 & xdg-open http://localhost:8080/{filename}")
            else:
                print("Kok bisa, belum install python, Install python dulu.")
                print("Ketik lang py")
        elif existensi == "asm":
            compile_f(namafile, nama, existensi)
            if os.system("command -v clang > /dev/null 2>&1") == 0:
                compile_f(nama + ".o", nama, "o")
            else:
                print("Install clang dulu")
                print("Ketik lang c")
            os.system(f"cd ~/ && rm {nama}.o")
        else:
            run_f(namafile, existensi)
    else:
        print(f"Bahasa '{existensi}' tidak terinstall")
        print(f"Ketik 'lang {cmd}' untuk install.")

def compile_f(namafile, nama, existensi):
    x = "cd ~/ && "
    compiler = "" 
    namaoutput = ""
    if existensi == "rs": 
        compiler = "rustc"
    elif existensi == "go": 
        compiler = "go build"
    elif existensi == "asm": 
        compiler = "nasm -f elf64"
        namaoutput = f" -o {nama}.o"
        os.system(f"cp {dir_cd}{namafile} ~/")
        os.system(f"{x}{compiler} {namafile}{namaoutput}")
        os.system(f"{x}rm {namafile}")
        return
    elif existensi == "o":
        compiler = "clang"
        namaoutput = f" -o {nama}"
        os.system(f"{x}{compiler} {namafile}{namaoutput}")
        os.system(f"{x}./{nama}")
        os.system(f"{x}rm {nama}")
        return
    else: 
        y = existensi.replace("c", "").replace("p", "+")
        compiler = f"clang{y}"
        namaoutput = f" -lm -o {nama}"    

    os.system(f"cp {dir_cd}{namafile} ~/")
    os.system(f"{x}{compiler} {namafile}{namaoutput}")
    os.system(f"{x}./{nama}")
    os.system(f"{x}rm {namafile} && rm {nama}")

def run_f(namafile, existensi):
    if existensi == "py": run = "python"
    elif existensi == "js": run = "node"
    elif existensi == "ts": run = "node --experimental-strip-types"
    elif existensi == "lua": run = "lua"
    elif existensi == "php": run = "php"
    elif existensi == "sh": run = "bash"
    os.system(f"{run} {dir_cd}{namafile}")

def info(): 
    print("""\n
  run <file>      - Menjalankan file pemograman
  lang <language> - Info/install bahasa pemograman
  clear           - Membersihkan terminal
  end             - Hentikan localhost:8080
  cd              - Masuk ke direktori
  exit            - Keluar
""")

def lang(language):
    language = language.lower()
    if language == "lang":
        print("lang <language>")
        return
    # Menghapus 'cs' dan 'vb' dari autokoreksi
    inisial = {
        "a": ["asm"],
        "c": ["c", "cpp"],
        "j": ["js"],
        "p": ["py", "php"],
        "t": ["ts"],
        "l": ["lua"],
        "r": ["rs"],
        "g": ["go"]
    }
    try:
        pkg = lang_map[language]["pkg"]
        cmd = lang_map[language]["cmd"]
    except KeyError:
        print(f"Bahasa pemograman {language} tidak ditemukan.")
        try:
            auto = inisial[language[0]]
            print("Mungkin maksud anda :")
            for i in range(len(auto)):
                print("Bahasa", auto[i])
            print()
        except KeyError: 
            print()
        return

    if os.system(f"command -v {cmd} > /dev/null 2>&1") == 0:
        os.system(f"{cmd} --version")
    else:
        print("Bahasa tidak tersedia.")
        print("Apakah anda ingin menginstallnya?", end="")
        pilihan = input("(y/n) :")
        if (pilihan + " ")[0].lower() == "y":
            # Perintah khusus Arch / EndeavourOS
            os.system(f"sudo pacman -S --noconfirm {pkg}") 
        else:
            return

def cd(folder):
    global dir_cd, dir_1, dircdx, len_dir
    if folder in ["cd", ""]:
        print("cd <dir>")
        return
    elif not os.path.isdir(f"{dir_cd}{folder}"):
        print("Folder tidak ditemukan")                   
        return
    if folder == "..":
        if len_dir <= 2:
            print("Akses ditolak")
        else:
            dir_cd = (("\u200b" + "/".join(dir_cd.split("/")[:-2]) + "/")
                      .replace("\u200b/", "")
                      .replace("\u200b", ""))
    elif folder == ".": 
        pass
    else:
        dir_cd = f"{dir_cd}{folder}/"

    dircdx = ((f"tools/{dir_cd.replace('.tools/', '')}")
             .split("../")[-1])
    len_dir = len(dircdx.split("/"))
    if len_dir > 3: 
        dircdx = (".../" + "/".join(dircdx.split("/")[-3:-1]) + "/")

while True:
    menu = readline(f"\x1b[32m~/{dircdx}\x1b[0m $ ").strip()
    params = menu.split(" ")[-1]
    if "/alat.py" in params:
        print("Anda tidak memiliki akses")
        continue
    perintah = menu.split(" ")[0].strip()
    if perintah == "run": 
        run(params)
    elif perintah == "help": 
        info()
    elif perintah == "lang": 
        lang(params)
    elif perintah in ["end", "^\u200bC"]: 
        os.system('pkill -9 -f "http.server"')
    elif perintah == "cd": 
        cd(params)
    elif perintah in ["exit", "^\u200bD"]: 
        os.system('pkill -9 -f "http.server"')
        break
    elif perintah in ["clear", "^\u200bL"]: 
        os.system('clear')
    else: 
        os.system(f"cd ./{dir_cd} && {menu}")