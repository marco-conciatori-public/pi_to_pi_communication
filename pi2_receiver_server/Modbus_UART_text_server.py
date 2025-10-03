import time
# import logging
import threading
from pymodbus.server import StartSerialServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext

# --- Configuration ---
SERIAL_PORT = "/dev/ttyAMA0"
BAUD_RATE = 9600
# This is the Slave ID for this server
SLAVE_ID = 0x01

# Optional: configure logging to see detailed Modbus frames
# logging.basicConfig()
# log = logging.getLogger()
# log.setLevel(logging.DEBUG)


def monitor_datastore_changes(context, slave_id):
    """
    A helper function to run in a separate thread.
    It periodically checks the datastore for changes and prints them.
    """
    print("Datastore monitor started.")
    last_values = []

    while True:
        # Get the block of holding registers for our slave
        # address=0, count=20 means we read 20 registers starting from address 0
        current_values = context[slave_id].getValues(3, 0, count=20)

        if current_values != last_values:
            # Filter out trailing zeros for cleaner display
            try:
                end_index = current_values.index(0)
                display_values = current_values[:end_index]
            except ValueError:
                display_values = current_values

            if display_values:
                # Convert ASCII values back to a string
                try:
                    message = "".join([chr(val) for val in display_values])
                    print(f"\n--- Data Changed ---")
                    print(f"Received Message: '{message}'")
                    print(f"Register values: {display_values}")
                    print("--------------------\n")
                except ValueError:
                    print(f"Received non-printable data: {display_values}")

            last_values = list(current_values)  # Make a copy

        time.sleep(0.5)


def run_server():
    """
    Sets up and runs the Modbus RTU server.
    """
    # Create the datastore for the server.
    # We create a block of 100 holding registers, all initialized to 0.
    store = ModbusSlaveContext(
        hr=ModbusSequentialDataBlock(address=0, values=[0] * 100)
    )

    # Create the server context, mapping the datastore to our slave ID
    context = ModbusServerContext(store, single=True)

    print("Modbus server starting up...")

    # Start the datastore monitor in a background thread
    monitor_thread = threading.Thread(target=monitor_datastore_changes, args=(context, SLAVE_ID), daemon=True)
    monitor_thread.start()

    # Start the Modbus serial server
    # This function blocks and runs forever
    StartSerialServer(
        context=context,
        port=SERIAL_PORT,
        baudrate=BAUD_RATE,
        timeout=1
    )


if __name__ == "__main__":
    print("Starting Modbus RTU Server. Press Ctrl+C to stop.")
    try:
        run_server()
    except KeyboardInterrupt:
        print("Server stopped by user.")
