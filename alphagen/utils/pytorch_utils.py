from typing import Generic, TypeVar, Callable, Tuple, Optional
import torch
from torch import nn, Tensor


_TIn = TypeVar("_TIn")
_TOut = TypeVar("_TOut")


class MapperModule(nn.Module, Generic[_TIn, _TOut]):
    def __init__(self, mapper: Callable[[_TIn], _TOut]) -> None:
        super().__init__()
        self.mapper = mapper

    def forward(self, input: _TIn) -> _TOut: return self.mapper(input)


def masked_mean_std(
    x: Tensor,
    n: Optional[Tensor] = None,
    mask: Optional[Tensor] = None
) -> Tuple[Tensor, Tensor]:
    """
    `x`: [days, stocks], input data
    `n`: [days], should be `(~mask).sum(dim=1)`, provide this to avoid necessary computations
    `mask`: [days, stocks], data masked as `True` will not participate in the computation, \
    defaults to `torch.isnan(x)`
    """
    if mask is None:
        mask = torch.isnan(x)
    if n is None:
        n = (~mask).sum(dim=1)
    x = x.clone()
    x[mask] = 0.
    mean = x.sum(dim=1) / n
    std = ((((x - mean[:, None]) * ~mask) ** 2).sum(dim=1) / n).sqrt()
    return mean, std
