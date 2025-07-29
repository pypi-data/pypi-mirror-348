#!/usr/bin/env python
# SPDX-License-Identifier: MIT

from absl import app, flags

from os.path import basename, expanduser
from typing import List

from .config import ToolConfig
from .device import Device
from .types import *

FLAGS = flags.FLAGS
flags.DEFINE_string('config_file', '~/.busytag.toml', 'Config file path')
flags.DEFINE_string('device', None, 'Busy Tag\'s serial port.')
flags.DEFINE_integer('baudrate', 115200, 'Connection baudrate.')

def format_size(size: int) -> str:
    if size < 1_000:
        return f'{size} B'
    if size < 500_000:
        return f'{size/1_000:.2f} kB'
    return f'{size/1_000_000:.2f} MB'


def main(argv: List[str]) -> None:
    config = ToolConfig(FLAGS.config_file)
    if FLAGS.device is not None:
        config.device = FLAGS.device
    if config.device is None:
        raise Exception('Device must be specified')

    bt:Device = None

    # Remove argv[0]
    argv.pop(0)
    command = 'help'
    if len(argv) > 0:
        command = argv.pop(0)
        bt = Device(config.device, baudrate=FLAGS.baudrate)


    match command:
        case 'info':
            print(f'Device name:      {bt.name}')
            print(f'Device ID:        {bt.device_id}')
            print(f'Firmware version: {bt.firmware_version}')
            print(f'Serial port:      {config.device}')
            print(f'Storage capacity: {format_size(bt.capacity)}')
            print(f'Free storage:     {format_size(bt.get_free_storage())}')

        case 'list_pictures':
            print('Pictures in device:')
            for picture in bt.list_pictures():
                print(f'  {picture.name} ({format_size(picture.size)})')
            print(f'Available space: {format_size(bt.get_free_storage())}')

        case 'list_files':
            print('Files in device: ')
            for file in bt.list_files():
                print(f'  {file.name} ({file.type.value} - {format_size(file.size)})')
            print(f'Available space: {format_size(bt.get_free_storage())}')

        case 'set_picture':
            assert len(argv) >= 1
            bt.set_active_picture(argv.pop(0))

        case 'get_picture':
            print(f'Current active picture: {bt.get_active_picture()}')

        case 'put':
            assert len(argv) >= 1
            filename = expanduser(argv.pop(0))
            with open(filename, 'rb') as fp:
                bt.upload_file(basename(filename), fp.read())

        case 'get':
            assert len(argv) >= 1
            filename = argv.pop(0)
            data = bt.read_file(filename)
            with open(filename, 'wb') as fp:
                fp.write(data)

        case 'rm':
            assert len(argv) >= 1
            filename = argv.pop(0)
            bt.delete_file(filename)

        case 'set_led_solid_color':
            assert len(argv) >= 1
            led_config = LedConfig(LedPin.ALL, argv.pop(0).upper())
            bt.set_led_solid_color(led_config)

        case 'get_brightness':
            print(f'Brightness: {bt.get_display_brightness()}')

        case 'set_brightness':
            assert len(argv) >= 1
            brightness = int(argv.pop(0))
            assert 0 < brightness <= 100
            bt.set_display_brightness(brightness)

        case 'help':
            print('Available commands:')
            print('  help: Prints this message')
            print('  info: Displays device information')
            print('  list_pictures: Lists pictures in device')
            print('  list_files: Lists files in device')
            print('  get_picture: Gets the filename of the picture being shown')
            print('  set_picture <filename>: Sets the picture shown in the device')
            print('  put <filename>: Uploads <filename>')
            print('  get <filename>: Copies <filename> from the device to the working directory')
            print('  rm <filename>: Deletes <filename>')
            print('  set_led_solid_color <6 hex RGB colour>: Sets the LEDs colour')
            print('  get_brightness: Gets current display brightness')
            print('  set_brightness <brightness>: Sets current display brightness (int between 1 and 100, inclusive')

        case _:
            print(f'Unknown command `{command}`. Please use the `help` to list available commands')

    config.write_to_file()

def run_main():
    app.run(main)

if __name__ == '__main__':
    run_main()