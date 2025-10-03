import time
from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ConnectionException

# --- Configuration ---
SERIAL_PORT = "/dev/ttyAMA0"
BAUD_RATE = 9600
# The Slave ID of the server we want to talk to
SLAVE_ID = 1


def run_client():
    """
    Connects to a Modbus RTU Server, prompts the user for text,
    and writes the text's ASCII values to the server's holding registers.
    """
    # Create the Modbus client
    client = ModbusSerialClient(
        port=SERIAL_PORT,
        baudrate=BAUD_RATE,
        timeout=1,
    )

    print("Attempting to connect to Modbus server...")
    if not client.connect():
        print(f"Failed to connect to the Modbus server on {SERIAL_PORT}.")
        return

    print("Successfully connected. Type a short message and press Enter.")
    print("Type 'quit' to exit.")

    try:
        while True:
            message = input("Message to send: ")
            if message.lower() == 'quit':
                break

            # Convert the string message to a list of ASCII integer values
            # Modbus registers are 16-bit, so ASCII values fit perfectly.
            register_values = [ord(char) for char in message]

            if not register_values:
                print("Cannot send an empty message.")
                continue

            print(f"Message as register values: {register_values}")

            # --- Write to the Modbus Server ---
            # write to 'Holding Registers' starting at address 0.
            try:
                # The 'unit' keyword is used for the slave ID
                write_response = client.write_registers(address=0, values=register_values, slave=SLAVE_ID)

                # We check if the response object itself indicates an error.
                if write_response.isError():
                    print(f"Error writing to server: {write_response}")
                else:
                    print(f"Successfully wrote {len(register_values)} registers to Slave {SLAVE_ID}.")

            except ConnectionException:
                print("Connection to server lost. Please restart client.")
                break
            except Exception as e:
                print(f"An error occurred during write: {e}")
                break

            time.sleep(1)

    except KeyboardInterrupt:
        print("\nClient stopped by user.")
    finally:
        if client.is_socket_open():
            client.close()
            print("Connection closed.")


if __name__ == "__main__":
    run_client()
