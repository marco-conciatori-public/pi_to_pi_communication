import time
import threading
from gpiozero import LED
from pymodbus.server import StartSerialServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext

# --- Configuration ---
SERIAL_PORT = "/dev/ttyAMA0"
BAUD_RATE = 9600
LED_PIN = 17  # BCM pin for the LED
SLAVE_ID = 0x01  # This is the Slave ID for this server

# The Modbus address we are monitoring.
COIL_ADDRESS = 0


def led_control_from_datastore(context, slave_id):
    """
    A helper function to run in a separate thread.
    It periodically checks the datastore's coil state and controls the LED.
    """
    print("Datastore monitor started.")
    led = LED(LED_PIN)
    last_coil_state = False

    while True:
        # Get the current state of the coil at our address
        # Function: getValues(function_code, address, count)
        # Function code 1 is for reading coils
        current_coil_state = context[slave_id].getValues(1, COIL_ADDRESS, count=1)[0]

        if current_coil_state != last_coil_state:
            if current_coil_state:
                print("Coil is ON -> Turning LED ON")
                led.on()
            else:
                print("Coil is OFF -> Turning LED OFF")
                led.off()

            last_coil_state = current_coil_state

        time.sleep(0.1)


def run_led_server():
    """
    Sets up and runs the Modbus RTU server with a coil datastore.
    """
    # Create the datastore for the server.
    # We create a block of 10 coils, all initialized to False (off).
    store = ModbusSlaveContext(
        co=ModbusSequentialDataBlock(0, [False] * 10)
    )

    context = ModbusServerContext(slaves=store, single=True)

    print("Modbus server starting up...")

    # Start the LED control monitor in a background thread
    monitor_thread = threading.Thread(
        target=led_control_from_datastore,
        args=(context, SLAVE_ID),
        daemon=True
    )
    monitor_thread.start()

    print("Server is running. Waiting for client commands...")
    StartSerialServer(
        context=context,
        port=SERIAL_PORT,
        baudrate=BAUD_RATE,
        timeout=1
    )


if __name__ == "__main__":
    print("Starting Modbus RTU LED Server. Press Ctrl+C to stop.")
    try:
        run_led_server()
    except KeyboardInterrupt:
        print("Server stopped by user.")
