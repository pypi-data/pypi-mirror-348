######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.12                                                                                #
# Generated on 2025-05-15T19:09:53.956774                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.plugins.pypi.conda_environment

from .conda_environment import CondaEnvironment as CondaEnvironment

class PyPIEnvironment(metaflow.plugins.pypi.conda_environment.CondaEnvironment, metaclass=type):
    ...

