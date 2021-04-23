plot: netspace.tsv
	gnuplot -c netspace.plot -p

netspace.tsv: netspace.json json_to_tsv.py
	./json_to_tsv.py <netspace.json >netspace.tsv

test:
	python3 -m unittest discover .

