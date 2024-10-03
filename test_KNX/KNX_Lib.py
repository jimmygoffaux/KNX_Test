import time
import sys
from ctypes import (
    CDLL, CFUNCTYPE,
    create_string_buffer,
    c_int, c_void_p,
    c_ushort, c_uint,
    c_ubyte, c_ulong,
    pointer, byref,
    c_char_p
)


# load the kdriveExpress dll (windows)
# for linux replace with kdriveExpress.so
kdrive = CDLL('./libkdriveExpress.so')  # the error callback pointer to function type
ERROR_CALLBACK = CFUNCTYPE(None, c_int, c_void_p)

# defines from kdrive (not available from the library)
KDRIVE_INVALID_DESCRIPTOR = -1
KDRIVE_ERROR_NONE = 0
KDRIVE_LOGGER_FATAL = 1
KDRIVE_LOGGER_INFORMATION = 6

_verbose = 0

# Set to 1 to use connection-oriented
# Set to 0 for connection-less
connection_oriented = 0


class KNX:
    def open_access_port(self):
        ap = kdrive.kdrive_ap_create()
        print("ap=", ap)
        if (ap != KDRIVE_INVALID_DESCRIPTOR):
            if (kdrive.kdrive_ap_enum_usb(ap) == 0) or (kdrive.kdrive_ap_open_usb(ap, 0) != KDRIVE_ERROR_NONE):
                kdrive.kdrive_ap_release(ap)
                ap = KDRIVE_INVALID_DESCRIPTOR
                print("KDRIVE_INVALID_DESCRIPTOR")
                sys.exit()
        return ap

    def serial_port(self, ap):
        sp = kdrive.kdrive_sp_create(ap)
        # sp = 1
        print("sp=", sp)
        if sp == KDRIVE_INVALID_DESCRIPTOR:
            print("KDRIVE_INVALID_DESCRIPTOR")
            sys.exit()
        return sp

    def restart(self, sp, add):
        kdrive.kdrive_sp_restart_device_type0(sp, add)

    def my_list_func(self, count, p_items):  #Returns a python list for the given times represented by a pointer and the number of items
        items = []
        for i in range(count):
            items.append(p_items[i])
        return items

    def read(self, ap, addr, type):
        buf = (c_ubyte * 64)()
        data = (c_ubyte * 14)()
        data_len = c_ulong(14)
        buf_len = kdrive.kdrive_ap_read_group_object(ap, addr, buf, len(buf), 1000)

        if type == "pulse":
            if buf_len > 0:
                kdrive.kdrive_ap_get_group_data(buf, buf_len, data, pointer(data_len))
                list = self.my_list_func(data_len.value, data)
                # print(l)
                answer = list[0] * 256 + list[1]
                print(answer)
                return answer
        if type == "pourcent":
            if buf_len > 0:
                kdrive.kdrive_ap_get_group_data(buf, buf_len, data, pointer(data_len))
                list = self.my_list_func(data_len.value, data)
                list = list[0]
                if list != 0:
                    # l = int(l, 0)
                    answer = (list*100)/255
                else:
                    answer = list
                print(answer)
                return answer
        if type == "switch":
            if buf_len > 0:
                kdrive.kdrive_ap_get_group_data(buf, buf_len, data, pointer(data_len))
                list = self.my_list_func(data_len.value, data)
                # print(l)
                answer = list[0]
                print(answer)
                return answer

        else:
            return None

    def control_value(self, ap, group_add, val_pos):
        ga = group_add
        val_pos = val_pos/100
        position = (c_ubyte * 1)(int(val_pos * 255))
        # position = (c_ubyte * 1)(int(val_pos * 255))  # value in pourcent
        print("position = ", position)
        try:
            kdrive.kdrive_ap_group_write(ap, ga, position, 8)
            # time.sleep(30)
        except KeyboardInterrupt:
            print("Interrupted!")
        return True

    def actual_value(self, ap, group_add):
        ga = group_add
        try:
            # print("slider name : ", slider["nom"])
            print("actual value :")
            self.read(ap, ga, "pourcent")

            time.sleep(1)
        except KeyboardInterrupt:
            print("Interrupted!")
        return True

    def detected_stroke(self, ap, group_add):
        ga = group_add
        try:
            self.read(ap, ga, "pulse")
            print("detected stroke :")
            time.sleep(1)
        except KeyboardInterrupt:
            print("Interrupted!")
        return True

    def calibration(self, ap, group_add, type):  # type : 0 = full calib / 1 = fast calib
        ga = group_add
        buffer = (c_ubyte * 1)(type)
        try:
            kdrive.kdrive_ap_group_write(ap, ga, buffer, 1)
            print('calibration in progress')
            time.sleep(180)

        except KeyboardInterrupt:
            print("Interrupted!")
        return True

    def maximum_stroke(self, ap, group_add):
        ga = group_add
        try:
            self.read(ap, ga, "pulse")
            time.sleep(1)
        except KeyboardInterrupt:
            print("Interrupted!")
        return True

    def minimum_stroke(self, ap, group_add):
        ga = group_add
        try:
            self.read(ap, ga, "pulse")
            time.sleep(1)
        except KeyboardInterrupt:
            print("Interrupted!")
        return True

    def limited_stroke(self, ap, group_add):
        ga = group_add
        try:
            self.read(ap, ga, "pulse")
            time.sleep(1)
        except KeyboardInterrupt:
            print("Interrupted!")
        return True

    def relay(self, ap, group_add, value):
        ga = group_add
        val = value
        buffer = (c_ubyte * 1)(val)
        try:
            kdrive.kdrive_ap_group_write(ap, ga, buffer, 1)
            # time.sleep(1)
            # answer = read(ap, slider["relay"], "switch")
            # print(answer)
            # assert answer == val

        except KeyboardInterrupt:
            print("Interrupted!")
        return True


# ap = KNX.open_access_port()

# if ap == KDRIVE_INVALID_DESCRIPTOR:
#     print("test")
#     kdrive.kdrive_logger(KDRIVE_LOGGER_FATAL, 'Unable to create access port. This is a terminal failure')
    # return


def main():
    global _verbose

    # We create a Access Port descriptor. This descriptor is then used for
    # all calls to that specific access port.
    print("start test")
    ap = KNX.open_access_port()
    try:
        kdrive.kdrive_sp_restart_device_type0(ap, 0xA01)

    except KeyboardInterrupt:
        print("Interrupted!")
        # break


if __name__ == '__main__':
    main()
