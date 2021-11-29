# Total request count
echo "Amount of queries"
cat access.log | grep -E '^.*$' -c

echo ''

# Total request per method
echo "Count requests per methods"
cat access.log | awk '{sub(/^\"/, "", $6); print $6}' | sort | uniq -c | awk 'length ($2) < 30'

echo ''

# Top 10 most frequently requested urls
echo "Ten most frequently requested urls"
echo "count          url"
cat access.log | awk '{print $7}' | sort | uniq -c | sort -k 1 -g -r | head

echo ''

# Top 5 4XX errors by response size
echo "5 4xx errors by response size"
echo "url        status code         size         ip"
cat access.log | grep -E '^.*" 4[0-9][0-9] .*$' | awk 'BEGIN{OFS=" "} {print $10,$1,$7,$9}' | sort -r -k 1 -g | awk 'BEGIN{OFS=" "} {print $3,$4,$1,$2}' | head -n 5

echo ''

# Top 5 5XX errors by ip
echo "top 5 5XX errors by ip"
echo "count           ip          status code"
cat access.log | awk 'BEGIN{OFS=" "} {print $1,$9}' | grep -E ' 5[0-9][0-9]$' | sort | uniq -c | sort -k 1 -g -r | head -n 5
