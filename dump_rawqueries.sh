for file in `ls output/*.html`; do

    date_file=`echo ${file} | rev | cut -d "_" -f 1 | rev | cut -d "." -f 1`
    
    for line in `cat ${file}  | grep selectedDateValue | head -n 1`; do echo $line; done > log
    date=`cat log | grep ^value | grep "202" | cut -d "=" -f 2 | tr -d "\""`
    rm -f log

    echo $file $date

    if [ "${date_file}" != "${date}" ]; then
	echo "The file seems to have wrong timestamp on its name! Something's wrong. Please check. Abort."
    fi

    outFileName=`echo ${file} | sed -e "s#.html#_event.html#g"`
    echo $outFileName
    cat $file | grep "availabilityResultFlightTime" > ${outFileName}
    
done
