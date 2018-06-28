#
# Remove non-ASCII characters from search strings. If we don't
# do this, there will be problems when loading the data into
# memory, and the encoding used for searching gets more complex.
#
perl -pi -e 's/[^[:ascii:]]//g' ../inputs/search-strings.csv
