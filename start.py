import chiliIo
import signal
import time
import RPi.GPIO as GPIO

# wird bei ctrl+c ausgefuehrt
def cleanup(signal,frame):
  global program_running
  print('Ctrl+C captured, ending read.')
  program_running = False

def initialize():
  global program_running
  program_running = True
  
  # hook fuer ctrl+c    
  signal.signal(signal.SIGINT, cleanup)
  
  GPIO.setmode(GPIO.BCM)
  io = chiliIo.chiliIO()
 
def main():
  initialize()
  while program_running:
    time.sleep(2)

if __name__ == '__main__':
  main()