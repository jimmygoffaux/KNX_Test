import time
import nidaqmx
# from nidaqmx.constants import AcquisitionType


class NI():
    def analog_out(self, channel, value):  # exemple channel : "Dev1/ao0"
        with nidaqmx.Task() as task_ao:
            task_ao.ao_channels.add_ao_voltage_chan(channel)
            voltage_to_output = value
            task_ao.write(voltage_to_output)
            time.sleep(0.5)

    def analog_in(self, channel):  # exemple channel : "Dev1/ai7"
        with nidaqmx.Task() as task_ai:
            task_ai.ai_channels.add_ai_voltage_chan(channel)
            valeur = task_ai.read()
            print("valeur lue : ", valeur)

    def analog_in_stab(self, channel, samples=100):  # exemple channel : "Dev1/ai7"
        with nidaqmx.Task() as task:
            task.ai_channels.add_ai_voltage_chan(channel)
            readings = [task.read() for _ in range(samples)]
            return sum(readings) / samples
