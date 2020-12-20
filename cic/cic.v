module cic (
    i_clk,
    i_reset,
    i_data,
    i_ready,
    o_data,
    o_ready
    );

    parameter IW=2, OW=16, M=5;

    input wire i_clk, i_reset;
    input wire signed [(IW-1):0] i_data;
    input wire i_ready;
    output wire signed [(OW-1):0] o_data;
    output wire o_ready;


    wire signed [(OW-1):0] integrated_data;
    wire integrated_ready;
    integrator #(
        .IW(IW),
        .OW(OW),
        .M(M)) 
    integrator_0 (
        .i_clk(i_clk),
        .i_data(i_data),
        .i_ready(i_ready),
        .o_data(integrated_data),
        .o_ready(integrated_ready)
    ); 

    wire decimated_ready;
    wire signed [(OW-1):0] decimated_data;
    decimator #(.W(OW),
                .M(M)) 
    decimator_0 (
        .i_clk(i_clk),
        .i_data(integrated_data),
        .i_ready(integrated_ready),
        .o_data(decimated_data),
        .o_ready(decimated_ready)
    );

    comb #(
        .IW(OW),
        .OW(OW),
        .M(M)) 
    comb_0 (
        .i_clk(i_clk),
        .i_data(decimated_data),
        .i_ready(decimated_ready),
        .o_data(o_data),
        .o_ready(o_ready)
    );


    `ifdef COCOTB_SIM
    initial begin
    $dumpfile ("cic.vcd");
    $dumpvars (0, cic);
    end
    `endif   
    

endmodule