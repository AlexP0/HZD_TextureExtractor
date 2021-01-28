import os
from struct import pack, unpack
from pathlib import Path
from tkinter import filedialog
import tkinter as tk

import sys

PixelFormat = {b'\x24':"INVALID",
               b'\x00':"RGBA_5551",
               b'\x01':"RGBA_5551_REV",
               b'\x02':"RGBA_4444",
               b'\x03':"RGBA_4444_REV",
               b'\x04':"RGB_888_32",
               b'\x05':"RGB_888_32_REV",
               b'\x06':"RGB_888",
               b'\x07':"RGB_888_REV",
               b'\x08':"RGB_565",
               b'\x09':"RGB_565_REV",
               b'\x0A':"RGB_555",
               b'\x0B':"RGB_555_REV",
               b'\x0C':"RGBA_8888",
               b'\x0D':"RGBA_8888_REV",
               b'\x0E':"RGBE_REV",
               b'\x0F':"RGBA_FLOAT_32",
               b'\x10':"RGB_FLOAT_32",
               b'\x11':"RG_FLOAT_32",
               b'\x12':"R_FLOAT_32",
               b'\x13':"RGBA_FLOAT_16",
               b'\x14':"RGB_FLOAT_16",
               b'\x15':"RG_FLOAT_16",
               b'\x16':"R_FLOAT_16",
               b'\x17':"RGBA_UNORM_32",
               b'\x18':"RG_UNORM_32",
               b'\x19':"R_UNORM_32",
               b'\x1A':"RGBA_UNORM_16",
               b'\x1B':"RG_UNORM_16",
               b'\x1C':"R_UNORM_16",
               b'\x1D':"RGBA_UNORM_8",
               b'\x1E':"RG_UNORM_8",
               b'\x1F':"R_UNORM_8",
               b'\x20':"RGBA_NORM_32",
               b'\x21':"RG_NORM_32",
               b'\x22':"R_NORM_32",
               b'\x23':"RGBA_NORM_16",
               b'\x24':"RG_NORM_16",
               b'\x25':"R_NORM_16",
               b'\x26':"RGBA_NORM_8",
               b'\x27':"RG_NORM_8",
               b'\x28':"R_NORM_8",
               b'\x29':"RGBA_UINT_32",
               b'\x2A':"RG_UINT_32",
               b'\x2B':"R_UINT_32",
               b'\x2C':"RGBA_UINT_16",
               b'\x2D':"RG_UINT_16",
               b'\x2E':"R_UINT_16",
               b'\x2F':"RGBA_UINT_8",
               b'\x30':"RG_UINT_8",
               b'\x31':"R_UINT_8",
               b'\x32':"RGBA_INT_32",
               b'\x33':"RG_INT_32",
               b'\x34':"R_INT_32",
               b'\x35':"RGBA_INT_16",
               b'\x36':"RG_INT_16",
               b'\x37':"R_INT_16",
               b'\x38':"RGBA_INT_8",
               b'\x39':"RG_INT_8",
               b'\x3A':"R_INT_8",
               b'\x3B':"RGB_FLOAT_11_11_10",
               b'\x3C':"RGBA_UNORM_10_10_10_2",
               b'\x3D':"RGB_UNORM_11_11_10",
               b'\x3E':"DEPTH_FLOAT_32_STENCIL_8",
               b'\x3F':"DEPTH_FLOAT_32_STENCIL_0",
               b'\x40':"DEPTH_24_STENCIL_8",
               b'\x41':"DEPTH_16_STENCIL_0",
               b'\x42':"BC1",
               b'\x43':"BC2 ",
               b'\x44':"BC3",
               b'\x45':"BC4U",
               b'\x46':"BC4S",
               b'\x47':"BC5U",
               b'\x48':"BC5S",
               b'\x49':"BC6U",
               b'\x4A':"BC6S",
               b'\x4B':"BC7"}
