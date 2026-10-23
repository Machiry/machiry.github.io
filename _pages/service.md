---
permalink: /service/
title: "Service"
author_profile: true
---

I recognize the importance of giving back and encourage everyone to serve the academic community.

I strive my best to do it, and the following are a few instances:

## Technical Program Committee

> Reviewing and providing feedback on submitted papers.

{% for v in site.data.service.program_committees %}{{ v.name }} ({{ v.years | join: ", " }}){% unless forloop.last %}, {% endunless %}{% endfor %}

## Chair

> Organizing (Reviews, Arranging Program, Funding, etc)

{% for c in site.data.service.chairs %}
* {{ c.name }} ({{ c.years | join: ", " }})
{%- endfor %}

## University Service

> Discussion and reviewing various department-level proposals

### Purdue University (ECE Department)

* Undergraduate Curriculum Committee (Fall 2022 - Present).


