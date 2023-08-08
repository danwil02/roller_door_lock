from PiicoDev_TMP117 import PiicoDev_TMP117, sleep_ms

tempsensor = PiicoDev_TMP117()

while True:
    tempC = tempsensor.readTempC()
    sleep_ms(1000)
    print(tempC)
