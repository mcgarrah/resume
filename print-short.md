---
layout: print
title: Michael McGarrah - Resume Summary
permalink: /print-short
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

<div class="section">
  <h2>Recent Experience</h2>
  {% assign recent_experiences = site.data.data.experiences.info | slice: 0, 6 %}
  {% for experience in recent_experiences %}
  <div class="item">
    <h4>{{ experience.role }}</h4>
    <div class="meta">{{ experience.company }} | {{ experience.time }}</div>
    <div class="details">
      {{ experience.summary | markdownify }}
    </div>
  </div>
  {% endfor %}
</div>

{% unless site.data.data.sidebar.education %}
  {% include education.html %}
{% endunless %}

{% include skills-short.html %}