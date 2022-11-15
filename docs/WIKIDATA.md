## Wikidata and friends

### Wikidata

The [Wikidata project](https://www.wikidata.org/) is an open
knowledge base of "things". The  QID (or Q number) is the unique
identifier of a data item on Wikidata, comprising the letter "Q"
followed by one or more digits. It is used to help people and
machines understand the difference between items with the same
or similar names.

A number of open data projects use Wikidata codes to augment
their data. So do we. Nearly all companies and brands of a certain
size have a Wikidata entry. Some examples include:
[Starbucks](https://www.wikidata.org/wiki/Q37158),
[McDonald’s](https://www.wikidata.org/wiki/Q38076),
[Travelodge](https://www.wikidata.org/wiki/Q7836087) and
[Travelodge](https://www.wikidata.org/wiki/Q9361374).
The latter two examples illustrating rather well
the name disambiguation.

If possible please apply a Wikidata QID to the POIs generated
by your spider. The simplest way is to add it to the
`item_attributes` field of the spider for it to be automatically
applied by [pipeline code](../locations/pipelines.py). For example:

```python
import scrapy

class TravelodgeGBSpider(scrapy.Spider):
    name = "travelodge_gb"
    item_attributes = {"brand": "Travelodge UK", "brand_wikidata": "Q9361374"}
```

Many of the companies that we write spiders for will be significant
enough to have been added to the
[Name Suggestion Index (NSI)](https://nsi.guide/?t=brands)
project (see below). We provide a custom `scrapy nsi` command for
doing name queries against the NSI dataset e.g.

```
$ pipenv run scrapy nsi --name travelodge
"Travelodge UK", "Q9361374"
       -> https://www.wikidata.org/wiki/Q9361374
       -> https://www.wikidata.org/wiki/Special:EntityData/Q9361374.json
       -> British budget hotel chain
       -> https://www.travelodge.co.uk/
       -> item_attributes = {"brand": "Travelodge UK", "brand_wikidata": "Q9361374"}
"Travelodge", "Q7836087"
       -> https://www.wikidata.org/wiki/Q7836087
       -> https://www.wikidata.org/wiki/Special:EntityData/Q7836087.json
       -> midscale hotel chain run by Wyndham Hotels & Resorts
       -> https://www.wyndhamhotels.com/travelodge
       -> item_attributes = {"brand": "Travelodge", "brand_wikidata": "Q7836087"}
```

Note the Python code fragments generated for you to copy and
paste into your spider as a convenience. If the NSI query does
not give you what  you want immediately then you may need to
dig deeper, perhaps  going directly to the
[Wikidata search page](https://www.wikidata.org/).

### Name Suggestion Index (NSI)

The NSI is essentially a well curated subset of
Wikidata brand and company QIDs. The main goal of the project is to aid
[OpenStreetMap](https://www.openstreetmap.org/)
editing of POIs by allowing easy import of common data. This
is well described in a
[video of a presentation](https://2019.stateofthemap.us/program/sat/mapping-brands-with-the-name-suggestion-index.html)
given at OSM State of the Map 2019.

The success of the NSI can be gauged from the rapid increase in the number
of OSM elements with Wikidata codes
[over the previous few years](https://taginfo.openstreetmap.org/keys/brand%3Awikidata#chronology).

Running our custom `scrapy nsi` command, but this time with a direct QID parameter
specified, yields the NSI tag suggestions for the QID. This is the bottom line
of the output below:

```
$ pipenv run scrapy nsi --code Q9361374
"Travelodge UK", "Q9361374"
       -> https://www.wikidata.org/wiki/Q9361374
       -> https://www.wikidata.org/wiki/Special:EntityData/Q9361374.json
       -> British budget hotel chain
       -> https://www.travelodge.co.uk/
       -> item_attributes = {"brand": "Travelodge UK", "brand_wikidata": "Q9361374"}
       -> {'displayName': 'Travelodge (Europe)', 'id': 'travelodge-dec11e', 'locationSet': {'include': ['es', 'gb', 'ie']}, 'tags': {'brand': 'Travelodge', 'brand:wikidata': 'Q9361374', 'internet_access': 'wlan', 'internet_access:fee': 'customers', 'internet_access:ssid': 'Travelodge WiFi', 'name': 'Travelodge', 'tourism': 'hotel'}}
```

Note the OSM POI category attributes for a hotel (`'tourism': 'hotel'`) are part
of the tag set that the NSI is "suggesting" in this case.

### Automatic POI categorisation

The [ATP item pipeline](../locations/pipelines.py)
will attempt to enhance POIs it sees automatically with OSM category
data from the NSI. It only does this if there is a non-ambiguous match
of QID, country location (if appropriate) and category suggestion.

In the great majority cases the automation gets the correct answer.
In the cases where it fails for some reason then the automation can be disabled
for the spider, and the correct categories applied in the spider
code itself.

### A virtuous circle?

Wikidata, NSI, OSM and ATP support each other with respect to data integrity
and consistency. Eyeballs in one project are able to pick up problems in
another.

Providing that a site does a good job of publishing its data and
providing the ATP spider does a good job of reading it, then a range
of possibilities open up.

For example, it is far easier to support editors making a change to
a POI from being non-branded (no QID) to one that is when we can point
to the co-located scraped POI. If there is good branded data in OSM
then it is easier to suggest change or removal based on changes in
the branded / scraped data set.

Currently, after each weekly run of the full project, [we publish a cross
correlation (by QID) of the data in ATP, NSI and OSM](https://www.alltheplaces.xyz/wikidata.html).
This is able to pick up various anomalies between and within the various
projects all leading to edits which can make the open data world a better place.

Others do [similar and interesting things](https://osm.mathmos.net/chains/).