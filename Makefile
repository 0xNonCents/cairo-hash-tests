all:
	@echo "Compiling.." 
	@cairo-compile btc_header.cairo --output build/btc_header.json 
	@echo "Running.." 
	@cairo-run --program build/btc_header.json --print_output --layout=all --print_info
run:
	@echo "Running.." 
	@cairo-run --program btc_header.json --print_output --layout=all --print_info

