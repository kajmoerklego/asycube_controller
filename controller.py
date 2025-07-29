import json
import socket
import time
from typing import Optional


class Asycube:
    def __init__(self, ip: str = "192.168.127.254", port: int = 4001) -> None:
        """
        Initialize the Asycube240 controller.

        :param ip: The IP address of the Asycube (default is '192.168.127.254').
        :param port: The port for TCP/IP communication (default is 4001).
        """
        self.ip = ip
        self.port = port
        self.sock: Optional[socket.socket] = None

    def connect(self) -> None:
        """Establish a TCP connection to the Asycube."""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ip, self.port))
        print(f"Connected to Asycube at {self.ip}:{self.port}")

    def disconnect(self) -> None:
        """Close the TCP connection."""
        if self.sock:
            self.sock.close()
            print("Disconnected from Asycube")

    def send_command(self, command: str) -> Optional[str]:
        """
        Send a command to the Asycube and return the response.

        :param command: The command to send to the Asycube.
        :return: The response from the Asycube, or None if an error occurs.
        """
        try:
            # Construct the command packet
            packet = f"{{{command}}}\r\n"
            print(f"Sending: {packet}")
            self.sock.sendall(packet.encode("utf-8"))
            time.sleep(0.1)  # Wait for the command to be processed
            response = self.sock.recv(1024).decode("utf-8")
            return response
        except Exception as e:
            print(f"Error sending command: {e}")
            return None

    def vibrate_from_json(self, json_data: dict) -> None:
        """
        Vibrate actuators based on JSON data.

        :param json_data: A dictionary containing actuator IDs and their parameters.

        .. code-block:: json

            {
                "B": {
                    "1": {
                        "amplitude": 50,
                        "frequency": 100,
                        "phase": 0,
                        "waveform": "1"
                    },
                    "2": {
                        "amplitude": 75,
                        "frequency": 150,
                        "phase": 0,
                        "waveform": "1"
                    },
                    "duration": 1200
                }
            }
        """
        json_data = json.loads(json.dumps(json_data))
        for vibration_id in json_data:
            cmd_base = f"SC{vibration_id}="
            cmd_actuators = ["0;0;0;0;"] * 4
            for actuator_id, params in json_data[vibration_id].items():
                if actuator_id != "duration":
                    print(params)
                    amplitude = params.get("amplitude", 0)
                    frequency = params.get("frequency", 0)
                    phase = params.get("phase", 0)
                    waveform = params.get("waveform", 1)
                    if int(actuator_id) - 1 == 3:
                        cmd_actuators[int(actuator_id) - 1] = f"{amplitude};{frequency};{phase};{waveform};"
                    cmd_actuators[int(actuator_id) - 1] = f"{amplitude};{frequency};{phase};{waveform};"
            duration = json_data[vibration_id].get("duration", 1000)
            cmd_out = (
                cmd_base + f"({cmd_actuators[0]}{cmd_actuators[1]}{cmd_actuators[2]}{cmd_actuators[3]}{duration})"
            )
            # cmd_out = "{"+cmd_out+"}"
        response = self.send_command(cmd_out)

        print(f"Vibrating actuators from JSON: {cmd_out}: Respone {response}")
        response = self.send_command(f"C{vibration_id}")

    def set_amplitude(self, actuator_id: int, amplitude: int) -> None:
        """
        Set the amplitude for a specific actuator.

        :param actuator_id: The ID of the actuator (1-26).
        :param amplitude: The amplitude to set (0-100).
        """
        command = f"WP{actuator_id * 100 + 1}={amplitude}"  # Example address calculation
        response = self.send_command(command)
        print(f"Setting amplitude for actuator {actuator_id}: {response}")

    def set_frequency(self, actuator_id: int, frequency: int) -> None:
        """
        Set the frequency for a specific actuator.

        :param actuator_id: The ID of the actuator (1-26).
        :param frequency: The frequency to set (Hz).
        """
        command = f"WP{actuator_id * 100 + 2}={frequency}"  # Example address calculation
        response = self.send_command(command)
        print(f"Setting frequency for actuator {actuator_id}: {response}")


# Example usage:
if __name__ == "__main__":
    asycube = Asycube()
    asycube.connect()
    json_cmd = {
        "B": {
            "1": {
                "amplitude": 60,
                "frequency": 150,
                "phase": 0,
                "waveform": "1",
            },
            "2": {
                "amplitude": 60,
                "frequency": 150,
                "phase": 0,
                "waveform": "1",
            },
            "3": {
                "amplitude": 0,
                "frequency": 150,
                "phase": 0,
                "waveform": "1",
            },
            "4": {
                "amplitude": 0,
                "frequency": 150,
                "phase": 0,
                "waveform": "1",
            },
            "duration": 1000,
        },
    }
    asycube.vibrate_from_json(json_cmd)
    asycube.disconnect()
