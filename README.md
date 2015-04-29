# YAPDNS


## Passive DNS

A passive DNS is a sensor that extracts data from DNS queries and responses and forwards them to a central database which processes and stores it. Passive DNS data is extremely useful to understand the historical evolution of a DNS entry and, more in general, the associations between IP addresses and DNS names. This kind of information comes pretty handy when dealing with malicious activities such as Command & Control Servers, Exploit Kits and so on, as it can help you find clusters between different incidents. Some examples:
* What are all the IP addresses that have been associated to a particular DNS name?
* What are all the DNS names associated to a given IP address?
Is this domain being resolved in different ways depending on the client’s geolocation? (e.g. is this domain a CDN?)
Does this domain have a Fast Flux behavior?


## Existing implementations

The most famous passive DNS system is probably DNSDB, initiated by the Internet Systems Consortium (ISC) and then acquired by Farsight Security. Farsight Security is a commercial entity but is committed to share security-related telemetry data with security industry partners and academic researchers at nominal or non-discriminatory subscription rates.
VirusTotal also has its own passive DNS system, which is free for non-commercial use. However, if I don’t get it wrong, this database is mostly based on data extracted from VirusTotal’s own activities (e.g. queries performed by their sandboxes while analyzing submitted samples, etc.) and, as such, is not aimed at being a complete passive DNS database, but rather a directory of known malicious domains.
Other similar databases exist, but they are either non-free or not complete enough.


## Passive DNS data is everywhere

The concept behind YAPDNS is that you don’t actually need to analyze direct DNS queries and responses to get passive DNS data. Extracting this piece of information from other sources is often more than enough.
Want an example? Well, suppose you are using a SIEM (e.g. Splunk, ELKS or ELSA) to collect logs from your company’s proxy server. Those logs almost always contain an association between an IP address (the destination IP) and a domain name (the web site’s name). In this case, you can safely assume that any domain associated to a IPv4 address corresponds to a “A” record on the DNS, while a domain to IPv6 association should correspond to a “AAAA” record.
Now, suppose you’re also collecting logs from your company’s mail server: again, if you see an outgoing SMTP flux to a certain IP address, you can assume that a “MX” record exists that associates that IP address with the mail recipient’s domain name.
You could point out that it would be much simpler (and probaby more accurate) to point your DNS server’s logs to the same SIEM and use direct DNS data to build your database. That’s correct, of course, but there are a number of times when you simply can’t access the DNS server’s logs and/or those logs aren’t complete enough.
But, of course, there’s much more than that. Assume you are collecting data from both direct and indirect sources. Assume you’ve built a huge database with that data. Think about your own web site’s domain name: you know it’s a “static” A record; you know it’s being resolved to the same IP address in all the world (regardless to where a client comes from) and you haven’t changed it in a while. Of course, direct DNS entries (e.g. direct monitoring of DNS query logs) can confirm this. Now, assume one of your passive sensors collecting indirect DNS data from a proxy’s logs is seeing your domain name associated to a completely different IP address: that’s an anomaly that could mean that the client’s hosts file was altered, or that it’s using a DNS service that is serving an altered record. When analyzing security-related data, this kind of information is extremely important.


## YAPDNS

Our idea about YAPDNS’s architecture is that of having multiple connectors that should be able to extract the relevant data (basically: IP address, domain name and timestamp – and hopefully record type like A, AAAA, MX etc) from various sources. Then, this data should be forwarded to a YAPDNS Server that should process and store it for further reference. On top of that, a Web GUI (hopefully based on Django) and a set of APIs (hopefully made with TastyPie) should make that data available to humans and to other tools.
YAPDNS should also be integrated with HPFriends, which is a tool developed by The Honeynet Project to allow different individuals and groups to share the data they collect with their analysis systems.


## Connectors

Simply said, connectors should be able to collect passive DNS data from as many sources as possible. For example, think about a host running syslog-ng to receive logs from a web proxy. Syslog-ng lets you define a set of parsers (see PatternDB) to be applied to incoming logs; then you can pass those already parsed logs to an external script that would be our connector. This connector takes the relevant data out of the parsed log and sends it to the central processing component.
Another connector could run as a scheduled job (e.g. from crontab) to periodically retrieve logs from SIEMs like Splunk or ELK Stack or even ELSA, extract the relevant info from those logs and then sends them to the processing component.
Of course, connectors should also exists for direct DNS data such as DNS logs, Bro IDS‘s logs, and it should be possible to distinguish between direct and indirect data.


## YAPDNS Server

The central processing component would essentially take the input data – that has already been normalized by the connectors – and store it to a database. Data should also be enriched with metadata, such as suspicious behaviours detected by some specific rules, e.g.:
if a domain is associated to a lot of different IP addresses that change every few seconds, then it may be a fast flux domain;
if the same domain is resolved with different IP addresses based on the geolocation of the client making the query, then it could be a CDN;
Another kind of metadata that could be associated with DNS entries is WHOIS information for both IP addresses and domains.
The YAPDNS server should also be able to forward the collected information, along with any other useful metadata, to external systems such as HPFriends. Communication with other projects and software may use the Common Output Format proposed by this draft on IETF.


## Web GUI

The centralized GUI would be a Django app with user authentication; the HTML/JavaScript part could be made with Bootstrap, jQuery and other similar de-facto standards to keep things nice and simple. It would let you search the data performing tasks such as:
find the history of all IP addresses associated with domain aaa.bbb.com
find the history of all domains associated with IP address X.Y.Z.W


## Conclusions

If you feel like getting involved in YAPDNS’s development, either as a GSoC student or as a contributor, you should make yourself familiar with those concepts:
* Passive DNS systems (general concepts and existing implementations)
* Syslog-ng and PatternDB
* SIEMs (Splunk, ELKs, ELSA, etc)
* Python, Django, TastyPie, Bootstrap, jQuery: that’s what most of the project will be made with

Should you have any questions, please feel free to subscribe to the Honeynet Project’s GSoC mailing list, or ping us via Twitter: @PietroDelsante and @a_de_pasquale.
