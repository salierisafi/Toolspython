import sys

WHITE = "\033[97m"
PURPLE = "\033[95m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

def custerror(msg: str) -> None: #untuk custom error gantikan raise
    stack = traceback.extract_stack() #ngambil semua frame call stack
    call_frame = stack[-3]
    #-1, baris extract_stack di atas
    #-2 baris dimana fungsi extract_stack dipanggil
    #-3 baris fungsi yang manggil fungsi 2

    print(f'{WHITE} File "{PURPLE}{call_frame.filename}{WHITE}", {WHITE}line {PURPLE}{call_frame.lineno}{WHITE}, in {call_frame.name}{RESET}', file=sys.stderr)
    if call_frame.line:
        clean_line = call_frame.line.split('#')[0].rstrip() #hapus dari sebelah kanannya '#'
        print(f' {RED}{clean_line}{RESET}', file=sys.stderr)
    print(f'{PURPLE}{BOLD}ValueError{RESET}: {PURPLE}{msg}{RESET}', file=sys.stderr)

# Ambil character di OS Windows dan linux, ini dapat dari AI
try: #windows
    import msvcrt
    def inputchar()-> str:
        ch = msvcrt.getch()
        if ch in (b'\x00', b'\xe0'):
            ch2 = msvcrt.getch()
            if ch2 == b'H': return '\x1b[A' #panah atas
            if ch2 == b'P': return '\x1b[B' #panah bawah
            if ch2 == b'M': return '\x1b[C' #panah kanan
            if ch2 == b'K': return '\x1b[D' #panah kiri
            return ''
        char_str = ch.decode('utf-8', errors='ignore')
        if char_str == '\x08': return '\x7f'
        return char_str
except ImportError: #jika bukan windows akan error import msvcrt, berarti linux
    import tty
    import termios
    def inputchar()->str:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            if ch == '\x1b': ch += sys.stdin.read(2)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

# Saat seumpama dicompile, hapus salah satu fungsi, sisakan yang dibutuhkan
# kalau compile di windown, sisakan msvcrt saja
# kalau linux sisakan tty dan termios saja
# hapus try except nya
#===================
# logika utama
memory = [] #manipulasi memori

