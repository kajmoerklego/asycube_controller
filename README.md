# asycube_controller
The repo contains a class for controlling the individual actuators of an Asycube vibration table using JSON commands.
The JSON command should look something like the following:
```json
{
  "B": {
      "1": {
          "amplitude": 60,
          "frequency": 150,
          "phase": 0,
          "waveform": "1",
      },
      "2": {
          "amplitude": 60,
          "frequency": 150,
          "phase": 0,
          "waveform": "1",
      },
      "3": {
          "amplitude": 0,
          "frequency": 150,
          "phase": 0,
          "waveform": "1",
      },
      "4": {
          "amplitude": 0,
          "frequency": 150,
          "phase": 0,
          "waveform": "1",
      },
      "duration": 1000,
  },
}

```
Where the letter "B" is the location at which the vibration pattern should be stored. This can be any letter, but the following are already reserved: A-D-E-F-I-J-K
1-4 is the individual actuators and for each actuator you can control the amplitude, frequency, phase, and waveform.
The limits for the individual params depends on the asycube types, which is defined on page 22-25 in [the documentation](asycube_240.pdf).
The last setting is the duration for how long the vibration pattern should run.
<img width="1748" height="1058" alt="image" src="https://github.com/user-attachments/assets/0c6faacd-60b8-4f7f-b7bc-c2cd3509d6e2" />
