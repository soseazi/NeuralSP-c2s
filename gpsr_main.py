#!/usr/bin/python2.7
from __future__ import print_function
import signal
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import pepper_io

import gpsr_config as config
import gpsr_state as state


DEBUGGING = False


# TODO: where to put this?
def init_pio():
    config.pio.set_volume(config.params.volume)
    config.pio.set_tts_parameter("defaultVoiceSpeed", config.params.voice_speed)
    config.pio.clear_reid_targets()
    config.pio.load_waypoints(config.params.file_waypoint, say=False)
    if config.params.debugging:
        config.pio.say("start debugging mode")
    config.pio.activate_keyboard_control()
    if config.params.data_recording:
        config.pio.start_data_recording()
    config.pio.set_initial_pose_wp(config.params.wp_start, 0.05, -0.002)

def main():
    pio = pepper_io.PepperIO(config.get_pio_params())
    config.params = config.Params(debugging=DEBUGGING)
    config.pio = pio
    state_machine = None

    pio.enable_head_fix(True)
    # pio.set_initial_pose([0, 0, 0], [0, 0, 0, 1], 0.01)
    pio.right_arm_motion("release")


    def signal_handler(signum, frame):
        if state_machine is not None:
            state_machine.terminate()
        if pio is not None:
            pio.stop()
            pio.say("emergency stop")
            pio.activate_keyboard_control()

    signal.signal(signal.SIGINT, signal_handler)

    init_pio()

    state_machine = state.StateMachine()
    state_machine.run()


if __name__ == "__main__":
    main()
