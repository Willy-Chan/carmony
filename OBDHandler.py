import pygame
import obd
import time
import sys

class OBDHandler():
    def __init__(self, simulate_inputs: bool):
        if simulate_inputs:
            self.connection = None  # Set to None for simulation purposes
        else:
            self.connection = obd.OBD("COM4") # auto-connects to USB or RF port
            
        self.simulate_inputs = simulate_inputs
        self.speed = 0
        self.rpm = 0
    
    
    """
    Get Car Attributes
    """
    def get_speed(self):
        if self.simulate_inputs:
            return self.speed
        else:
            cmd = obd.commands.SPEED # select an OBD command (sensor)
            response = self.connection.query(cmd) # send the command, and parse the response
            return response.value.to("mph").magnitude # user-friendly unit conversions
        
    def get_rpm(self):
        if self.simulate_inputs:
            return self.rpm
        else:
            cmd = obd.commands.RPM # select an OBD command (sensor)
            response = self.connection.query(cmd) # send the command, and parse the response
            return response.value.magnitude  # user-friendly unit conversions
    
    def refresh(self):
        self.rpm = self.get_rpm()
        self.speed = self.get_speed()
        # not needed for simulated driving
    
    
    """
    Adjust Volume: changes the volume and set the slopes for how they should change depending
    on the inputs above
    """
    def get_bass_volume(self):
        bass_percent = self.rpm / 7000
        bass_volume = min(bass_percent + 0.5, 1)
        return bass_volume
    
    def get_drums_volume(self):
        drums_percent = self.speed / 70
        drums_volume = max(min(drums_percent * 7 - 1, 1), 0)
        return drums_volume

    def get_other_volume(self):
        other_percent = self.speed / 70
        other_volume = max(min(other_percent * 7 - 2.5, 1), 0)
        return other_volume
    
    def get_vocals_volume(self):
        vocals_percent = self.speed / 70
        vocals_volume = max(min(vocals_percent * 7 - 4, 1), 0)
        return vocals_volume
    
    # All of the volumes are later exported via this function's dictionary.
    def get_volumes(self):
        volumes = {
            'piano': 0.5,
            'bass': self.get_bass_volume(),
            'vocals': self.get_vocals_volume(),
            'drums': self.get_drums_volume(),
            'guitar': self.get_other_volume(),
            'other': 0.8
        }
        return volumes
    
    
    
    
    """
    SIMULATION of all of the car attributes.
    """
    def simulate_accelerator(self, amount):
        self.rpm = min(self.rpm + amount, 7000)  # 7000 is the MAX RPM
        self.speed = min(self.speed + amount * 0.01, 120)
    
    def simulate_brake(self, amount):
        self.rpm = max(self.rpm - amount, 0)
        self.speed = max(self.speed - amount * 0.05, 0)
    
    def simulate_steering(self, direction, amount):
        self.speed = max(self.speed - amount * 0.05, 0)   # only change speed...

