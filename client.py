import pika
import os
import psutil
import socket
import platform
from config import mq_server, queue_name, exchange

# Standard connection setup
connection = pika.BlockingConnection(pika.ConnectionParameters(mq_server))
channel = connection.channel()


def queue_setup():
    channel.queue_declare(queue_name)


def send_message_to_queue(body, ex=exchange, route_key=queue_name):
    channel.basic_publish(ex, route_key, body)
    print(f" [x] Sent {body} to queue {route_key}")


def get_os():
    return platform.system()


def get_host_name():
    return socket.gethostname()


def get_ip_address(interface='eth0'):
    import netifaces
    netifaces.ifaddresses(interface)
    ip = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
    return ip


def get_cpu_usage_percent():
    cpu_time_interval = 5
    return psutil.cpu_percent(cpu_time_interval)


def get_cpu_frequency():
    return int(psutil.cpu_freq().current)


def get_cpu_temp(degree_format='fahrenheit'):
    # Only compatible with Linux
    if get_os() == 'Linux':
        result = 0.0
        if os.path.isfile('/sys/class/thermal/thermal_zone0/temp'):
            with open('/sys/class/thermal/thermal_zone0/temp') as f:
                line = f.readline().strip()
            if line.isdigit():
                result = float(line) / 1000

        # Returns in Celsius
        if degree_format == 'fahrenheit':
            result = (result * 1.8) + 32

        return int(result)
    # elif get_os() == 'Windows':
    #     import wmi
    #     w = wmi.WMI('root\\wmi')
    #     temp = w.MSAcpi_ThermalZoneTemperature()[0]
    #     return int(temp.CurrentTemperature)
    else:
        return 'Not Supported'


def get_ram_usage_bytes(size_format: str = 'M'):
    """
    Size formats include K = Kilobyte, M = Megabyte, G = Gigabyte
    """
    total = psutil.virtual_memory().total
    available = psutil.virtual_memory().available
    used = total - available

    # Apply size
    if size_format == 'K':
        used = used / 1024
    if size_format == 'M':
        used = used / 1024 / 1024
    if size_format == 'G':
        used = used / 1024 / 1024 / 1024

    return int(used)


def get_ram_usage_percent():
    return psutil.virtual_memory().percent


def get_swap_usage_percent():
    return psutil.swap_memory().percent


# Gather information we'd like to send
def gather_info():
    import datetime
    current_timestamp = str(datetime.datetime.now())

    results = {
        "timestamp": current_timestamp,
        "hostname": get_host_name(),
        "os": get_os(),
        "ip_address": get_ip_address('wlp0s20f3'),
        "cpu_usage_percent": get_cpu_usage_percent(),
        "cpu_frequency": get_cpu_frequency(),
        "cpu_temperature": get_cpu_temp(),
        "memory_usage_percent": get_ram_usage_percent(),
        "memory_usage": get_ram_usage_bytes(),
        "swap_usage_percent": get_swap_usage_percent()
    }

    return results


send_message_to_queue(str(gather_info()))

connection.close()
