from .commando import draai_pijp, vereis_programma


def map_hash(map_pad: str):
    vereis_programma("tar")
    vereis_programma("sha1sum")

    return draai_pijp(
        [
            [
                "tar",
                "-c",
                "-f",
                "-",
                "-C",
                map_pad,
                "--sort=name",
                "--owner=root:0",
                "--group=root:0",
                "--mtime=UTC 1970-01-01",
                ".",
            ],
            ["sha1sum"],
        ]
    ).split(" ")[0]
