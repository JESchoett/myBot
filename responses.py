import random

listOfMsg = {
    'hello':'says "Hello there!"',
    'd6':'roll a d6',
    'd20':'roll a d20',
    'hello or $/?':'displays this msg',
}

def handle_response(message) -> str:
    msg = message.lower()

    if msg == 'help' or msg == '':
        return ("commandos available: " + str(listOfMsg) + "\n'$' to give the command in public\n'?' in privat chat")

    if msg == 'hello':
        return 'Hello there!'

    if msg == 'd6':
        return ("you rolled a: " + str(random.randint(1, 6)))

    if msg == 'd20':
        return ("you rolled a: " + str(random.randint(1, 20)))