def readline(prompt="", input_val="", end_line="", type="string")->str:
    # endline untuk satuan di akhir input, tipe untuk validasi
    valid_type = ["string", "integer", "float"]
    if type not in valid_type:
        custerror(f"Invalid data type '{type}'. Choose one of: {valid_type}")
        return

    # saat seumpama dicompile, hapus if di atas dan custom error

    cursor_position = len(input_val) #taruh cursor di akhir input val

    # cetak nilai sekali di awal
    sys.stdout.write(prompt + input_val + end_line)
    if len(end_line) > 0:
        sys.stdout.write("\b" * len(end_line)) #mundurin cursor ke tepat sebelum endline
    sys.stdout.flush() #kayak gini itu paksa cetak sekarang.

    memocount = len(memory)
    temp_memo = ""

    while True: #perulangan yang dipanggil setiap input dipencet, dan berhenti ketika enter
        char = inputchar() #ambil char
        
        if char in ['\r', '\n']: #jika char adalah enter
            if cursor_position < len(input_val): #jika cursor ditengah teks,
                #dorong kursor ke ujung teks
                sys.stdout.write(input_val[cursor_position:] + end_line)
            sys.stdout.write("\n")
            sys.stdout.flush()
            try :memo = memory[-1] #jika memori sudah terisi, memo = memory paling belakang
            except IndexError : memo = "" #jika memori belum terisi, memo kosong
            #jika input tidak kosong atau sama seperti memlry sebelumnya
            # maka tambahkan input val ke memory paling belakang
            if input_val.strip() not in ["",memo]: memory.append(input_val)
            return input_val
        
        # Backspace
        elif char == '\x7f':
            if cursor_position > 0: #jika cursor tidak di ujung paling awal/kiri
                input_val = input_val[:cursor_position-1] + input_val[cursor_position:]
                cursor_position -= 1 #cursor mundur 1
                sisa_kanan = input_val[cursor_position:] + end_line
                
                sys.stdout.write("\b\x1b[P")
                if len(sisa_kanan) > 0:
                    sys.stdout.write(sisa_kanan + "\b" * len(sisa_kanan))
                    # mundur sebanyak sisa kanan jika ada
                sys.stdout.flush()

        elif char == '\x1b[A': #panah atas
            if memocount > 0: #jika ada memory di atas nya
                if memocount == len(memory): # jika belum klik panah atas
                    temp_memo = input_val # masukan input ke memo sementara
                memocount -= 1 #mundur ke memo sebelumnya
                
                if cursor_position > 0: # taruh cursor di awal, mundurkan sampai belakang
                    sys.stdout.write("\b" * cursor_position)
                
                panjang_lama = len(input_val) + len(end_line)
                #cetak spasi kosong lalu mundurkan kembali
                sys.stdout.write(" " * panjang_lama + "\b" * panjang_lama)
                
                input_val = memory[memocount] #ambil memori
                cursor_position = len(input_val) #cursor taruh ujung
                
                sys.stdout.write(input_val + end_line) 
                if len(end_line) > 0: sys.stdout.write("\b" * len(end_line))
                sys.stdout.flush()

        elif char == '\x1b[B': #panah bawah
            if memocount < len(memory): #jika ada memori di bawahnya
                memocount += 1 # maju ke memo selanjutnya
                
                if cursor_position > 0: #sama kayak fungsi panah atas
                    sys.stdout.write("\b" * cursor_position)
                
                panjang_lama = len(input_val) + len(end_line)
                sys.stdout.write(" " * panjang_lama + "\b" * panjang_lama)
                
                if memocount == len(memory): 
                    input_val = temp_memo
                else: 
                    input_val = memory[memocount]
                    
                cursor_position = len(input_val)
                sys.stdout.write(input_val + end_line)
                if len(end_line) > 0: sys.stdout.write("\b" * len(end_line))
                sys.stdout.flush()
            
        elif char == '\x1b[C': # kursor ke kanan
            if cursor_position < len(input_val):
                sys.stdout.write(input_val[cursor_position])
                cursor_position += 1
                sys.stdout.flush()

        elif char == '\x1b[D': #kursor ke kiri
            if cursor_position > 0:
                cursor_position -= 1
                sys.stdout.write("\b")
                sys.stdout.flush()

        elif char == "-" and not input_val: 
            #jika tidak mengandung -, dan input belum terisi, selalu bisa diisi '-'
            input_val = "-"
            cursor_position = 1
            sys.stdout.write(char + end_line)
            if end_line:
                sys.stdout.write("\b" * len(end_line))                                          
            sys.stdout.flush()

        elif char.isprintable(): #jika karakter printable
            inputable = False
            if type == "integer": #bilangan bulat
                if char.isdigit(): inputable = True
            elif type == "float": #bilangan koma, bisa '.' satu kali
                if char.isdigit() or (char == "." and "." not in input_val): inputable = True
            else: #bisa semua, string bebas
                inputable = True   
                
            if inputable: #jika bisa tambahkan setelah cursor position
                sisa_kanan = input_val[cursor_position:] + end_line
                input_val = input_val[:cursor_position] + char + input_val[cursor_position:]
                cursor_position += 1
                
                sys.stdout.write(char + sisa_kanan)
                if len(sisa_kanan) > 0:
                    sys.stdout.write("\b" * len(sisa_kanan))
                sys.stdout.flush()

        elif char in ['\x1b[H', '\x01']: #home, mundur ke awal
            if cursor_position > 0:
                sys.stdout.write("\b" * cursor_position)
                cursor_position = 0
                sys.stdout.flush()

        elif char in ['\x1b[F', '\x05']: #end maju paling akhir
            if cursor_position < len(input_val):
                sisa_teks = input_val[cursor_position:]
                sys.stdout.write(sisa_teks)
                cursor_position = len(input_val)
                sys.stdout.flush()

        # khusus, Ctrl C, D, L
        elif char == '\x03':
            sys.stdout.write("^C\n")
            return "^\u200bC"
        elif char == '\x04':
            sys.stdout.write("^D\n")
            return "^\u200bD"
        elif char == '\x0c':
            sys.stdout.write("^L\n")
            return "^\u200bL"