class ByteReader:
    @staticmethod
    def int8(f):
        b = f.read(1)
        i = unpack('<b', b)[0]
        return i
    @staticmethod
    def uint8(f):
        b = f.read(1)
        i = unpack('<B', b)[0]
        return i
    @staticmethod
    def int16(f):
        return unpack('<h', f.read(2))[0]

    @staticmethod
    def uint16(f):
        b = f.read(2)
        i = unpack('<H', b)[0]
        return i

    # @staticmethod
    # def float16(f):
    #     b = f.read(2)
    #     # print(b.hex())
    #     return float(np.frombuffer(b,dtype=np.float16)[0])

    @staticmethod
    def int32(f):
        b = f.read(4)
        i = unpack('<i',b)[0]
        return i
    @staticmethod
    def int64(f):
        b = f.read(8)
        i = unpack('<Q',b)[0]
        return i
    @staticmethod
    def string(f,length):
        b = f.read(length)
        return "".join(chr(x) for x in b)
    @staticmethod
    def float(f):
        b = f.read(4)
        fl = unpack('<f',b)[0]
        return fl
class BytePacker:
    @staticmethod
    def int8(v):
        return pack('<b', v)

    @staticmethod
    def uint8(v):
        return pack('<B', v)

    @staticmethod
    def int16(v):
        return pack('<h', v)

    @staticmethod
    def uint16(v):
        return pack('<H', v)

    # @staticmethod
    # def float16(v):
    #     f32 = np.float32(v)
    #     f16 = f32.astype(np.float16)
    #     b16 = f16.tobytes()
    #     return b16

    @staticmethod
    def int32(v):
        return pack('<i', v)

    @staticmethod
    def int64(v):
        return pack('<Q', v)

    @staticmethod
    def float(v):
        return pack('<f', v)

root = tk.Tk()
root.withdraw()

core = filedialog.askopenfilename(title = "Select Core", filetypes = [("Core",".core")])
core = Path(core)
coresize = os.path.getsize(core)
stream = core.with_suffix(".core.stream")
stream = Path(stream)
if not stream.exists():
    print("Stream not found, please locate .stream file")
    stream = filedialog.askopenfilename(title="Select Stream,", filetypes=[("Stream", ".stream")])
    stream = Path(stream)
streamsize = os.path.getsize(stream)
OutputDir = stream.parent

print(core)
print(stream)

Textures = []

class Texture:
    Name = ""
    Format = b''
    Offset = 0
    Size = 0
    Height = 0
    Width = 0

with open(core,'rb') as c:
    r = ByteReader()

    while c.tell() < coresize:
        ID = c.read(8)

        if ID == b'\x66\x38\x2B\x05\xB7\xAF\xE1\xF2':
            size = r.int32(c)
            blockOffset = c.tell()
            if size < 200:
                print("Single Color Texture")
                pass
            else:
                tex = Texture()
                c.seek(16,1)
                NameLength = r.int32(c)
                c.seek(4,1)
                tex.Name = r.string(c,NameLength) #Name
                c.seek(2,1)
                tex.Height = r.int16(c) #Height
                tex.Width = r.int16(c) #Width
                c.seek(3,1)
                tex.Format = c.read(1) #Format
                c.seek(38,1)
                PathLength = r.int32(c)
                c.seek(PathLength,1)
                tex.Offset = r.int64(c) #Offset
                tex.Size = r.int64(c) #Size
                Textures.append(tex)

            c.seek(blockOffset+size)
        else:
            size = r.int32(c)
            blockOffset = c.tell()
            c.seek(blockOffset + size)


for t in Textures:
    print(t.Name,t.Height,t.Width,t.Offset,t.Size,"  Format: ",PixelFormat[t.Format])

with open(stream,'rb') as s:
    for t in Textures:
        s.seek(t.Offset)
        texbuffer = s.read(t.Size)
        OutputFile = os.path.join(OutputDir, t.Name)
        with open(OutputFile,'wb') as w:
            w.write(texbuffer)
        print("Created file: ", OutputFile)

input()
