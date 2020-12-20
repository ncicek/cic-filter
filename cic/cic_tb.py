import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, FallingEdge, RisingEdge
import pandas as pd 
import numpy as np
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
    o_data = np.empty(shape=total_cycles)
    o_ready = np.empty(shape=total_cycles)

    for i in range(total_cycles):
        await RisingEdge(dut.i_clk)

        val = [-1,1][random.randrange(2)]
        #print (val)
        dut.i_data <= val  # Assign the random value val to the input port d
        dut.i_ready <= 1
        i_data[i] = val
        o_data[i] = dut.o_data.value.signed_integer
        o_ready[i] = dut.o_ready.value

    df = pd.DataFrame({ 'i_data': i_data,
                        'o_data': o_data, 
                        'o_ready': o_ready,
                      })
    df.to_csv("wave.csv")