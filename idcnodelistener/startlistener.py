from nodelistener import nodelistener

def main():
    try:
        nodelistener.main()
    except OSError:
        print("Listener was already running, or something else is using the port.")
