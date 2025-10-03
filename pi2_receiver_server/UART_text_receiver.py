import time
import serial

# --- Configuration ---
# Ensure these settings match the sender's configuration
SERIAL_PORT = "/dev/ttyAMA0"
BAUD_RATE = 9600


def receive_messages():
    """
    Initializes the serial connection and continuously listens for incoming messages.
    """
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            print(f"Listening for data on {SERIAL_PORT} at {BAUD_RATE} baud...")

            while True:
                # Check if there is data waiting in the serial buffer
                if ser.in_waiting > 0:
                    # ser.readline() reads until a newline character ('\n') is found
                    line = ser.readline()

                    # Decode the bytes into a string and strip leading/trailing whitespace
                    message = line.decode('utf-8').strip()

                    # Print the received message
                    if message:
                        print(f"Received: {message}")

                # A small delay to prevent the loop from consuming too much CPU
                time.sleep(0.1)

    except serial.SerialException as e:
        print(f"Error: Could not open serial port {SERIAL_PORT}.")
        print(f"Details: {e}")
        print("Please ensure the serial port is configured correctly and not in use by another program.")
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    receive_messages()
