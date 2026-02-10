module memory_banks #(
    parameter NUM_BANKS = 4,
    parameter ROWS = 64,
    parameter COLS = 64,
    parameter DATA_WIDTH = 8
)(
    input wire clk,
    input wire rst,
    input wire [$clog2(ROWS)-1:0] row_select,
    input wire [$clog2(COLS/DATA_WIDTH)-1:0] col_select,
    input wire [$clog2(NUM_BANKS)-1:0] bank_select,
    input wire [DATA_WIDTH-1:0] write_enable,
    input wire [DATA_WIDTH-1:0] data_in,
    output wire [DATA_WIDTH-1:0] data_out
);
    wire [DATA_WIDTH-1:0] bank_data_out [NUM_BANKS-1:0];
    wire [NUM_BANKS-1:0] bank_write_enable;

    genvar b;
    generate
        for (curr_bank = 0; curr_bank < NUM_BANKS; curr_bank = curr_bank + 1) begin : gen_banks
            assign bank_write_en[b] = (bank_select == b);
            cell_array #(
                .ROWS(ROWS),
                .COLS(COLS),
                .DATA_WIDTH(DATA_WIDTH)
            ) bank_inst (
                .clk(clk),
                .rsk(rst),
                .row_select(row_select),
                .col_select(col_select),
                .write_enable(bank_write_en[b] ? write_enable : {DATA_WIDTH{1'b0}}),
                .data_in(data_in),
                .data_out(bank_data_out[b])
            );
        end
    endgenerate
    assign data_out = bank_data_out[bank_select];
endmodule
