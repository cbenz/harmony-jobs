<?xml version="1.0" encoding="UTF-8"?>
<feed xml:lang="fr" xmlns="http://www.w3.org/2005/Atom">
    <id>${feed_url}</id>
    <title>OSM/GIS Harmony - ATOM feed</title>
    <updated>${feed_updated[:-2]+':00'}</updated>
    <link href="${feed_url}" rel="self" />
    <author>
        <name>Easter-eggs.com</name>
        <email>info@easter-eggs.com</email>
        <uri></uri>
    </author>
% for entry in entries:
    <entry>
        <id>${entry['link']}</id>
        <title>${entry['filename']}</title>
        <link rel="alternate" type="text/html" href="${entry['link']}" />
        <published>${entry['upload_at_formated'][:-2]+':00'}</published>
        <updated>${entry['upload_at_formated'][:-2]+':00'}</updated>
        <content type="html"><![CDATA[
        ]]></content>
    </entry>
% endfor
</feed>
