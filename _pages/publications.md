---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
---

{% if author.googlescholar %}
  You can also find my articles on <u><a href="{{author.googlescholar}}">my Google Scholar profile</a>.</u>
{% endif %}

{% include base_path %}

{% assign sorted_pubs = site.publications | sort: 'date' | reverse %}
{% assign preprints = sorted_pubs | where: 'pubtype', 'preprint' %}
{% assign papers = sorted_pubs | where_exp: 'p', "p.pubtype != 'preprint'" %}

{% if preprints.size > 0 %}
<h2 id="preprints">Preprints</h2>
{% for post in preprints %}
  {% include archive-single.html %}
{% endfor %}
{% endif %}

<h2 id="published">Published papers</h2>
{% for post in papers %}
  {% include archive-single.html %}
{% endfor %}
