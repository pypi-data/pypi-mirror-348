"""Example demonstrates simple read and write data operations through Serial COM port"""  

# pylint: disable=W0105

import pyvisa
import pyvisa.constants

# import functions
import nipcbatt
from nipcbatt.pcbatt_utilities.pcbatt_logger import PcbattLogger

# Note to run with Hardware: Update Serial VISA for the COM port

DEVICE_ID = "DeviceB"
SESSION_NUMBER = 0

# Set the default file path to save the acquired waveforms and measurement analysis results.
DEFAULT_FILEPATH = "C:\\Windows\\Temp\\serial_comm_test_results.txt"


# region initialize
######## INITIALIZE ################################################################################
def setup():
    """Creates and initializes serial communication object""" 
    resource = nipcbatt.SerialCommunication()
    resource.initialize(serial_device_name=DEVICE_ID)
    return resource


# endregion initialize


# region configure
####### CONFIGURE & READ/WRITE DATA ###############################################################
def main(
    resource: nipcbatt.SerialCommunication,
    write_to_file: bool,
):
    """If you wish to write your results to a file use the following commands
    Make sure the write_to_file option is set to True when calling i2c_comm_test()
    Change the file path to desired location on your drive
    The default file path is C:\\Windows\\Temp\\serial_comm_test_results.txt"""  

    # if write_to_file is True, call write_results_to_file in order to output the results to a file
    if write_to_file:
        logger = PcbattLogger(file=DEFAULT_FILEPATH)
        logger.attach(resource)

    """Note to run with Hardware: Update Serial comm settings for write-read operation"""

    # Update the Serial Write Command based on the usecase

    comm_params = nipcbatt.SerialCommunicationParameters(
        data_rate_bauds=9600,
        number_of_bits_in_data_frame=8,
        delay_before_receive_response_milliseconds=500,
        parity=pyvisa.constants.Parity.none,
        stop_bits=pyvisa.constants.StopBits.one,
        flow_control=pyvisa.constants.ControlFlow,
    )

    command = "IDN?\n"  # Update the command to send

    config = nipcbatt.SerialCommunicationConfiguration(
        communication_parameters=comm_params, command_to_send=command
    )

    response_data = resource.configure_then_send_command_and_receive_response(configuration=config)

    """Storing results -- create both a Python dictionary (hashmap) 
    A dictionary will store values with a key provided by the user"""
    results_map = {}  # this structure will hold results in key-value pairs

    # record result
    results_map["SERIAL DATA"] = response_data.received_response()

    return response_data


# endregion configure


# region close
############################# CLEAN UP FUNCTION: CLOSE ALL TASKS ###################################


# Close all tasks
def cleanup(resource: nipcbatt.SerialCommunication):
    """Closes out the created objects used in the communication""" 
    resource.close()


####################################################################################################
# endregion close


# region test
############# USE THIS FUNCTION TO CALL THE WHOLE SEQUENCE #########################################
def serial_comm_test():
    """Execute all steps in the sequence"""  

    # Run setup function
    serial_resource = setup()

    # Run main function
    main(resource=serial_resource, write_to_file=True)

    # run cleanup function
    cleanup(serial_resource)


####################################################################################################
# endregion test  
