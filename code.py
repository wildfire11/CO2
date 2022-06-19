
import time
import board
import adafruit_scd4x
import microcontroller
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306

i2c = board.I2C()
scd4x = adafruit_scd4x.SCD4X(i2c)
print("Serial number:", [hex(i) for i in scd4x.serial_number])

displayio.release_displays()

oled_reset = board.D9

# Use for I2C
i2c = board.I2C()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C, reset=oled_reset)

WIDTH = 128
HEIGHT = 32  # Change to 64 if needed
BORDER = 5

display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)

# Make the display context
splash = displayio.Group()
display.show(splash)

color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF  # White

text = "Getting ready..."
text_area = label.Label(
    terminalio.FONT, text=text, color=0xFFFFFF, x=10, y=HEIGHT // 2 - 1
)
splash.append(text_area)


scd4x.start_periodic_measurement()
print("Waiting for first measurement....")

while True:
    if scd4x.data_ready:
        print("CO2: %d ppm" % scd4x.CO2)
        print("Internal temp: %d *C" % microcontroller.cpu.temperature)
        print("Temperature: %0.1f *C" % scd4x.temperature)
        print("Humidity: %0.1f %%" % scd4x.relative_humidity)
        print()
        text_area.text = "CO2: %d ppm" % scd4x.CO2
                
    time.sleep(1)
    
