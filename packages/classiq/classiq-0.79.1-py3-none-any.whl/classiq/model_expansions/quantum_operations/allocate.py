from typing import TYPE_CHECKING, Optional

import sympy

from classiq.interface.debug_info.debug_info import FunctionDebugInfo
from classiq.interface.exceptions import ClassiqValueError
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.expressions.proxies.classical.any_classical_value import (
    AnyClassicalValue,
)
from classiq.interface.model.allocate import Allocate
from classiq.interface.model.handle_binding import NestedHandleBinding
from classiq.interface.model.quantum_type import QuantumBitvector, QuantumNumeric

from classiq.model_expansions.evaluators.quantum_type_utils import copy_type_information
from classiq.model_expansions.quantum_operations.emitter import Emitter
from classiq.model_expansions.scope import QuantumSymbol

if TYPE_CHECKING:
    from classiq.model_expansions.interpreters.base_interpreter import BaseInterpreter


class AllocateEmitter(Emitter[Allocate]):
    def __init__(
        self, interpreter: "BaseInterpreter", allow_symbolic_size: bool = False
    ) -> None:
        super().__init__(interpreter)
        self._allow_symbolic_size = allow_symbolic_size

    def emit(self, allocate: Allocate, /) -> bool:
        target: QuantumSymbol = self._interpreter.evaluate(allocate.target).as_type(
            QuantumSymbol
        )

        if isinstance(target.handle, NestedHandleBinding):
            raise ClassiqValueError(
                f"Cannot allocate partial quantum variable {str(target.handle)!r}"
            )

        size_expr = self._get_var_size(target, allocate.size)
        if isinstance(target.quantum_type, QuantumNumeric):
            target.quantum_type.set_bounds((0, 0))
        allocate = allocate.model_copy(
            update=dict(
                size=Expression(expr=size_expr),
                target=target.handle,
                back_ref=allocate.uuid,
            )
        )
        self._register_debug_info(allocate)
        self.emit_statement(allocate)
        return True

    def _get_var_size(self, target: QuantumSymbol, size: Optional[Expression]) -> str:
        if size is None:
            if not target.quantum_type.is_evaluated:
                raise ClassiqValueError(
                    f"Could not infer the size of variable {str(target.handle)!r}"
                )
            return str(target.quantum_type.size_in_bits)

        size_value = self._interpreter.evaluate(size).value
        if self._allow_symbolic_size and isinstance(
            size_value, (sympy.Basic, AnyClassicalValue)
        ):
            return str(size_value)
        if not isinstance(size_value, (int, float)):
            raise ClassiqValueError(
                f"The number of allocated qubits must be an integer. Got "
                f"{str(size_value)!r}"
            )
        size_expr = str(size_value)
        copy_type_information(
            QuantumBitvector(length=Expression(expr=size_expr)),
            target.quantum_type,
            str(target.handle),
        )
        return size_expr

    def _register_debug_info(self, allocate: Allocate) -> None:
        if (
            allocate.uuid in self._debug_info
            and self._debug_info[allocate.uuid].name != ""
        ):
            return
        parameters: dict[str, str] = {}
        if allocate.size is not None:
            parameters["num_qubits"] = allocate.size.expr
        self._debug_info[allocate.uuid] = FunctionDebugInfo(
            name="allocate",
            port_to_passed_variable_map={"ARG": str(allocate.target)},
            node=allocate._as_back_ref(),
        )
