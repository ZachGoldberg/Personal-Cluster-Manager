import sys

if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        sys.stderr.write("Usage: %s command commandargs\n" % args[0])
        sys.exit(1)

    command = args[1]
    try:
        module = __import__("commands.%s" % command,
                            globals(), locals(), 
                            command)
    except:
        sys.stderr.write("Invalid command: %s\n" % command)
        sys.exit(1)

    module.__dict__[command](args[2:])
