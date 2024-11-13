import serial
import threading
import time

#This class is the serial reading system that once initiated, will continously record the most recent
#average reading of the sensors and get ready to be access by other systems
class RealTimeAverageReader:
    def __init__(self, port='COM3', baudrate=9600):
        """
        Initialize the real-time average reader.
        
        Args:
            port (str): Serial port of the ESP32.
            baudrate (int): Baud rate for the serial connection.
        """
        self.serial_port = serial.Serial(port, baudrate)
        time.sleep(2)  # Give time for the serial connection to establish
        self.latest_reading = None
        self.latest_weight_kg = None
        self.running = True

        # Start the background thread
        self.thread = threading.Thread(target=self._read_serial)
        self.thread.start()

    def _read_serial(self):
        """Continuously read from the serial port and update the latest reading."""
        while self.running:
            if self.serial_port.in_waiting > 0:
                # Read a line from the serial port and handle decoding errors
                line = self.serial_port.readline().decode('utf-8', errors='ignore').strip()

                # Check if the line contains "Average Reading"
                if line.startswith("Average Reading:"):
                    try:
                        # Extract the value
                        average_reading = int(line.split(":")[1].strip())

                        # Convert the reading to kg
                        weight_kg = (4095 - average_reading) * (2 / 4095)

                        # Update the latest reading and weight
                        self.latest_reading = average_reading
                        self.latest_weight_kg = weight_kg
                    except ValueError:
                        print("Error parsing the average reading value.")

    def get_latest_reading(self):
        """
        Returns the most recent average reading and its equivalent in kg.
        
        Returns:
            tuple: The latest average reading value and calculated weight in kg.
        """
        return self.latest_reading, self.latest_weight_kg

    def stop(self):
        """Stops the background thread and closes the serial connection."""
        self.running = False
        self.thread.join()
        self.serial_port.close()

# Example usage

#initate the serial readtime reader system
reader = RealTimeAverageReader(port='COM3', baudrate=9600)

# In a real application, you would call this repeatedly or at specific intervals
time.sleep(5)  # Wait a bit to allow some readings to accumulate

#After initiated, call .get_latest_reading to get the lastest average reading from the sensor
latest_reading, latest_weight_kg = reader.get_latest_reading()
print(f"Latest Average Reading: {latest_reading} | Approximate Weight: {latest_weight_kg:.3f} kg")


# Stop the reader when done, this will kil the serial process, only call it when everything was done.
reader.stop()
