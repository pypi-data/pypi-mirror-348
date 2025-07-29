
from typing import List

from sqlalchemy import text
from .base import UMnetdbBase


class UMnetdb(UMnetdbBase):

    URL="postgresql+psycopg://{UMNETDB_USER}:{UMNETDB_PASSWORD}@wintermute.umnet.umich.edu/umnetdb"

    def get_device_neighbors(
        self, device: str, known_devices_only: bool = True
    ) -> List[dict]:
        """
        Gets a list of the neighbors of a particular device. If the port
        has a parent in the LAG table that is included as well.
        Neighbor hostname is also looked up in the device table and
        the "source of truth" hostname is returned instead of what shows
        up in lldp neighbor.

        Setting 'known_devices_only' to true only returns neighbors that are found
        in umnet_db's device table. Setting it to false will return all lldp neighbors.

        Returns results as a list of dictionary entries keyed on column names.
        """

        if known_devices_only:
            select = [
                "n.port",
                "n_d.name as remote_device",
                "n.remote_port",
                "l.parent",
                "n_l.parent as remote_parent"
                ]
        else:
            select = [
                "n.port",
                "coalesce(n_d.name, n.remote_device) as remote_device",
                "n.remote_port",
                "l.parent",
                "n_l.parent as remote_parent"
            ]
        
        table = "neighbor n"

        joins = [
             "left outer join device n_d on n_d.hostname=n.remote_device",
             "left outer join lag l on l.device=n.device and l.member=n.port",
             "left outer join lag n_l on n_l.device=n_d.name and n_l.member=n.remote_port",
        ]

        where = [f"n.device='{device}'"]

        query = self._build_select(select, table, joins, where)
        result = self.session.execute(text(query))

        return [dict(zip(result.keys(), r)) for r in result]