

def BallotCount():
    # Program to read all the lines in a file using readline() function
    file = open("python.txt", "r")
    while True:
        content=file.readline()
        if not content:
            break
        print(content)
    file.close()


if __name__ == "__main__":
    BallotCount()

