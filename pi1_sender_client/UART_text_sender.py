import time
import serial

# --- Configuration ---
# The primary UART on Raspberry Pi 5 is typically /dev/ttyAMA0
# If that doesn't work, you can try /dev/serial0
SERIAL_PORT = "/dev/ttyAMA0"
BAUD_RATE = 9600


def send_message():
    """
    Initializes the serial connection and enters a loop to send user input.
    """
    # The 'with' statement ensures the serial port is automatically closed
    # even if an error occurs.
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            print(f"Serial port {SERIAL_PORT} opened successfully.")
            print("Type your message and press Enter to send.")
            print("Type 'quit' to exit.")

            while True:
                # Get input from the user
                message = input("Message: ")

                if message.lower() == 'quit':
                    print("Exiting sender program.")
                    break

                # The message needs to be encoded into bytes before sending.
                # We add a newline character so the receiver knows when the message ends.
                encoded_message = message.encode('utf-8') + b'\n'

                # Write the encoded message to the serial port
                ser.write(encoded_message)
                print(f"Sent: {message}")

                # A small delay to ensure the message is sent completely
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
    send_message()
