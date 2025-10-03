import time
import serial
from gpiozero import Button

# --- Configuration ---
SERIAL_PORT = "/dev/ttyAMA0"
BAUD_RATE = 9600
# BCM pin number for the button
BUTTON_PIN = 2


def main():
    """
    Monitors a button and sends its state ('1' for pressed, '0' for released)
    over a serial connection.
    """
    # Initialize the button. pull_up=True means the pin is high by default
    # and goes low when the button connects it to ground.
    button = Button(BUTTON_PIN, pull_up=True)

    # Keep track of the last state to only send data when a change occurs
    last_state_pressed = False

    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            print(f"Serial port {SERIAL_PORT} opened.")
            print(f"Watching button on GPIO {BUTTON_PIN}. Press Ctrl+C to exit.")

            while True:
                current_state_pressed = button.is_pressed

                if current_state_pressed != last_state_pressed:
                    if current_state_pressed:
                        print("Button pressed, sending '1'...")
                        ser.write(b'1')
                    else:
                        print("Button released, sending '0'...")
                        ser.write(b'0')

                    # Update the last known state
                    last_state_pressed = current_state_pressed

                # A small delay to prevent high CPU usage
                time.sleep(0.02)

    except serial.SerialException as e:
        print(f"Error: Could not open serial port {SERIAL_PORT}.")
        print(f"Details: {e}")
    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
