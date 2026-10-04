"""E6: Vista de despliegue de San Camilo en Línea (Python Diagrams).

Requisitos: pip install diagrams  +  Graphviz instalado en el sistema.
Ejecución: python despliegue.py   ->   genera img/despliegue.png junto a este script.
"""
import os

from diagrams import Cluster, Diagram, Edge
from diagrams.generic.device import Mobile
from diagrams.onprem.client import Users
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.network import Internet, Nginx
from diagrams.onprem.queue import Celery
from diagrams.programming.framework import Django

BASE = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(BASE, "img"), exist_ok=True)

graph_attr = {"fontsize": "20", "bgcolor": "white", "pad": "0.3"}

with Diagram(
    "San Camilo en Línea - Vista de despliegue",
    filename=os.path.join(BASE, "img", "despliegue"),
    show=False,
    direction="LR",
    graph_attr=graph_attr,
    outformat="png",
):
    usuarios = Users("Clientes, comerciantes\ny repartidores")
    movil = Mobile("PWA en celular\n(gama baja)")

    with Cluster("Servidor único en la nube"):
        proxy = Nginx("Nginx\n(HTTPS)")
        with Cluster("Monolito modular"):
            app = Django("Aplicación web\n(Catálogo, Pedidos, Pagos,\nNotificaciones, Delivery)")
            worker = Celery("Worker\n(notificaciones con reintento)")
        cola = Redis("Redis\n(cola + caché)")
        db = PostgreSQL("Base de datos\nrelacional")
        with Cluster("Monitoreo"):
            prom = Prometheus("Prometheus")
            graf = Grafana("Grafana")

    yape = Internet("Yape / proveedor de pago\n(servicio externo)")
    wsp = Internet("Servicio de WhatsApp\n(servicio externo)")

    usuarios >> movil >> Edge(label="HTTPS") >> proxy >> Edge(label="solicitudes") >> app
    app >> Edge(label="SQL") >> db
    app >> Edge(label="encola / caché") >> cola >> Edge(label="consume") >> worker
    worker >> Edge(label="confirmación", style="dashed") >> wsp
    app >> Edge(label="cobro", style="dashed") >> yape
    app >> Edge(label="métricas", style="dotted") >> prom >> graf
