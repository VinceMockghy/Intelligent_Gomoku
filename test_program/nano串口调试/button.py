from periphery import GPIO

gpio_get = GPIO(38,"in")

while 1:
    value = gpio_get.read()
    print(value)

gpio_get.close()
