# System resource monitor that uses psutil to obtain resource information

import psutil
import curses
from time import sleep

def main(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Welcome to the resources monitor written in Python")
    stdscr.refresh()

    while True:
        cpu_usage = psutil.cpu_percent(interval=None,
                                        percpu=True)
        memory = (psutil.virtual_memory()[0] - psutil.virtual_memory()[1]) / psutil.virtual_memory()[0] * 100
        disk_usage = psutil.disk_io_counters(perdisk=True,
                                             nowrap=True)["PhysicalDrive0"]
        network = psutil.net_io_counters(pernic=False,
                                         nowrap=True)
        info = f"""CPU Usage\t-\t{cpu_usage}\nMemory\t\t-\t{memory}
Disk Usage\t-\t{(disk_usage.read_count)} - {disk_usage.write_count}
Network\t\t-\t{network.packets_sent} - {network.packets_recv}"""
        stdscr.addstr(2, 0, info)
        stdscr.refresh()
        sleep(1)
        stdscr.clear()
if __name__ == "__main__":
    curses.wrapper(main)