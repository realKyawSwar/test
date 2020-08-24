
# convert hexstring to signed decimal
def decodeOut(hexstr, bits):
    value = int(hexstr, 16)
    if value & (1 << (bits-1)):
        value -= 1 << bits
    return(value)


def speedClean(B_array):
    firstPart = B_array[:-7]
    midPart = str(firstPart[6:])
    # print(type(midPart))
    if midPart[0] == '1':
        midPart = "0" + midPart[1:]
        speed_result = decodeOut(midPart, 16)
        # speed_result = 2**16 - decodeOut(midPart, 16)
    else:
        speed_result = decodeOut(midPart, 16)
    return speed_result


def torqueClean(B_array):
    firstPart = B_array[:-3]
    midPart = str(firstPart[11:])
    torque_result = decodeOut(midPart, 16)/10
    return torque_result


B_array = [bytearray(b'\x020A0001FFEFFFD2\x034E'),
           bytearray(b'.0A0000FB5AFFF1.35'),
           bytearray(b'.0A0000FB59FFEB.3D'),
           bytearray(b'.0A0000FB58FFE1.2B'),
           bytearray(b'.0A0000FB61FFD9.2C'),
           bytearray(b'.0A0000FB55FFDE.3B'),
           bytearray(b'.0A0000FB55FFDE.3B'),
           bytearray(b'.0A0000FB50FFD5.26'),
           bytearray(b'.0A0000FB51FFD4.26'),
           bytearray(b'.0A0000FB52FFD5.28'),
           bytearray(b'.0A0000FB4EFFD9.3E'),
           bytearray(b'.0A0000FB4DFFD9.3D'),
           bytearray(b'.0A0000FB45FFD8.2D'),
           bytearray(b'.0A0000FB49FFDB.3B'),
           bytearray(b'.0A0000FB48FFDE.3D'),
           bytearray(b'.0A0000FB3EFFEC.48'),
           bytearray(b'.0A0000FB44FFF3.29'),
           bytearray(b'.0A0000FB46FFF4.2C'),
           bytearray(b'.0A0001FFF50005.01'),
           bytearray(b'.0A0001FFF9FFFF.58'),
           bytearray(b'.0A0001FFFCFFF9.55'),
           bytearray(b'.0A0001FFFDFFF5.52')]


for i in B_array:
    a = torqueClean(i.decode())
    b = speedClean(i.decode())
    # print(a)
    print(b)

# print(decodeOut(bytearray(b'1869F'),32)/10)