#==========================================
# from pyread import readline
import os, traceback, re

if not os.path.isdir(".tools"):
    #menyiapkan folder terisolasi
    os.system("mkdir .tools && cd .tools")
else : os.system("cd .tools")
    
dir_cd = ".tools/" #directori
dircdx = "tools/"
len_dir = 2
dir_cdx = dircdx

lang_map={"c":{"pkg":"clang", "cmd":"clang"},
          "cpp":{"pkg":"clang", "cmd":"clang++"},
          "cs":{"pkg":"mono", "cmd":"mcs"},
          "js":{"pkg":"nodejs", "cmd":"node"},
          "ts":{"pkg":"nodejs", "cmd":"node"},
          "vb":{"pkg":"mono", "cmd":"vbc"},
          "lua":{"pkg":"lua", "cmd":"lua"},
          "rs":{"pkg":"rust", "cmd":"rustc"},
          "go":{"pkg":"golang", "cmd":"go"},
          "py":{"pkg":"python", "cmd":"python"},
          "php":{"pkg":"php", "cmd":"php"},
          "asm":{"pkg":"nasm", "cmd":"nasm"}
          }
def run(namafile):
    #untuk mendefinisikan perintah run
    if namafile == "run":
        print("run <file>")
        return #jika cuma ngetik run doang
    elif not os.path.isfile(f"{dir_cd}{namafile}"):
        print("File tidak ditemukan")
        return #jika file tidak ditemukan

    # memecah nama file dan existensi
    nama = ".".join(namafile.split(".")[:-1])
    existensi = namafile.split(".")[-1]
    compile_ext = ["c","cpp","rs","go"] #dicompile
    mono_ext = ["cs", "vb"] #jadi exe
    try:cmd = lang_map[existensi]["cmd"]
    except KeyError:
        if existensi not in ["html", "sh"]:
            print(f"Format file tidak diketahui.")
            return
    if (existensi in ["html","sh"] or
        os.system(f"command -v {cmd} > /dev/null 2>&1") == 0):
        if existensi in compile_ext:
            compile_f(namafile, nama, existensi)
        elif existensi in mono_ext:
            mono_f(namafile, nama, existensi)
        elif existensi == "html":#untuk html jalankan ke localhost port 8080
            if os.system(f"command -v python > /dev/null 2>&1") == 0:
                filename = namafile
                if namafile == "index.html" : filename = ""
                os.system(f"cd ./{dir_cd} && python -m http.server 8080 & termux-open http://localhost:8080/{filename}")
            else :
                print("Kok bisa, belum install python,",end=" ")
                print("Install python dulu.")
                print("Ketik lang py")
        elif existensi == "asm":
            compile_f(namafile, nama, existensi) #jadiin file objek.o
            if (os.system(f"command -v clang > /dev/null 2>&1")
                == 0): # clang untuk dari o ke bisa dijalankan
                compile_f(nama+".o", nama, "o")
            else :
                print("Install clang dulu")
                print("Ketik lang c")
            os.system(f" cd ~/ && rm {nama}.o") #selalu hapus .o

        else:
            run_f(namafile, existensi) #interpreter
    else:
        print(f"Bahasa '{existensi}' tidak terinstall")
        print(f"Ketik 'lang {cmd}' untuk install.")

def compile_f(namafile, nama, existensi):
    x = "cd ~/ && " # pergi ke folder home
    #Copy file ke home, compile, jalankan, hapus
    compiler = "" 
    namaoutput = ""
    if existensi == "rs": compiler = "rustc"
    elif existensi == "go": compiler = "go build"
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
    else : 
        y = existensi.replace("c","").replace("p","+")
        compiler = f"clang{y}"
        namaoutput = f" -lm -o {nama}"    
    os.system(f"cp {dir_cd}{namafile} ~/")
    os.system(f"{x}{compiler} {namafile}{namaoutput}")
    os.system(f"{x}./{nama}")
    os.system(f"{x}rm {namafile} && rm {nama}")

