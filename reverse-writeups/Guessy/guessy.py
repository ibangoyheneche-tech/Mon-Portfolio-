print("FLAG")
print("FCSC{")
print("e7552cf6")

hex1 = "0x34 0x63 0x65 0x32 0x65 0x35 0x61 0x64"
res1 = ""
for h in hex1.split():
    nombre = int(h, 16)
    caractere = chr(nombre)
    res1 += caractere
print(res1)

hex2 ="0x30 0x62 0x62 0x30 0x39 0x35 0x34 0x66"
res2 = ""
for h in hex2.split():
    nombre = int(h,16)
    caractere = chr(nombre)
    res2 += caractere
print(res2)

hex3 = "0x1 0x54 0x55 0x51 0x9 0x7 0x57"
res3 = ""
for h, i in zip(hex3.split(), hex2.split()):
        nombre = int(h,16) ^ int(i,16)
        caractere = chr(nombre)
        res3 += caractere

# dernier caractére
res3 += "f"
print(res3)
print("}")
