from typing import Sequence


def format_iterable(collection: Sequence, width: int) -> str:
    truncated_collection = []
    total_width = 0

    for item in collection:
        item_width = len(str(item)) + 2
        if total_width + item_width > width - 4 - len(str(collection[-1])):
            break

        truncated_collection.append(item)
        total_width += item_width

    if len(truncated_collection) == len(collection):
        return ", ".join(map(str, collection))

    return ", ".join(map(str, truncated_collection)) + f",...{collection[-1]}"


def generate_settings_report(
    args,
    max_channels,
    max_intensity,
    width=80,
    padding_left=15,
    padding_right=12,
) -> str:
    def row(desc: str, value: str, info: str = "") -> str:
        return f"{desc:>{padding_left}}: {value:.<{width-padding_left-padding_right}}{info:.>{padding_right}}"  # noqa: E501 # pylint: disable=line-too-long

    sections = [
        row(
            desc="source",
            value=str(args.IP_ADDRESS),
        ),
        row(
            desc="destination",
            value=(str(args.dst) if args.dst else "MULTICAST"),
        ),
        "",  # SECTION BREAK
        row(
            desc="mode",
            value=args.mode.value.upper(),
        ),
        row(
            desc="duration",
            value=f"{args.duration:.2f} s" if args.duration else "INDEFINITE",
        ),
        row(
            desc="frequency",
            value=f"{args.frequency:.2f} Hz",
        ),
        row(
            desc="resolution",
            value=f"{args.fps} fps",
        ),
        "",  # SECTION BREAK
        row(
            desc="universes",
            value=format_iterable(args.universes, width - padding_left - padding_right),
            info=f"({len(args.universes)})",
        ),
        row(
            desc="channels",
            value=str(args.channels),
            info=f"(out of {max_channels})",
        ),
        row(
            desc="intensity",
            value=f"{str(args.intensity_min)} - {str(args.intensity)}",
            info=f"(out of {max_intensity})",
        ),
    ]

    return "\n".join(sections)
