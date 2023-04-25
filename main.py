#!/usr/bin/env python3

# Read list of URLs from file
with open("sitelist.raw", "r") as f:
    urls = [url.strip() for url in f.readlines()]

# Remove duplicate lines
unique_urls = list(set(urls))

# Remove any trailing slashes
unique_urls = [url[:-1] if url.endswith('/') else url for url in unique_urls]

# Do the actual work (modified to use unique_urls and use tabs instead of 4x spaces, and to write to file)
base = unique_urls[0]
qtabdepth = 0
ptabdepth = 0
ttabdepth = 0
plen = len(base.split('?'))
qlen = len(base.split('&'))
tlen = len(base.split('/'))

final_urls = []
for url in unique_urls[1:]:
    if '&' in url:
        q = url.split('&')
        lq = len(q)
        if lq != qlen:
            qtabdepth += 1 if lq > qlen else -1
            qlen = lq
        temp_urls = ['?' + q[-1]]
        pad = '\t' * (qtabdepth + ttabdepth)
        final_urls.append(pad + ''.join(temp_urls))
    elif '?' in url:
        p = url.split('?')
        lp = len(p)
        if lp != plen:
            ptabdepth += 1 if lp > plen else -(plen - lp)
            plen = lp
        temp_urls = ['?' + p[-1]]
        pad = '\t' * (ptabdepth + ttabdepth)
        final_urls.append(pad + ''.join(temp_urls))
    else:
        t = url.split('/')
        lt = len(t)
        if lt != tlen:
            ttabdepth += 1 if lt > tlen else -(tlen - lt)
            tlen = lt
        temp_urls = ['/' + t[-1]]
        pad = '\t' * ttabdepth
        final_urls.append(pad + ''.join(temp_urls))

with open("sitelist.new", "wt") as f:
    f.write(base + "\n")
    f.write('\n'.join(final_urls) + "\n")
