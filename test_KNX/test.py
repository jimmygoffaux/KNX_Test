import time
from KNX_Lib import KNX
from NI_Lib import NI
from ctypes import (
    CDLL, CFUNCTYPE,
    create_string_buffer,
    c_int, c_void_p,
    c_ushort, c_uint,
    c_ubyte, c_ulong,
    pointer, byref, 
    c_char_p
)

knx = KNX()
ni = NI()


class CMD:
    def __init__(self, nom, cont_val, act_val, det_stk, calib, max_stk, min_stk, lim_stk, relay):
        self.nom = nom
        self.cont_val = cont_val
        self.act_val = act_val
        self.det_stk = det_stk
        self.calib = calib
        self.max_stk = max_stk
        self.min_stk = min_stk
        self.lim_stk = lim_stk
        self.relay = relay


def CMD_SLD():
    sliders = [
        {"nom": "SLD160_1", "cont_val": 0x901, "act_val": 0x902, "det_stk": 0x903,
         "calib": 0x904, "max_stk": 0x905, "min_stk": 0x906, "lim_stk": 0x907, "relay": "none"},
        {"nom": "SLD160_2", "cont_val": 0xA01, "act_val": 0xA02, "det_stk": 0xA03,
         "calib": 0xA04, "max_stk": 0xA05, "min_stk": 0xA06, "lim_stk": 0xA07, "relay": "none"},
        {"nom": "SLD160_3", "cont_val": 0xB01, "act_val": 0xB02, "det_stk": 0xB03,
         "calib": 0xB04, "max_stk": 0xB05, "min_stk": 0xB06, "lim_stk": 0xB07, "relay": "none"},
        {"nom": "SLD160_4", "cont_val": 0xC01, "act_val": 0xC02, "det_stk": 0xC03,
         "calib": 0xC04, "max_stk": 0xC05, "min_stk": 0xC06, "lim_stk": 0xC07, "relay": "none"},
        {"nom": "SLD160_5", "cont_val": 0xD01, "act_val": 0xD02, "det_stk": 0xD03,
         "calib": 0xD04, "max_stk": 0xD05, "min_stk": 0xD06, "lim_stk": 0xD07, "relay": "none"},
        {"nom": "SLD160_R24_1", "cont_val": 0x1101, "act_val": 0x1102, "det_stk": 0x1103,
         "calib": 0x1104, "max_stk": 0x1105, "min_stk": 0x1106, "lim_stk": 0x1107, "relay": 0x110E}
    ]
    return sliders


sliders = CMD_SLD()
devices = []
for slider in sliders:
    device = CMD(**slider)
    devices.append(device)


def main():
    # global _verbose
    #output = "Dev1/ao0"
    #input = "Dev1/ai7"
    #ni.analog_out(output, 3)
    # We create a Access Port descriptor. This descriptor is then used for
    # all calls to that specific access port.
    print("start test")
    ap = knx.open_access_port()
    #sp = knx.serial_port(ap)
    #knx.ind_addr_prog_mode_read(sp)
    #knx.restart(sp, 0xA01)
    try:
       for slider in sliders:
         print("search sld")
        # if slider["nom"] == "SLD160_R24_1":
         knx.control_value(ap, slider["cont_val"], 0)
         time.sleep(30)
         value = ni.analog_in_stab(input)
         print("value on NI : ", value, "V")
    #             knx.control_value(ap, slider["cont_val"], 50)
    #             time.sleep(30)
    #             value = ni.analog_in_stab(input)
    #             print("value on NI : ", value, "V")
    #             knx.control_value(ap, slider["cont_val"], 100)
    #             time.sleep(30)
    #             value = ni.analog_in_stab(input)
    #             print("value on NI : ", value, "V")
    #             # knx.calibration(ap, slider["calib"], 0)
    except KeyboardInterrupt:
        print("Interrupted!")
    #     # break


if __name__ == '__main__':
    main()


# previous_value = None
# channel = "Dev1/ai7"
# first_read = read_stabilized_value(channel)
# while True:
#     stabilized_value = read_stabilized_value(channel)
#     print(f"first read : {first_read:.6f}")
#     print(f"Valeur stabilisée : {stabilized_value:.6f}")

#     if previous_value is not None:
#         variation = abs(stabilized_value - previous_value)
#         if variation > 0.001 or (abs(first_read - stabilized_value)) > 0.001:
#             break

#     previous_value = stabilized_value
#     time.sleep(1)  # Attendre 1 seconde avant la prochaine lecture

# print("Valeur stabilisée varie de plus de 0.01. Arrêt du programme.")
