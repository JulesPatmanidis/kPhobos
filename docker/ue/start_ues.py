import sys
import os
import subprocess
import time
import concurrent.futures
from multiprocessing import Process

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
FILES_DIR = os.path.join(ROOT_DIR, 'files')

# def parse_mobility(ue_id):
#     handovers = []
#     filename = os.path.join(FILES_DIR, f'handover_table.csv')
#     print(os.path.isfile(filename))
#     if (not os.path.isfile(filename)):
#         print(f'{filename} does not exist, skipping')
#         return []
#     start = '0'
#     first_target = '0'
#     with open(filename, 'r') as f:
#         start = f.readline().strip().split(',')[0]
#         first_target = f.readline().strip().split(',')[0]
#         if not first_target:
#             first_target = '0'
        
#         handovers.append((start, first_target))
#     print(handovers)
#     return handovers

def fetch_files(ue_id):
    command = f'wget -cO - http://10.10.0.1:8000/mobility_file_ue{ue_id}.csv > handover_table.csv'
    print(command)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    command = f'wget http://10.10.0.1:8000/traffic_scenario.txt'
    print(command)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()


def run_ue(num_enbs, ue_id):
    
    command = f'/openairinterface5g/cmake_targets/ran_build/build/oai_ue.sh  {ue_id} {num_enbs} handover_table.csv'
    print(command)
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        if process.returncode != 0:
            print(f'Error executing command: {command}\n{error.decode()}')
            pass
        else:
            print(f'Success executing command: {command}\n{output.decode()}')
            pass
    except Exception as e:
        pass
        print(f'Error executing command: {command}\n{e}')
    pass
    


def parse_traffic_commands(ue_id):
    filename = os.path.join(ROOT_DIR, f'traffic_scenario.txt')
    with open(filename, 'r') as file:
        lines = file.readlines()
        commands = []
        for line in lines:
            [ue, *sessions] = line.strip().split('|')
            id = int(ue.strip('UE'))
            if id != ue_id:
                continue
            for session in sessions:
                command, time_seconds = session.strip().split(',')
                time_seconds = int(time_seconds)
                #print(f'ID: {id}, Command: {command}, Time: {time_seconds}')
                commands.append((command, time_seconds))
    return commands
        


def execute_traffic_commands(commands):
    start_time = time.time()
    index = 0
    kill_cmd = 'pkill -2 -f iperf'.split(' ') # Send SIGINT signal
    while (index < len(commands)):
        current_time = time.time()
        command, delay = commands[index]

        if (start_time + delay > current_time):
            continue
        else:
            #print(current_time - start_time)
            try:
                process = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if (index + 1 < len(commands)):
                    max_duration = commands[index + 1][1] - delay
                    print(f'Timeout is: {max_duration - 1}s')
                    time.sleep(max_duration - 1)
                    output, error = subprocess.Popen(kill_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                    o ,e = process.communicate()
                else:
                    pass
                    print(f'Last traffic command')
                    output, error = process.communicate()
                if process.returncode == 137: # SIGKILL code
                    print(f'Command killed successfully: {command}')
                    pass
                elif process.returncode != 0:
                    print(process.returncode)
                    print(f'Error executing command: {command}\n{error.decode()}')
                    pass
                else:
                    print(f'Success executing command: {command}\n{output.decode()}')
                    pass
            except Exception as e:
                pass
                print(f'Error executing command e: {command}\n{e}')
            index += 1


def is_interface_up(interface):
    for line in open('/proc/net/dev', 'r'):
        if interface in line:
            return True
    return False


def main():
    if (len(sys.argv) != 3):
        print('Use: python3 run_ues.py <ue_id> <num_enbs>')
        exit()

    ue_id = int(sys.argv[1])
    num_enbs = int(sys.argv[2])
    print(ue_id)
    #fetch_files(ue_id)

    # Run
    ue_process = Process(target=lambda: run_ue(num_enbs, ue_id))
    #ue_process.start()
    print('Ue run thread is running...')

    print('Waiting for oai interface to be set up...')
    while not is_interface_up('oaitun_ue1'):
        time.sleep(0.1)
    print('Done')
    # Traffic
    traffic_commands = parse_traffic_commands(ue_id)
    traffic_process = Process(target=lambda: execute_traffic_commands(traffic_commands))
    #traffic_process.start()
    print('Traffic thread is running...')


if __name__ == "__main__":
    main()