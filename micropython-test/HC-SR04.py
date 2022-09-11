from machine import Pin
import rp2
from time import sleep


@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW)
def measure():
    wrap_target()
    pull()
    mov(x, invert(null)).side(1)
    set(y, 20)
    label('delay')
    jmp(y_dec, 'delay')[5]
    nop().side(0)
    label('wait')
    jmp(pin, 'start')
    jmp('wait')
    label('start')
    jmp(x_dec, 'cont')
    label('cont')
    jmp(pin, 'start')
    in_(x, 32)
    push()
    wrap()


sm = rp2.StateMachine(0, measure, freq=10000000, jmp_pin=Pin(27, Pin.IN), sideset_base=Pin(26, value=0))
sm.active(1)

sleep(1)
sm.put(1)
sleep(1)
result = sm.get()

print((2**32 - 1 - result) * 2 / 10**7 * 340 / 2)
