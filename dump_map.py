import sys


in_file = open(sys.argv[1], "rb")
in_bytes = in_file.read()
in_file.close()

out_file = open(sys.argv[1] + ".txt", "wb")

def write_utf8(f, s):
    f.write(s.encode('utf-8'))

def write_byte_span(f, b, start_offset, count):
    hex_str = "0123456789abcdef"
    for i in range(0, count):
        if i != 0:
            write_utf8(f, ' ')
        byte = b[start_offset + i]
        write_utf8(f, hex_str[byte >> 4])
        write_utf8(f, hex_str[byte & 0xf])
    write_utf8(f, '\n')

write_utf8(out_file, "Global header:\n")
write_byte_span(out_file, in_bytes, 0, 16)
write_utf8(out_file, "\n")

for area in range(0,96):
    for direction in range(0,8):
        catalog_offset = 16 + (area * 8 + direction) * 4
        data_offset = in_bytes[catalog_offset] + (in_bytes[catalog_offset + 1] << 8) + (in_bytes[catalog_offset + 2] << 16) + (in_bytes[catalog_offset + 3] << 24)

        if data_offset != 0:
            write_utf8(out_file, "Area " + str(area + 160) + " (" + hex(area + 160) + ") subarea " + str(direction) + ":\n")
            num_objects = in_bytes[data_offset] + (in_bytes[data_offset + 1] << 8)
            write_byte_span(out_file, in_bytes, data_offset, 16)
            for obj in range(0, num_objects):
                write_byte_span(out_file, in_bytes, data_offset + 16 + obj * 12, 12)
            write_utf8(out_file, '\n')

out_file.close()
