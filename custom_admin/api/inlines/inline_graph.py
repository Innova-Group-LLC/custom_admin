import typing
from dataclasses import asdict, dataclass, field

from custom_admin.api.inlines.interfaces import InlineResultInterface

PLUGINS = {
    'title': {
        'display': True,
    },
    'tooltip': {
        'mode': 'index',
        'intersect': False,
    },
}


@dataclass
class ChartOptions:
    width: int = 400
    height: int = 400

    plugins: typing.Dict[str, dict] = field(default_factory=lambda: PLUGINS)


@dataclass
class GraphDataset:
    # читаемое название
    label: str

    data: typing.List[dict]

    # https://www.chartjs.org/docs/latest/charts/area.html#filling-modes
    fill: str = 'false'

    backgroundColor: str = 'rgb(200, 200, 200)'

    pointBorderColor: typing.Optional[str] = None

    borderColor: str = 'gray'
    borderWidth: int = 1

    pointBorderWidth: int = 1
    tension: float = 0.1


class ChartType:
    LINE = 'line'
    BAR = 'bar'
    BUBBLE = 'bubble'
    DOUGHNUT = 'doughnut'
    PIE = 'pie'
    POLARAREA = 'polararea'
    RADAR = 'radar'
    SCATTER = 'scatter'


@dataclass
class ChartData:
    type: ChartType = ChartType.LINE

    labels: typing.List[str] = field(default_factory=list)
    datasets: typing.List[GraphDataset] = field(default_factory=list)
    options: ChartOptions = field(default_factory=ChartOptions)


@dataclass
@InlineResultInterface.register
class InlineGraphResult:
    messages: typing.List[dict] = field(default_factory=dict)

    charts: typing.List[ChartData] = field(default_factory=list)

    def asdict(self) -> dict:
        return asdict(self)
