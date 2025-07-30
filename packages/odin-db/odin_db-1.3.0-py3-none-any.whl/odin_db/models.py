from pydantic import BaseModel, Field
from typing import Literal
from enum import Enum
from typing import Any


class ODINDBModelType(str, Enum):
    U8 = "u8"
    U16 = "u16"
    U32 = "u32"
    U64 = "u64"
    I8 = "i8"
    I16 = "i16"
    I32 = "i32"
    I64 = "i64"
    F32 = "f32"
    F64 = "f64"
    BOOL = "bool"
    CHAR = "char"

    @classmethod
    def from_string(cls, value: str) -> "ODINDBModelType":
        try:
            return cls(value)
        except KeyError:
            raise ValueError(f"Invalid type: {value}")


class OdinDBTypeDefinitionModel(BaseModel):
    type: Literal["type_definition"] = Field(default="type_definition", description="Type of the type definition")
    size: int = Field(description="Size of the structure in bytes")
    structure: "ODINDBModelType | list[ODINDBModelType] | dict[str, OdinDBTypeDefinitionModel | ODINDBModelType]" = (
        Field(description="Structure of the type definition, key value based")
    )
    count: int | None = Field(description="Number of elements in the structure, if applicable")


class OdinDBBaseModel(BaseModel):
    name: str = Field(description="Name of the object")
    description: str = Field(description="Description of the object")
    global_id: int = Field(description="Unique ID of the object")
    global_name: str = Field(description="Unique name of the object")


class OdinDBParameterModel(OdinDBBaseModel):
    type: Literal["parameter"] = Field(default="parameter", description="Type of the parameter")
    element_size: int = Field(description="Size of the parameter in bytes")
    element_type: str = Field(description="Type of the parameter")
    default_value: Any | None = Field(description="Default value of the parameter")


class OdinDBArrayModel(OdinDBBaseModel):
    type: Literal["array"] = Field(default="array", description="Type of the array")

    element_size: int = Field(description="Size of the array in bytes")
    element_type: str = Field(description="Type of the elements in the array")
    element_count: int = Field(description="Number of elements in the array")
    default_value: list[Any] | None = Field(description="Default value of the array")


class OdinDBVectorModel(OdinDBBaseModel):
    type: Literal["vector"] = Field(default="vector", description="Type of the vector")

    element_size: int = Field(description="Size of the vector in bytes")
    element_type: str = Field(description="Type of the elements in the vector")
    max_element_count: int = Field(description="Maximum number of elements in the vector")
    default_value: list[Any] | None = Field(description="Default value of the vector")


class OdinDBParameterGroupModel(OdinDBBaseModel):
    type: Literal["parameter_group"] = Field(default="parameter_group", description="Type of the parameter group")
    parameters: "list[OdinDBParameterModel|OdinDBVectorModel|OdinDBArrayModel|OdinDBParameterGroupModel]" = Field(
        description="List of parameters in the group"
    )

    def as_flat_dict(self) -> dict[int, OdinDBParameterModel | OdinDBVectorModel | OdinDBArrayModel]:
        flat_dict = {}
        for param in self.parameters:
            if isinstance(param, OdinDBParameterModel | OdinDBVectorModel | OdinDBArrayModel):
                flat_dict[param.global_id] = param
            else:
                flat_dict.update(param.as_flat_dict())
        return flat_dict


class OdinDBModel(BaseModel):
    name: str
    description: str
    creation_timestamp: float  # Unix timestamp
    configuration_hash: int
    types: dict[str, OdinDBTypeDefinitionModel] | None = Field(description="Type definitions for the model")
    root: OdinDBParameterGroupModel
