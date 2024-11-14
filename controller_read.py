import serial
import time

# This class provides a real-time average reading system that, when called,
# parses the latest line for the current average reading.
class RealTimeAverageReader:
    def __init__(self, port='COM3', baudrate=115200):
        """
        Initialize the real-time average reader.
        
        Args:
            port (str): Serial port of the ESP32.
            baudrate (int): Baud rate for the serial connection.
        """
        self.serial_port = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)  # Give time for the serial connection to establish

    def get_latest_reading(self):
        """
        Reads the most recent line from the serial port and parses the average reading.
        
        Returns:
            tuple: The latest average reading value and calculated weight in kg,
                   or (None, None) if no valid reading is available.
        """
        # Flush any initial stale data from the buffer
        self.serial_port.reset_input_buffer()

        start_time = time.time()
        while time.time() - start_time < 2:  # Try for up to 2 seconds
            if self.serial_port.in_waiting > 0:
                line = self.serial_port.readline().decode('utf-8', errors='ignore').strip()

                # Check if the line contains "Current Average"
                if "Average Reading: " in line:
                    try:
                        # Extract the value after "Current Average:"
                        average_reading_str = line.split("Average Reading: ")[1].strip()
                        
                        # Convert extracted string to an integer
                        average_reading = int(average_reading_str)

                        # Convert the reading to kg
                        weight_kg = (4095 - average_reading) * (2 / 4095)

                        return average_reading, weight_kg
                    except (ValueError, IndexError) as e:
                        print(f"Error parsing the average reading value: {e}")
                        print(f"Debug: Could not parse '{average_reading_str}' as integer.")
            time.sleep(0.1)  # Short delay to avoid excessive looping
        return None, None

    def stop(self):
        """Closes the serial connection."""
        self.serial_port.close()

# Example usage

# Initiate the serial real-time reader system
reader = RealTimeAverageReader(port='COM3', baudrate=115200)

# Allow some time for initial readings
time.sleep(2)

# Call .get_latest_reading to get the latest average reading from the sensor
latest_reading, latest_weight_kg = reader.get_latest_reading()
if latest_reading is not None:
    print(f"Latest Average Reading: {latest_reading} | Approximate Weight: {latest_weight_kg:.3f} kg")
else:
    print("No data available yet.")

time.sleep(0.1)

# Call .get_latest_reading to get the latest average reading from the sensor
latest_reading, latest_weight_kg = reader.get_latest_reading()
if latest_reading is not None:
    print(f"Latest Average Reading: {latest_reading} | Approximate Weight: {latest_weight_kg:.3f} kg")
else:
    print("No data available yet.")

time.sleep(0.1)

# Call .get_latest_reading to get the latest average reading from the sensor
latest_reading, latest_weight_kg = reader.get_latest_reading()
if latest_reading is not None:
    print(f"Latest Average Reading: {latest_reading} | Approximate Weight: {latest_weight_kg:.3f} kg")
else:
    print("No data available yet.")

time.sleep(0.1)

# Call .get_latest_reading to get the latest average reading from the sensor
latest_reading, latest_weight_kg = reader.get_latest_reading()
if latest_reading is not None:
    print(f"Latest Average Reading: {latest_reading} | Approximate Weight: {latest_weight_kg:.3f} kg")
else:
    print("No data available yet.")


time.sleep(0.1)

# Call .get_latest_reading to get the latest average reading from the sensor
latest_reading, latest_weight_kg = reader.get_latest_reading()
if latest_reading is not None:
    print(f"Latest Average Reading: {latest_reading} | Approximate Weight: {latest_weight_kg:.3f} kg")
else:
    print("No data available yet.")

# Stop the reader when done

reader.stop()
