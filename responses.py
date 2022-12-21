import random

listOfMsg = {
    'hello':'says "Hello there!"',
    'd[num] [num of dice]':'roll a dice',
    'hello or $/?':'displays this msg',
}

def handle_response(message) -> str:
    msg = message.lower()

    if msg == 'help' or msg == '':
        return ("commandos available:\n" + str(listOfMsg) + "\n'$' to give the command in public\n'?' in privat chat")

    if msg == 'hello':
        return 'Hello there!'

    if msg[0:1] == 'd':
        rolling = []

        if ' ' in msg:
            rollFor = int(msg[msg.index(' ') + 1:])
            for _ in range (0,rollFor) :
                rolling.append("you rolled a:" + str(random.randint(1, int(msg[1:msg.index(' ')]))))
        else:
            rolling.append("you rolled a:\n" + str(random.randint(1, int(msg[1:]))))

        returnString = str(rolling).replace('[', '')
        returnString = returnString.replace(']', '')
        returnString = returnString.replace(',', '\n')
        returnString = returnString.replace("'", '')
        return returnString