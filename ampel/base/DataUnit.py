#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/ampel/base/DataUnit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 12.10.2019
# Last Modified Date: 24.08.2020
# Last Modified By  : Jakob van Santen <jakob.van.santen@desy.de>

from typing import Tuple, Dict, Any, Optional, Union, TYPE_CHECKING
from ampel.base.AmpelBaseModel import AmpelBaseModel
if TYPE_CHECKING:
	from ampel.log.AmpelLogger import AmpelLogger


class DataUnit(AmpelBaseModel):

	# Named resources required by this unit.
	require: Optional[Tuple[str, ...]] = None
	version: Optional[Union[str, float]] = None

	logger: 'AmpelLogger'

	# Some unit contributors might want to restrict units usage
	# by scoping them to their respective distribution name (str)
	# private: Optional[str] = None

	@classmethod
	def __init_subclass__(cls, **kwargs) -> None:
		"""
		Inherit `require` attribute from superclass
		"""
		super().__init_subclass__(**kwargs) # type: ignore
		if (require := getattr(cls, "require", None)) or isinstance(require, tuple):
			combined_require = set(sum(
				(
					r for base in cls.__bases__
					if isinstance(r := getattr(base, 'require', None), tuple)
				),
				tuple()
			)).union(require)
			setattr(cls, "require", tuple(combined_require))


	def __init__(self,
		resource: Optional[Dict[str, Any]] = None, **kwargs
	) -> None:
		AmpelBaseModel.__init__(self, **kwargs)
		self.resource = resource

		if hasattr(self, "post_init"):
			self.post_init() # type: ignore


	def get_version(self) -> Optional[Union[str, float]]:
		return self.version
