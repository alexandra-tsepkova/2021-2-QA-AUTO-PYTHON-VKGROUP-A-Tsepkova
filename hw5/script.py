f = open("access.log", "r")
lines = f.readlines()
res = open("result_py.txt", "w")


res.write(" ".join(("Amount of queries:", str(len(lines)))) + "\n")
methods = {'GET': 0, 'HEAD': 0, 'POST': 0, 'PUT': 0, 'PATCH': 0,
           'DELETE': 0, 'CONNECT': 0, 'OPTIONS': 0, 'TRACE': 0}
for m, v in methods.items():
    for string in lines:
        if '"' + m in string:
            methods[m] += 1
for m, v in methods.items():
    res.write(f"{m} - {v}\n")

times_visited_urls = {}
for line in lines:
    url = line.split()[6]
    if url in times_visited_urls.keys():
        times_visited_urls[url] += 1
    else:
        times_visited_urls[url] = 1
res.write("Most visited urls:" + "\n" + "url       times\n")
res.write("\n".join(map(str, sorted(times_visited_urls.items(), key=lambda x: x[1], reverse=True)[:10])) + "\n")


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
res.write("\n".join(map(str, sorted(queries, key=lambda x: int(x.split()[-1]), reverse=True)[:5])) + "\n")
res.write("Top queries with status code 5xx by users" + "\n" + "ip         times\n")
res.write("\n".join(map(str, sorted(queries_5xx.items(), key=lambda x: x[1], reverse=True)[:5])) + "\n")
