
rule rotate:
  input:
    "<input_loc>/{sample}.json"
  output:
    "<output_loc>/{sample}/rotate/out.json"
  log:
    "<output_loc>/{sample}/rotate/out.log"
  shell:
    "uv run polymap make rotate {input} {output} 2>{log}"


rule ortho:
  input:
    "<output_loc>/{sample}/rotate/out.json"
  output:
    "<output_loc>/{sample}/ortho/out.json"
  log:
    "<output_loc>/{sample}/ortho/out.log"
  shell:
    "uv run polymap make ortho {input} {output} 2>{log}"


rule simplify:
  input:
    "<output_loc>/{sample}/ortho/out.json"
  output:
    "<output_loc>/{sample}/simplify/out.json"
  log:
    "<output_loc>/{sample}/simplify/out.log"
  shell:
    "uv run polymap make simplify {input} {output} 2>{log}"


rule xplan:
  input:
    "<output_loc>/{sample}/simplify/out.json"
  params:
    ax="X"
  output:
    "<output_loc>/{sample}/xplan/out.json"
  log:
    "<output_loc>/{sample}/xplan/out.log"
  shell:
    "uv run polymap make plan {params.ax} {input} {output} 2>{log}"

rule xmove:
  input:
    "<output_loc>/{sample}/xplan/out.json"
  params:
    ax="X"
  output:
    "<output_loc>/{sample}/xmove/out.json"
  log:
    "<output_loc>/{sample}/xmove/out.log"
  shell:
    "uv run polymap make move {params.ax} {input} {output} 2>{log}"




rule yplan:
  input:
    "<output_loc>/{sample}/xmove/out.json"
  params:
    ax="Y"
  output:
    "<output_loc>/{sample}/yplan/out.json"
  log:
    "<output_loc>/{sample}/yplan/out.log"
  shell:
    "uv run polymap make plan {params.ax} {input} {output} 2>{log}"

rule ymove:
  input:
    "<output_loc>/{sample}/yplan/out.json"
  params:
    ax="Y"
  output:
    "<output_loc>/{sample}/ymove/out.json"
  log:
    "<output_loc>/{sample}/ymove/out.log"
  shell:
    "uv run polymap make move {params.ax} {input} {output} 2>{log}"

