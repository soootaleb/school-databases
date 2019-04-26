import os
PRINT = True


def get_path():
    path = os.path.join(os.getcwd(), "data", "twitter")
    if PRINT:
        print(path)
    return path
def main():
    path = get_path()

    users = dict()
    actual_id = -1
    for root, directory, files in os.walk(path):
        for actual_file in files:
            actual = actual_file.split('.')
            actual_id = actual[0]
            type_of_actual = actual[1]
            
            if PRINT:
                print("actual_file", actual_id, type_of_actual)
            try :
                users[actual_id].append(type_of_actual = dict)
            except:
                users[actual_id] = dict()
                users[actual_id].append(type_of_actual)


    print(users)
if __name__ == "__main__":
    main()
