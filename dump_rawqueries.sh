origin=$1
dest=$2

echo "dump_rawqueries.sh  INFO  origin: ${origin}"
echo "dump_rawqueries.sh  INFO    dest:   ${dest}"

for file in `ls output/*${origin}_${dest}*.html | grep -v event.html`; do

    date_file=`echo ${file} | rev | cut -d "_" -f 1 | rev | cut -d "." -f 1`
    outFileName=`echo ${file} | sed -e "s#.html#_event.html#g"`

    echo "dump_rawqueries.sh  INFO  Dumping $file... Output: ${outFileName}"

    
    for line in `cat ${file}  | grep selectedDateValue | head -n 1`; do echo $line; done > log
    date=`cat log | grep ^value | grep "202" | cut -d "=" -f 2 | tr -d "\""`
    rm -f log

    if [ "${date_file}" != "${date}" ]; then
	echo "dump_rawqueries.sh  ERROR  The file ${file} seems to contain a wrong timestamp in the body (${date})! Something's wrong. Please check."
    fi

    cat $file | grep "availabilityResultFlightTime" > ${outFileName}
    
done

python parse_html.py -O ${origin} -D ${dest}
