for month in 1; do
    for dest in naha sapporo fukuoka yamaguchi komatsu tsushima; do
	python ANAPremQuery.py -y 2022 -m ${month} -O haneda -D ${dest} &
	python ANAPremQuery.py -y 2022 -m ${month} -O ${dest} -D haneda &
    done
done
