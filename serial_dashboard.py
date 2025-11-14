# serial_dashboard.py
import serial, csv, time, sys

PORT = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyUSB0"
BAUD = 115200
OUT_CSV = "serial_log.csv"

ser = serial.Serial(PORT, BAUD, timeout=1)
print(f"Listening on {PORT} @ {BAUD}")

with open(OUT_CSV, "a", newline='') as csvfile:
    writer = csv.writer(csvfile)
    while True:
        try:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if not line:
                continue
            ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(f"{ts} | {line}")
            writer.writerow([ts, line])
            csvfile.flush()
        except KeyboardInterrupt:
            print("Exiting")
            break
        except Exception as e:
            print("Err:", e)
            time.sleep(0.5)
          
