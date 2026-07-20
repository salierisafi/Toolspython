import pyread #install pyread dulu juga

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
