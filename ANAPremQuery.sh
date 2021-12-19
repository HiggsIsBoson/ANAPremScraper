months=(1 2 3)
destinations=(naha sapporo fukuoka yamaguchi komatsu tsushima)

query_month(){

    for month in ${months[@]}; do
	for dest in ${destinations[@]}; do
	    python ANAPremQuery.py -y 2022 -m ${month} -O haneda -D ${dest} &
	    python ANAPremQuery.py -y 2022 -m ${month} -O ${dest} -D haneda &
	done
    done
}

dump_result(){
    for dest in ${destinations[@]}; do
	. dump_rawqueries.sh haneda ${dest}
    done
}

query_month
#dump_result
