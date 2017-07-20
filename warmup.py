import mmap
from struct import pack, unpack


def write_data_to_binary_file(item_list, file_name):
    with open(file_name, "wb") as file_object:
        for item in item_list:
            file_object.write(
                pack("<i q", item, item**2))  




def get_memory_map_from_binary_file(file_name):
    num_bytes = (21 * 8 + 21 * 4)   

    with open(file_name, "r") as file_object:
        file_map = mmap.mmap(
            file_object.fileno(),
            length=num_bytes,
            access=mmap.ACCESS_READ)

    return num_bytes, file_map


def parse_memory_map(file_map):
    parsed_values = []

    for i in range(21):   
        parsed_values.append(
            unpack("<i q", file_map[i * 12: i * 12 + 12]))  

    return parsed_values




def warmup():
    item_list = range(1,42,2)   

    write_data_to_binary_file(item_list=item_list, file_name="out_warmup.bin")

    num_bytes, file_map = get_memory_map_from_binary_file("out_warmup.bin")

    with open("out_warmup_bytes.txt", "w") as file_object:
        file_object.write(str(num_bytes))

    parsed_values = parse_memory_map(file_map)

    for item in parsed_values:
        print item


if __name__ == "__main__":
    warmup()
