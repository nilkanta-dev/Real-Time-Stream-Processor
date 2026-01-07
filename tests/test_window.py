import time
from pipeline.window_manager import WindowManager

w = WindowManager(window_size=3)

w.add_event("apple")
w.add_event("banana")
w.add_event("apple")

print("Freq:", w.get_frequencies())  
# {'apple': 2, 'banana': 1}

time.sleep(4)
w.add_event("cherry")

print("Freq after cleanup:", w.get_frequencies())
# old ones should be gone

