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

    genvar curr_row, curr_col;
    generate
        for (curr_row = 0; curr_row < ROWS; curr_row++) begin : gen_rows
            for (curr_col = 0; curr_col < COLS; curr_col++) begin : gen_cols
                bit_cell cell (
                    .clk(clk),
                    .rst(rst),
                    .write_enable((row_select == curr_row) & col_write_enable[curr_col]),
                    .data_in(col_data_in[curr_col]),
                    .data_out(total_data_out[curr_row][curr_col])
                );
            end
        end
    endgenerate