def mono_f(namafile, nama, existensi):
    if existensi=="cs": run = "mcs" # c sharp
    elif existensi == "vb" : run = "mono /data/data/com.termux/files/usr/lib/mono/4.5/vbc.exe /sdkpath:/data/data/com.termux/files/usr/lib/mono/4.8-api/ /reference:/data/data/com.termux/files/usr/lib/mono/4.8-api/Microsoft.VisualBasic.dll /nologo" # vb net
    os.system(f'cd  {dir_cd} && {run} {namafile}') #jadikan exe
    os.system(f'mono {dir_cd}{nama}.exe') #jalankan
    os.system(f"rm {dir_cd}{nama}.exe") #hapus

def run_f(namafile, existensi): #interpreter
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

def lang(language): # install bahasa
    language = language.lower()
    if language == "lang": #jika ngetik lang doang
        print("lang <language>")
        return
    inisial = {"a":["asm"],
               "c":["c","cpp","cs"],
               "j":["js"],
               "p":["py","php"],
               "t":["ts"],
               "l":["lua"],
               "r":["rs"],
               "g":["go"],
               "v":["vb"]
               } #untuk koreksi
    try:
        pkg = lang_map[language]["pkg"]
        cmd = lang_map[language]["cmd"]
    except KeyError:
        print(f"Bahasa pemograman {language} tidak ditemukan.")
        # koreksi
        try:
            auto = inisial[language[0]]
            print("Mungkin maksud anda :")
            for i in range(len(auto)):
                print("Bahasa", auto[i])
            print()
        except KeyError: print()
        return
    #ngecek apakah bahasa / compiler sudah terinstal
    if os.system(f"command -v {cmd} > /dev/null 2>&1") == 0:
        os.system(f"{cmd} --version")#ngasih tau versi
    else :
        print("Bahasa tidak tersedia.")
        print("Apakah anda ingin menginstallnya?",end="")
        pilihan = input("(y/n) :")
        if (pilihan+" ")[0].lower() == "y":
            os.system(f"pkg install {pkg}") 
            #install bahasa atau compiler
        else :
            return
def cd(folder): #pindah direktori
    global dir_cd, dir_1,dircdx,len_dir
    if folder in ["cd",""]:
        print("cd <dir>")
        return #jika cuma ngetik cd doang
    elif not os.path.isdir(f"{dir_cd}{folder}"):
        print("Folder tidak ditemukan")                   
        return
    if folder == "..": #jika akses selain folder file ini
        if len_dir <= 2:
            print("Akses ditolak")
        else :
            #hapus direktori paling terakhir
            dir_cd = (("\u200b"+
                       "/".join(dir_cd.split("/")[:-2])+
                       "/")
                      .replace("\u200b/","")
                      .replace("\u200b",""))
    elif folder == ".": pass
    else :
        dir_cd = f"{dir_cd}{folder}/"
    dircdx = ((f"tools/{dir_cd
              .replace(".tools/","")}")
             .split("../")[-1])
    len_dir = len(dircdx.split("/"))
    if len_dir > 3: dircdx = (".../"+
                              "/".join(dircdx
                                .split("/")
                                 [-3:-1])+
                              "/")


while True:
    menu = readline(f"\x1b[32m~/{dircdx}\x1b[0m $ ").strip()
    params = menu.split(" ")[-1]
    if "/alat.py" in params: #nyoba akses file ini
        #seperti nano, rm, run, nvim, dll
        print("Anda tidak memiliki akses")
        continue
    perintah = menu.split(" ")[0].strip()
    if perintah == "run" : run(params)
    elif perintah == "help": info()
    elif perintah == "lang" : lang(params)
    elif perintah in ["end","^\u200bC"] : os.system('pkill -9 -f "http.server"') #hentikan localhost
    elif perintah == "cd" : cd(params)
    elif perintah in ["exit","^\u200bD"] : 
        os.system('pkill -9 -f "http.server"')
        break
    elif perintah in ["clear","^\u200bL"] :os.system('clear')
    else: os.system(f"cd ./{dir_cd} && {menu}")#jika tidak ada, pake default
