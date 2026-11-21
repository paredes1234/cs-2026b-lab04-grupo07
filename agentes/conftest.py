# Las copias del sandbox (agentes/ejecuciones/) repiten los nombres de tests/: pytest no debe recolectarlas.
collect_ignore_glob = ["ejecuciones/*"]
