# Import statement for the string module
import string

# Import statement for the SmartDevice parent class
from devices.Devices import SmartDevice


# Defines a new class, NewClass, which inherits from SmartDevice
class NewDevice(SmartDevice):
    """
    Class-level "private" property. Class-level properties are
    associated with the class, and not a particular instance of a class.
    This is particularly useful if all instances of an object should
    share the same value for a property. In this case, it holds the
    properties which should be returned on a default __api__ query,
    with the method being defined in the parent class.
    Typically, a single underscore represents to other programmers that
    this value is not meant to be set directly.
    """
    _api_return_parameters = [
        "new_property_a",
        "new_property_b"
    ]

    """
        Type hints provide hints to programmers as to what data type
        the input should take. It is specified as:
        <name>:<type> = <default_value>
    """

    def __init__(self, key1: str = "value1", key2: str = "value2"):
        """The constructor. Magic methods, or dunder (double-underscore)
        methods typically have special meanings to the Python
        interpreter or to other programmers. The __init__ method is
        called when a new object is constructed, e.g., running
        nd = NewDevice()
        will execute this code.
        In non-static member functions, the current object, usually
        named "self", is passed as the first argument.

        Args:
            key1 (str, optional): Named argument 1. Defaults to "value1".
            key2 (str, optional): Named argument 2. Defaults to "value2".
        """
        # Calls the constructor of the parent class, SmartDevice
        super.__init__(key1=key1, key2=key2)
        self.set_new_property("c")
        self.set_new_property("d")

    """
    Type hints for return values take the form of:
    def <function>(<args>) -> <return_type>:
    """
    @property
    def new_property_a(self) -> int:
        """Getter for new_property_a. Getting in this manner can allow
        custom logic to be applied to the "private" data stored in the
        class.
        For example, this function will return the property as
        the Unicode code point using the built-in function ord().
        This example is not necessarily useful, but working with
        datetimes, for instance, can allow the time to be stored as a
        datetime.datetime internally (for ease of calculations, perhaps)
        and returned as a string when accessed as a property.

        Returns:
            int: The Unicode code point equivalent of the value stored
            in self._new_property_a
        """
        return ord(self._new_property_a)

    def set_new_property_a(self, value: str = "a"):
        """Setter method for self._new_property_a. Setting in this
        manner allows for custom logic to be applied to setting values.
        For example, this function specifies that the input character
        must be a lowercase letter. If it is not, the value of
        self._new_property_a will not be updated.

        Args:
            value (str, optional): The value to set self._new_property_a
            to. Must be lowercase. Defaults to "a".
        """
        if value in string.ascii_lowercase:
            self._new_property_a

    @property
    def new_property_b(self) -> str:
        """Getter for new_property_b

        Returns:
            str: The value stored in self._new_property_b
        """
        return self._new_property_b

    def set_new_property_b(self, value: str = "b"):
        """Setter for self._new_property_b

        Args:
            value (str, optional): The value to set self._new_property_b
            to. Defaults to "b".
        """
        self._new_property_b
