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
