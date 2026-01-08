module cell_array #(
    parameter ROWS = 64, 
    parameter COLS = 64
)(
    input wire clk,
    input wire rst,                        
    input wire[$clog2(ROWS)-1:0] row_select,
    input wire[COLS-1:0] col_write_enable,
    input wire[COLS-1:0] col_data_in,
    output wire[COLS-1:0] col_data_out  //represents the final output of each bit in a specified column.
);

    wire [ROWS-1:0][COLS-1:0] total_data_out; //final output of every cell in all ROWS and COLS

    wire [ROWS-1:0] row_decoder;
    genvar r;
    generate
        for(r = 0; r < ROWS; r = r + 1) begin : gen_decoder
            assign row_decoder[r] = (row_select == r);
        end
    endgenerate

    genvar curr_row;
    genvar curr_col;
    generate
        for (curr_row = 0; curr_row < ROWS; curr_row = curr_row + 1) begin : gen_rows
            for (curr_col = 0; curr_col < COLS; curr_col = curr_col + 1) begin : gen_cols
                bit_cell bit_cell_inst (
                    .clk(clk),
                    .rst(rst),
                    .write_enable(row_decoder[curr_row] & col_write_enable[curr_col]),
                    .data_in(col_data_in[curr_col]),
                    .data_out(total_data_out[curr_row][curr_col])
                );
            end
        end
    endgenerate

    assign col_data_out = total_data_out[row_select];
endmodule