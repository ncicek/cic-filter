module integrator (
    i_clk,
    i_data,
    i_ready,
    o_data,
    o_ready
    );

    parameter IW=2, OW=5, M=5;

    input wire i_clk;
    input wire i_ready;
    input wire signed [(IW-1):0] i_data;
    output wire signed [(OW-1):0] o_data;
    output reg o_ready = 1'b0;
    integer i;

    reg signed [(OW-1):0] accumulator = {OW{1'b0}};
    //sign_extend = {(OW-IW){delay_line[0][IW-1]}, delay_line[0]}
    assign o_data = {{(OW-IW){i_data[IW-1]}}, i_data} + accumulator;

    always @(posedge i_clk) begin
        if (i_ready) begin
            accumulator <= o_data;
            o_ready <= 1'b1;
        end else begin
            o_ready <= 1'b0;
        end
    end 


endmodule