---
layout: print
title: Michael McGarrah - Complete Resume
permalink: /print-long
docx: true
pdf: true
---

{% include contact-print.html %}

<div class="sidebar-inline">
  {% assign languages = site.data.data.sidebar.languages %}
  {% if languages %}
  <div class="sidebar-section">
    <h3>{{ languages.title }}</h3>
    <ul>
      {% for language in languages.info %}
      <li>{{ language.idiom }} ({{ language.level }})</li>
      {% endfor %}
    </ul>
  </div>
  {% endif %}
  
  {% assign interests = site.data.data.sidebar.interests %}
  {% if interests %}
  <div class="sidebar-section">
    <h3>{{ interests.title }}</h3>
    <ul>
      {% for interest in interests.info %}
      <li>{{ interest.item }}</li>
      {% endfor %}
    </ul>
  </div>
  {% endif %}
</div>

{% include career-profile.html %}

{% unless site.data.data.sidebar.education %}
  {% include education.html %}
{% endunless %}

{% include experiences-print.html %}

{% include certifications.html %}

{% include projects.html %}

{% include oss-contributions.html %}

{% include publications.html %}

{% include skills.html %}