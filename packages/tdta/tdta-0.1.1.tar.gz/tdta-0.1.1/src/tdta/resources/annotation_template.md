---
title: {{annotation.cell_set_accession}}
weight: {{annotation.weight}}
---
## {{annotation.cell_label}} ({{annotation.cell_set_accession}})
{% if 'parents' in annotation %}
<b>Hierarchy: </b>
{% for parent in annotation.parents %}
[{{parent}}](../{{parent|replace(":", "_")}}) >
{% endfor %}
[{{annotation.cell_set_accession}}](../{{annotation.cell_set_accession|replace(":", "_")}})
{% endif %}

**PURL:** [{{metadata.purl_base}}{{annotation.cell_set_accession|replace(":", "_")}}]({{metadata.purl_base}}{{annotation.cell_set_accession|replace(":", "_")}})

---

{% set labelset = metadata.labelsets|selectattr("name", "==", annotation.labelset) | list | first  %}

**Labelset:** {{annotation.labelset}} (Rank: {{labelset.rank}})

{% if 'parent_cell_set_accession' in annotation %}
{% set parent_annotation = metadata.annotations|selectattr("cell_set_accession", "==", annotation.parent_cell_set_accession) | list | first  %}
**Parent Cell Set:** {{parent_annotation.cell_label}} ([{{annotation.parent_cell_set_accession}}](../{{annotation.parent_cell_set_accession|replace(":", "_")}}))
{% else %}
**Parent Cell Set:** -
{% endif %}

{% if 'cell_fullname' in annotation %}
{{annotation.cell_fullname}}
{% endif %}

{% if 'synonyms' in annotation %}
| Synonyms |
|----------|
{% for synonym in annotation.synonyms %}
|{{synonym}}|
{% endfor %}
{% endif %}

**Cell Ontology Term:** {% if 'cell_ontology_term' in annotation %} {{annotation.cell_ontology_term}} ([{{annotation.cell_ontology_term_id}}](https://www.ebi.ac.uk/ols/ontologies/cl/terms?obo_id={{annotation.cell_ontology_term_id}})) {% endif %}

{% if 'rationale' in annotation %}

**Rationale:** {{annotation.rationale}}
{% endif %}
{% if 'rationale_dois' in annotation %}

| Rationale DOIs |
|----------------|
{% for doi in annotation.rationale_dois %}
|[{{doi}}]({{doi}})|
{% endfor %}
{% endif %}

[MARKER GENES.]: #

{% if 'marker_gene_evidence' in annotation %}

| Marker Genes |
|--------------|
{% for gene in annotation.marker_gene_evidence %}
|{{gene}}|
{% endfor %}
{% endif %}

---

[TRANSFERRED ANNOTATIONS.]: #

{% if 'transferred_annotations' in annotation %}

**Transferred annotations:**

| Transferred cell label | Source taxonomy | Source node accession | Algorithm name | Comment |
|------------------------|-----------------|-----------------------|----------------|---------|
{% for at in annotation.transferred_annotations %}
|{{at.transferred_cell_label}}|[{{at.source_taxonomy}}]({{at.purl_base}})|[{{at.source_node_accession}}]({{at.purl_base}}{{at.source_node_accession|replace(":", "_")}})|{{at.algorithm_name}}|{{at.comment}}|
{% endfor %}
{% endif %}

[AUTHOR ANNOTATION FIELDS.]: #

{% if 'author_annotation_fields' in annotation %}

**Author annotation fields:**

| Author annotation | Value |
|-------------------|-------|
{% for key, value in annotation.author_annotation_fields.items() %}
|{{key}}|{{value}}|
{% endfor %}
{% endif %}
