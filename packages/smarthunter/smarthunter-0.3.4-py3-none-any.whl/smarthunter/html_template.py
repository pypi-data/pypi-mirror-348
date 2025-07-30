from jinja2 import Template

HTML_TEMPLATE = Template(r"""
<!DOCTYPE html><html lang=en><meta charset=utf-8>
<title>{{ name }} strings</title>
<style>
body{font-family:ui-monospace,monospace;background:#111;color:#ddd;padding:1rem;font-size:15px}
h1{color:#69f;margin:0 0 .5em}.score{color:#8f8}.flag{color:#ffa}.url{color:#99f}
.email{color:#9f9}.ip{color:#9ff}.hash{color:#fc9}.secret{color:#f99}.encoded{color:#c9f}
details{margin-left:1.3em}.gray{color:#666}
.tooltip{position:relative;display:inline-block;border-bottom:1px dotted #ccc;cursor:help}
.tooltip .tooltiptext{visibility:hidden;width:220px;background:#333;color:#fff;border-radius:6px;
padding:5px;position:absolute;z-index:1;bottom:125%;left:50%;margin-left:-110px;opacity:0;
transition:opacity .3s}.tooltip:hover .tooltiptext{visibility:visible;opacity:1}
</style>
<h1>{{ name }} – Smart-Strings report</h1>
<p>{{ total }} raw strings → {{ clusters|length }} clusters. Generated {{ ts }} UTC.</p>
{% for c in clusters %}
<div>
  <span class=score>[{{ c.score }}]</span>
  <span class="tooltip
        {{ 'flag' if c.flag else '' }}
        {{ 'url' if c.url else '' }}
        {{ 'email' if c.email else '' }}
        {{ 'ip' if c.ip else '' }}
        {{ 'hash' if c.hash else '' }}
        {{ 'secret' if c.secret else '' }}
        {{ 'encoded' if c.rep.startswith('[') else '' }}">
    {{ c.rep|e }}
    <span class=tooltiptext>
      {% if c.details.patterns %}Matches: {{ c.details.patterns|join(', ') }}<br>{% endif %}
      Entropy {{ c.details.entropy }} | Len {{ c.details.length }} | Rarity {{ c.details.rarity }}
    </span>
  </span>
  {% if c.dup %}<details class=gray><summary>{{ c.dup|length }} more</summary>
  {% for d in c.dup %}<div class=gray>{{ d|e }}</div>{% endfor %}</details>{% endif %}
</div>{% endfor %}""") 