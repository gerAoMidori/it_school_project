import os 

class WriteData:
    def __init__(self, path):
        self.path = path


    def write_data(self, data):
        with open(self.path, 'r', encoding='utf-8') as f:
            existing_data = f.read()
        print(existing_data)
        with open(self.path, 'w', encoding='utf-8') as f:
            f.write(existing_data + "\n" + data)

if __name__ == "__main__":
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(base_dir + "\myapp" )
        write_data = WriteData(path + "\\templates\correct.txt")
        write_data.write_data("This is a")
        print("Data written successfully.")