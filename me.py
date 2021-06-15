#!/usr/bin/env python3

import asyncio
import logging
import sys
from ipaddress import IPv4Address, IPv6Address, ip_address
from time import time
from typing import Any, NamedTuple, Union

import click
from aioprometheus import Gauge, Service


IPAddress = Union[IPv4Address, IPv6Address]
LOG = logging.getLogger(__name__)


class MifiStats(NamedTuple):
    http_responding: int
    http_response_time: float
    http_status_code: int


def _handle_debug(
    ctx: click.core.Context,
    param: Union[click.core.Option, click.core.Parameter],
    debug: Union[bool, int, str],
) -> Union[bool, int, str]:
    """Turn on debugging if asked otherwise INFO default"""
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        format="[%(asctime)s] %(levelname)s: %(message)s (%(filename)s:%(lineno)d)",
        level=log_level,
    )
    return debug


async def check_http_endpoint(url: str) -> MifiStats:
    # start_time = time()
    return MifiStats(1, 69, 200)


async def update_prom_stats(
    interval: float, prom_service: Service, mifi_ip: IPAddress
) -> None:
    prom_gauges = {
        "http_status_code": Gauge(
            "http_status_code",
            "HTTP status code",
        ),
        "http_responding": Gauge(
            "http_responding",
            "Bool of accessible before ",
        ),
        "http_response_time": Gauge(
            "http_response_time_ms",
            "http response time in milliseconds",
        ),
    }
    for gauge in prom_gauges.values():
        prom_service.register(gauge)

    mifi_url = (
        f"http://{mifi_ip.compressed}/"
        if mifi_ip.version == 4
        else f"http://[{mifi_ip.compressed}]/"
    )
    while True:
        LOG.info(f"Starting a check of {mifi_url}")
        collect_start_time = time()
        current_metrics = await check_http_endpoint(mifi_url)
        for k, gauge in prom_gauges.items():
            gauge.set({"mifi_ip": mifi_ip.compressed}, getattr(current_metrics, k))

        collect_time_ms = (collect_start_time - time()) * 1000
        LOG.info(f"Finished collecting {len(prom_gauges)} metrics in {collect_time_ms}")
        await asyncio.sleep(interval)


async def prometheus_server(interval: float, port: int, mifi_ip: IPAddress) -> int:
    """Use aioprometheus to serve statistics to prometheus"""
    prom_service = Service()
    await prom_service.start(addr="::", port=port)
    LOG.info(f"Serving prometheus metrics on: {prom_service.metrics_url}")
    await update_prom_stats(interval, prom_service, mifi_ip)
    return 0


async def async_main(debug: bool, interval: float, port: int, mifi_ip: str) -> int:
    mifi_ip_addr = ip_address(mifi_ip)
    return await prometheus_server(interval, port, mifi_ip_addr)


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option(
    "--debug",
    is_flag=True,
    callback=_handle_debug,
    show_default=True,
    help="Turn on debug logging",
)
@click.option(
    "--interval",
    default=60.0,
    show_default=True,
    type=float,
    help="Interval to collect metrics",
)
@click.option(
    "--port",
    default=6123,
    show_default=True,
    type=int,
    help="Port for promethus http server to listen on",
)
@click.argument("mifi_ip", nargs=1)
@click.pass_context
def main(ctx: click.core.Context, **kwargs: Any) -> None:
    LOG.debug(f"Starting {sys.argv[0]}")
    ctx.exit(asyncio.run(async_main(**kwargs)))


if __name__ == "__main__":
    main()
