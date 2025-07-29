from typing import Any, Dict, Union, List, Tuple
import binascii
from .gtv import encode_value, gtv_auto

def to_buffer(hex_str: str) -> bytes:
    """Convert hex string to bytes"""
    return binascii.unhexlify(hex_str)

def to_string(buffer: bytes, encoding: str = 'hex') -> str:
    """Convert bytes to string"""
    if encoding == 'hex':
        return binascii.hexlify(buffer).decode('ascii').upper()
    return buffer.decode(encoding)

def to_query_object(name_or_query_object: Union[str, Dict[str, Any]], query_arguments: Dict[str, Any] = None) -> bytes:
    """
    Convert a query name/arguments or query object into a GTV-compatible format.
    
    This matches the JavaScript implementation:
    export type QueryObjectGTV = [name: string, args: Arg];
    export function toQueryObjectGTV(
      nameOrObject: string | QueryObject,
      queryArguments?: DictPair,
    ): QueryObjectGTV {
      let name;
      if (typeof nameOrObject === "string") {
        name = nameOrObject;
        return [name, { ...queryArguments }];
      } else {
        const objectCopy = { ...nameOrObject };
        const { type, ...restProps } = objectCopy;
        return [type, restProps];
      }
    }
    
    Args:
        name_or_query_object: Either a string query name or a query object
        query_arguments: Optional dictionary of query arguments
    
    Returns:
        Bytes containing the GTV-encoded query
    """
    if isinstance(name_or_query_object, str):
        # If it's a string, use it as the name and the arguments as the second element
        query_tuple = [name_or_query_object, query_arguments or {}]
    else:
        # If it's a dict, extract the 'type' as the name and the rest as arguments
        query_dict = name_or_query_object.copy()
        query_type = query_dict.pop('type', None)
        if query_type is None:
            raise ValueError("Query object must have a 'type' field")
        query_tuple = [query_type, query_dict]
    
    # Convert to GTV format and encode
    gtv_value = gtv_auto(query_tuple)
    return encode_value(gtv_value)