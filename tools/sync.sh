#!/bin/bash
# Downloads all forex data from histdata.com

# ANSI Formatting
BLD='\033[0;1m'
RED='\033[0;31m'
GRN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# RAW data path
YEAR_PATH="../data/1m/year"
MONTH_PATH="../data/1m/month"
mkdir -p $YEAR_PATH $MONTH_PATH

echo "Retrieving symbols"
export ALL_SYMBOLS=$(`pwd`/symbols.sh)
printf "${BLD}`wc -w <<< $ALL_SYMBOLS`${NC} symbols found\n"

# override w/ specific symbols to retrieve
#ALL_SYMBOLS=(USDJPY)

echo "Downloading missing data"

# TODO parallelize!
for s in $ALL_SYMBOLS; do
    for y in `seq 1999 $(date +%Y)`; do
    	if [ $y == $(date +%Y) ]; then
    		# download each month
    		for m in `seq 1 $(date +%m)`; do
    			FILE="$MONTH_PATH/${s}_${y}`printf "%02d\n" ${m}`.csv"

    			# always retrieve the current month
    			if [[ "$m" -eq $(date +%m | sed 's/^0*//') ]]; then
    				rm -f $FILE
    			fi

    			if [[ -s $FILE ]]; then
		    		printf "${RED}File $FILE exists${NC}, skipping...\n"

		    	else
            printf "Retrieving ${BLUE}$s-$y-$m${NC}\n"
        		./download.sh --symbol="$s" --year="$y" --month="$m"
    			fi
    		done

      else
      	# download a single year
	      FILE="$YEAR_PATH/${s}_${y}.csv"
	      if [[ -a $FILE ]]; then
	      	printf "${RED}File $FILE exists${NC}, skipping...\n"

	      else
            printf "Retrieving ${BLUE}$s-$y${NC}\n"
	        	./download.sh --symbol="$s" --year="$y"
	        	EXIT_CODE=$?
	        	if [ $EXIT_CODE == 3 ]; then
	        		touch $FILE
	        		printf "${RED}Generating empty($FILE)${NC}\n"
	        	fi
      	fi
    	fi
    done
done

printf "${BLD}Download complete${NC}, inflating all targets\n"

inflate_and_clean(){
  tgt_path=$1

  # Unzip everything
  unzip -qq -u \*.zip 2> /dev/null

  # delete zip files
  rm -rf *.zip 2> /dev/null

  # delete gap files
  # TODO incoropate this in output
  rm -rf *.txt  2> /dev/null

  # change names using sed
  for file in *.csv; do mv $file $(echo $file | sed -e 's/^DAT_MS_//') 2> /dev/null; done
  for file in *.csv; do mv $file $(echo $file | sed -e 's/_M1_/_/')    2> /dev/null; done

  # move data we care about
  mv -f *.csv $tgt_path 2> /dev/null
}

cd year/
inflate_and_clean "../$YEAR_PATH"

cd ../month/
inflate_and_clean "../$MONTH_PATH"

cd ..

# Fin!
printf "\n${GRN}FIN!${NC}\n"
