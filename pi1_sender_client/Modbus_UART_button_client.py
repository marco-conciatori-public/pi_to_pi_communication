import time
from gpiozero import Button
from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ConnectionException

# --- Configuration ---
SERIAL_PORT = "/dev/ttyAMA0"
BAUD_RATE = 9600
BUTTON_PIN = 2  # BCM pin for the button
SLAVE_ID = 1  # The Slave ID of the server we want to talk to

# The Modbus address we are writing to. Coils are for single on/off values.
COIL_ADDRESS = 0


def run_button_client():
    """
    Monitors a button and writes its state to a specific Modbus coil
    on a remote server.
    """
    button = Button(BUTTON_PIN, pull_up=True)
    client = ModbusSerialClient(
        port=SERIAL_PORT,
        baudrate=BAUD_RATE,
        timeout=1
    )

    print("Attempting to connect to Modbus server...")
    if not client.connect():
        print(f"Failed to connect to the Modbus server on {SERIAL_PORT}.")
        return

    print("Successfully connected.")
    print(f"Watching button on GPIO {BUTTON_PIN}. Press Ctrl+C to exit.")

    last_state_pressed = False

    try:
        while True:
            current_state_pressed = button.is_pressed

            if current_state_pressed != last_state_pressed:
                print(f"Button state changed to {'PRESSED' if current_state_pressed else 'RELEASED'}.")

                try:
                    # --- Write to the Modbus Server ---
                    # We write the boolean state to a single coil.
                    # Function: write_coil(address, value, unit=slave_id)
                    write_response = client.write_coil(COIL_ADDRESS, current_state_pressed, unit=SLAVE_ID)

                    if write_response.isError():
                        print(f"Error writing to server: {write_response}")
                    else:
                        print(f"Successfully wrote {current_state_pressed} to Coil {COIL_ADDRESS}.")

                except ConnectionException:
                    print("Connection to server lost. Please restart client.")
                    break
                except Exception as e:
                    print(f"An error occurred during write: {e}")

                # Update the last known state
                last_state_pressed = current_state_pressed

            # Small delay to prevent high CPU usage
            time.sleep(0.02)

    except KeyboardInterrupt:
        print("\nClient stopped by user.")
    finally:
        if client.is_socket_open():
            client.close()
            print("Connection closed.")


if __name__ == "__main__":
    run_button_client()
