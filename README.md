# CTI League: MISP Slack Bots

Slack bots that add MISP objects to MISP events.

Based on prior work of [Emilio Escobar](https://twitter.com/eaescob?lang=enr)
and his `flask-sigauth` library.

Commands:
```bash
# Create a Twitter post microblog object
/misp_twitter <misp event id> <twitter status id or status url>

# Scrape BuiltWith tracking-ids from site.
/misp_builtwith <misp event id> <domain or url>
```

