for file in `ls output/*.html`; do
    echo $file
    date_file=`echo ${file} | rev | cut -d "_" -f 1 | rev | cut -d "." -f 1`
    
    for line in `cat ${file}  | grep selectedDateValue | head -n 1`; do echo $line; done > log
    date=`cat log | grep ^value | grep "202" | cut -d "=" -f 2 | tr -d "\""`
    rm -f log
    
    if [ "${date_file}" != "${date}" ]; then
	echo "The file seems to have wrong timestamp on its name!"
	newFileName=`echo ${file} | sed -e "s#${date_file}#${date}#g"`.renamed
	echo "To be rename to ${newFileName}..."
	mv ${file} ${newFileName}	
    fi
    
done
