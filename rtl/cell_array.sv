module cell_array #(
    parameter ROWS = 64,
    parameter COLS = 64,
    parameter DATA_WIDTH = 8
)(
    input wire clk,
    input wire rst,
    input wire[$clog2(ROWS)-1:0] row_select,
    input wire[$clog2(COLS/DATA_WIDTH)-1:0] col_select,
    input wire[DATA_WIDTH-1:0] write_enable,
    input wire[DATA_WIDTH-1:0] data_in,
    output wire[DATA_WIDTH-1:0] data_out
);

    wire [ROWS-1:0][COLS-1:0] total_data_out; //final output of every cell in all ROWS and COLS

    wire [ROWS-1:0] row_decoder;
    genvar r;
    generate
        for(r = 0; r < ROWS; r = r + 1) begin : gen_row_decoder
            assign row_decoder[r] = (row_select == r);
        end
    endgenerate

    localparam NUM_COL_GROUPS = COLS / DATA_WIDTH;
    wire [NUM_COL_GROUPS-1:0] col_decoder;
    genvar c;
    generate
        for(c = 0; c < NUM_COL_GROUPS; c = c + 1) begin : gen_col_decoder
            assign col_decoder[c] = (col_select == c);
        end
    endgenerate

    genvar curr_row;
    genvar curr_col;
    generate
        for (curr_row = 0; curr_row < ROWS; curr_row = curr_row + 1) begin : gen_rows
            for (curr_col = 0; curr_col < COLS; curr_col = curr_col + 1) begin : gen_cols
                localparam COL_GROUP = curr_col / DATA_WIDTH;
                localparam BIT_INDEX = curr_col % DATA_WIDTH;

                bit_cell bit_cell_inst (
                    .clk(clk),
                    .rst(rst),
                    .write_enable(row_decoder[curr_row] & col_decoder[COL_GROUP] & write_enable[BIT_INDEX]),
                    .data_in(data_in[BIT_INDEX]),
                    .data_out(total_data_out[curr_row][curr_col])
                );
            end
        end
    endgenerate

    wire [COLS-1:0] selected_row;
    assign selected_row = total_data_out[row_select];

    reg [DATA_WIDTH-1:0] data_out_mux;
    always @(*) begin
        data_out_mux = selected_row[col_select*DATA_WIDTH +: DATA_WIDTH];
    end
    assign data_out = data_out_mux;
endmodule