import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, FallingEdge, RisingEdge
import pandas as pd 
import numpy as np
from scipy import signal
import random

@cocotb.test()
async def cic_tb(dut):
    #rpdb.set_trace()
    total_cycles = 10000

    clock = Clock(dut.i_clk, 1, units="ns")  # Create a 10us period clock on port clk
    cocotb.fork(clock.start())  # Start the clock

    await FallingEdge(dut.i_clk)  # Synchronize with the clock
    dut.i_data <= 0  # Assign the random value val to the input port d
    dut.i_ready <= 1
    #init
    await Timer(10, "ns") #skip the undefined state

    i_data = np.empty(shape=total_cycles)
    integrated_data = np.empty(shape=total_cycles)
    decimated_data = np.empty(shape=total_cycles)
    o_data = np.empty(shape=total_cycles)
    o_ready = np.empty(shape=total_cycles)

    t = np.linspace(0, 1, total_cycles, endpoint=False)
    sig = np.sin(2 * 10* np.pi * t)
    pwm = signal.square(2 * np.pi * 1000 * t, duty=(sig + 1)/2)

    for i in range(total_cycles):
        await RisingEdge(dut.i_clk)

        val = int(pwm[i])
        #print (sig[i], val)
        dut.i_data <= val  # Assign the random value val to the input port d
        dut.i_ready <= 1
        i_data[i] = val
        integrated_data[i] = dut.integrator_data[0].value.signed_integer
        decimated_data[i] = dut.decimator_data.value.signed_integer

        o_data[i] = dut.o_data.value.signed_integer
        o_ready[i] = dut.o_ready.value

    df = pd.DataFrame({ 'i_data': i_data,
                        'decimated_data': decimated_data,
                        'integrated_data': integrated_data,
                        'o_data': o_data, 
                        'o_ready': o_ready,
                      })
    df.to_csv("wave.csv")