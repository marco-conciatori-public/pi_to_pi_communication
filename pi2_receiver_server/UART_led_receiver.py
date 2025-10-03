import time
import serial
from gpiozero import LED

# --- Configuration ---
SERIAL_PORT = "/dev/ttyAMA0"
BAUD_RATE = 9600
# BCM pin number for the LED
LED_PIN = 17


def main():
    """
    Listens for incoming serial data and controls an LED based on the
    received message ('1' for ON, '0' for OFF).
    """
    led = LED(LED_PIN)

    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            print(f"Listening for data on {SERIAL_PORT}...")
            print(f"LED connected to GPIO {LED_PIN}. Press Ctrl+C to exit.")

            while True:
                # Check if there is data in the serial buffer
                if ser.in_waiting > 0:
                    # Read a single byte of data
                    data_byte = ser.read(1)

                    if data_byte == b'1':
                        print("Received '1' -> LED ON")
                        led.on()
                    elif data_byte == b'0':
                        print("Received '0' -> LED OFF")
                        led.off()

                # A small delay to prevent high CPU usage
                time.sleep(0.01)

    except serial.SerialException as e:
        print(f"Error: Could not open serial port {SERIAL_PORT}.")
        print(f"Details: {e}")
    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting.")
        led.off()  # Ensure LED is off on exit
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
