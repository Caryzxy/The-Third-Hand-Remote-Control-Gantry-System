import serial


class Gcode:
    def __init__(self) -> None:
        self.ser = serial.Serial('COM3', 115200)

        # Set current limit to 2000mA
        self.command("M906X2000Y2000Z2000\r\n")
        self.pos = [0, 0, 0]

    def command(self, command):
        self.ser.write(str.encode(command))
        while True:
            line = self.ser.readline()
            # wait for ack
            if line == b'ok\n':
                break

    def move_x(self, cmd):
        # set to relative position mode
        self.command("G91\r\n")
        # G1: move, F3200: set speed
        self.command("G1 X" + str(int(cmd)) + " F3200\r\n")
        print("MOVE X: ", cmd)
        self.pos[0] += int(cmd)

    def move_y(self, cmd):
        # set to relative position mode
        self.command("G91\r\n")
        # G1: move, F3200: set speed
        self.command("G1 Y" + str(int(cmd)) + " F3200\r\n")
        print("MOVE Y: ", cmd)
        self.pos[1] += int(cmd)

    def move_z(self, cmd):
        # set to relative position mode
        self.command("G91\r\n")
        # G1: move, F3200: set speed1
        self.command("G1 Z" + str(int(cmd)) + " F3200\r\n")
        print("MOVE Z ", cmd)
        self.pos[2] += int(cmd)

    def move_xyz(self, cmd: tuple[int, int, int]):
        # set to relative position mode
        self.command("G91\r\n")
        self.command(
            "G1 X" + str(int(cmd[0])) +
            "G1 Y" + str(int(cmd[1])) +
            "G1 Z" + str(int(cmd[2])) +
            " F3200\r\n")

        print("MOVE XYZ", cmd)
        self.pos[0] += int(cmd[0])
        self.pos[1] += int(cmd[1])
        self.pos[2] += int(cmd[2])

    def move_xyz_abs(self, cmd: tuple[int, int, int]):
        # set to relative position mode
        self.command("G91\r\n")
        self.command(
            "G1 X" + str(int(cmd[0] - self.pos[0])) +
            "G1 Y" + str(int(cmd[1] - self.pos[1])) +
            "G1 Z" + str(int(cmd[2] - self.pos[2])) +
            " F3200\r\n")

        print("MOVE XYZ ABS", cmd)
        self.pos[0] = int(cmd[0])
        self.pos[1] = int(cmd[1])
        self.pos[2] = int(cmd[2])



if __name__=="__main__":
    gcode_sender = Gcode()
    gcode_sender.move_xyz_abs((100, 100, 10))
    gcode_sender.move_xyz_abs((0, 0, 0))
    gcode_sender.move_xyz_abs((100, 100, 10))