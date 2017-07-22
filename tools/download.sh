#!/bin/bash
# HistData.com Downloader

while test $# -gt 0; do
        case "$1" in
                -h|--help)
                        echo "$0 - download data from histdata.com"
                        echo " "
                        echo "$0 [arguments]"
                        echo " "
                        echo "arguments:"
                        echo "-h, --help            show brief help (this)"
                        echo "--symbol=SYMBOL       specify symbol to download"
                        echo "--year=YEAR           the year to download"
                        echo "--month=MONTH         the month to download"
                        exit 0
                        ;;
                --symbol*)
                        export SYMBOL=`echo $1 | sed -e 's/^[^=]*=//g'`
                        shift
                        ;;
                --year*)
                        export YEAR=`echo $1 | sed -e 's/^[^=]*=//g'`
                        shift
                        ;;
                --month*)
                        export MONTH=`echo $1 | sed -e 's/^[^=]*=//g'`
                        shift
                        ;;
                *)
                        break
                        ;;
        esac
done
if [[ -z "$SYMBOL" ]]; then
    echo "Symbol not set"
    exit 1
fi
if [[ -z "$YEAR" ]]; then
    echo "Year not set"
    exit 2
fi

# get token value...
export TK_URL="http://www.histdata.com/download-free-forex-historical-data/?/metastock/1-minute-bar-quotes/${SYMBOL}/${YEAR}"

if [[ -z "$MONTH" ]]; then
    # no month, use the year-based scheme
    export MONTH=""
else
    export MONTH=`printf "%02d\n" ${MONTH}`
    export TK_URL="http://www.histdata.com/download-free-forex-historical-data/?/metastock/1-minute-bar-quotes/${SYMBOL}/${YEAR}/${MONTH}"
fi

export TK=$(curl -s ${TK_URL} | grep "name=\"tk\"" | head -n 1 | sed -e "s/.* value=\"\(.*\)\".*/\1/")

if [[ -z "$TK" ]]; then
    echo "No data for $SYMBOL-$YEAR-$MONTH"
    exit 3
fi

export FILE_PATH="output-$SYMBOL-$YEAR-$MONTH.zip"
export PAYLOAD="tk=$TK&date=$YEAR&datemonth=$YEAR$MONTH&platform=MS&timeframe=M1&fxpair=$SYMBOL"

curl 'http://www.histdata.com/get.php' \
    -H 'Referer: http://www.histdata.com/download-free-forex-historical-data/' \
    -s \
    --data "$PAYLOAD" \
    --compressed > $FILE_PATH

if [[ -s $FILE_PATH ]]; then
    echo "Done!"
    exit 0

else
    echo "Failed to download"
    exit 3
fi
