f = open("access.log", "r")
lines = f.readlines()
res = open("result_py.txt", "w")


res.write(" ".join(("Amount of queries:\n", str(len(lines)))) + "\n\n")

methods = {}
for line in lines:
    method = line.split()[5].lstrip('"')
    if method in methods.keys():
        methods[method] += 1
    elif len(method) < 100:
        methods[method] = 1
res.write("Count requests per methods:\n")
for m, v in methods.items():
    res.write("{: >6}  {}\n".format(v, m))
res.write("\n")

times_visited_urls = {}
for line in lines:
    url = line.split()[6]
    if url in times_visited_urls.keys():
        times_visited_urls[url] += 1
    else:
        times_visited_urls[url] = 1
res.write("Most visited urls:" + "\n" + "url       times\n")
res.write("\n".join(map(str, sorted(times_visited_urls.items(), key=lambda x: x[1], reverse=True)[:10])) + "\n\n")


queries = []
queries_5xx = {}
for line in lines:
    status_code = line.split()[8]
    ip = line.split()[0]
    url = line.split()[6]
    size = line.split()[9]
    if int(status_code) // 100 == 4:
        queries.append(ip + " " + url + " " + status_code + " " + size)
    elif int(status_code) // 100 == 5:
        if ip in queries_5xx.keys():
            queries_5xx[ip] +=1
        else:
            queries_5xx[ip] = 1

res.write("Biggest queries with status code 4xx" + "\n" +
          "ip        url         status code        size\n")
res.write("\n".join(map(str, sorted(queries, key=lambda x: int(x.split()[-1]), reverse=True)[:5])) + "\n\n")
res.write("Top queries with status code 5xx by users" + "\n" + "ip         times\n")
res.write("\n".join(map(str, sorted(queries_5xx.items(), key=lambda x: x[1], reverse=True)[:5])) + "\n")
