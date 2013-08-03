import lightwaverf

# TODO(3) Have list of devices loaded from a repository
devices = lightwaverf.LightwaveDeviceList()
devices.append('foyer', 1, 'light', 1)
devices.append('bedroom', 2, 'fan', 1)

while True:
    command = ''
    input = raw_input('Enter your command: ')

    # TODO(3) Break out into a command parser
    tokens = input.split()
    if len(tokens) > 0:             # we have a command to execute
        command = tokens[0]         # the command is always the first token
        args = tokens[1:]           # args are everything else

    # TODO(3) command factory required 
    if command == 'exit':
        break
    elif command == 'plug':         # we are going to execute a plug based command
        # TODO(3) push validation into commands e.g. if command.is_valid() : command.execute() else: print command.validation_failure_reason()
        # TODO(2) Create argument shortcuts common execution e.g. [plug flon] translates to [plug foyer light on]  
        if len(args) == 3:
            device = devices.find(args[0], args[1])
            if device == None:
                print 'No matching device'
            else:
                mediator = lightwaverf.LightwaveMediator()   
                mediator.execute_plug(device.room_number, device.device_number, args[2])
        else:
            print 'Fail. Usage: plug <room_name> <device_name> <on>'
    else:
        print 'Fail. Command not found'

        







