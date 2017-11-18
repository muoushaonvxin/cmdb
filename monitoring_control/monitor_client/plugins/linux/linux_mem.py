import subprocess

def monitor():
    try:
        mem_command = 'cat /proc/meminfo | grep -E -i "memtotal|memfree|buffers|cached|swapcached"'
        result = subprocess.Popen(mem_command,shell=True,stdout=subprocess.PIPE).stdout.readlines()
        value_dict = {'status': 0, 'data': {}}
        for line in result:
            line = line.decode().strip().split()
            memory_item, memory_size, memory_unit = line
            value_dict['data'][memory_item] = [memory_size, memory_unit]
    except Exception as e:
        value_dict = {'status': 250, 'data': {}}
        return value_dict
    return value_dict