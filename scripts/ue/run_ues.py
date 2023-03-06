import sys
import os
import subprocess
import time
import concurrent.futures
from multiprocessing import Process


def send_ue_files(num_ues):
    for i in range(1, num_ues + 1):
        if ( not os.path.isfile(f'files/mobility_file_ue{i}')):
            print(f'files/mobility_file_ue{i} does not exist, skipping')
            continue

        command = f'kubectl cp files/mobility_file_ue{i} ue{i}:/openairinterface5g/cmake_targets/ran_build/build/'
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


def get_ue_params(num_ues):
    params = []
    for i in range(1, num_ues + 1):
        if (not os.path.isfile(f'mobility_file_ue{i}')):
            print(f'mobility_file_ue{i} does not exist, skipping')
            continue
        source = '0'
        target = '0'
        with open(f'mobility_file_ue{i}', 'r') as f:
            source = f.readline().strip().split(',')[0]
            target = f.readline().strip().split(',')[0]
            if not target:
                target = '0'
            
            params.append((source, target))
    return params

def run_ues(num_enbs, ue_params):
    for i, (source, target) in enumerate(ue_params):
        command = f'kubectl exec ue{i + 1} -- /openairinterface5g/cmake_targets/ran_build/build/oai_ue.sh {i + 1} {num_enbs} {source}'
        print(command)
        # try:
        #     process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #     output, error = process.communicate()
        #     if process.returncode != 0:
        #         print(f'Error executing command: {command}\n{error.decode()}')
        #         pass
        #     else:
        #         print(f'Success executing command: {command}\n{output.decode()}')
        #         pass
        # except Exception as e:
        #     pass
        #     print(f'Error executing command: {command}\n{e}')
        # pass
    pass

def execute_traffic_commands(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
        command_lists = []
        for line in lines:
            ue_commands = []
            [ue, *sessions] = line.strip().split('|')
            id = int(ue.strip('UE'))
            for session in sessions:
                command, time_seconds = session.strip().split(',')
                time_seconds = int(time_seconds)
                #print(f'ID: {id}, Command: {command}, Time: {time_seconds}')
                ue_commands.append([id, time_seconds, command])
            command_lists.append(ue_commands)
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for commands in command_lists:
                futures.append(executor.submit(execute_commands, commands))

            # for future in concurrent.futures.as_completed(futures):
            #     result = future.result()
            #     if result is not None:
            #         print(result)
        print('Traffic commands finished')


def execute_commands(commands):
    tmp = 0
    start_time = time.time()
    done = False
    index = 0
    while (index < len(commands)):
        current_time = time.time()
        id, delay, command = commands[index]
        if (start_time + delay > current_time):
            continue
        else:
            #print(current_time - start_time)
            try:
                process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if (index + 1 < len(commands)):
                    max_duration = commands[index + 1][1] - delay
                    #print(f'Timeout is: {max_duration - 1}s')
                    output, error = process.communicate(timeout=max_duration)
                else:
                    pass
                    output, error = process.communicate(timeout=30)
                if process.returncode != 0:
                    #print(f'Error executing command: {command}\n{error.decode()}')
                    pass
                else:
                    #print(f'Success executing command: {command}\n{output.decode()}')
                    pass
            except Exception as e:
                pass
                #print(f'Error executing command: {command}\n{e}')
            index += 1

def main():
    if (len(sys.argv) != 3):
        print('Wrong number of arguments')
        exit()

    num_ues = int(sys.argv[1])
    num_enbs = int(sys.argv[2])

    print('Copying mobility files to UE pods...')
    #send_ue_files(num_ues)

    # Run
    ue_params = get_ue_params(num_ues)
    ues_process = Process(target=lambda: run_ues(num_enbs, ue_params))
    ues_process.start()
    print('Ue run thread is running...')

    # Traffic
    traffic_process = Process(target=lambda: execute_traffic_commands('files/traffic_scenario.txt'))
    traffic_process.start()
    print('Traffic thread is running...')

if __name__ == "__main__":
    main()
