module bit_cell (
    input wire clk,
    input wire rst,
    input wire write_enable,
    input wire data_in,
    output reg data_out
);
    always @(posedge clk or posedge rst) begin
        if (rst) begin
            data_out <= 1'b0;
        end
        else if (write_enable) begin
            data_out <= data_in;
        end
    end
endmodule