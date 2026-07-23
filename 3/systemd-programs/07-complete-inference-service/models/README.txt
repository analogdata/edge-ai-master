Place your model.tflite file in this directory.

On the Raspberry Pi, this would be:
  /home/pi/edgeai/models/model.tflite

The ExecStartPre in edgeai.service checks that this file exists
before starting the inference script.
