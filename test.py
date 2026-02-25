from dc_u2_driver import ElementDriver
from dataclasses import dataclass, field
from typing import List, Optional, Any
import time

@dataclass
class ElementFinder:
    deviceID: str
    xpaths: List[str]
    retries: int = 30
    retry_delay: float = 0.5  # seconds between retries
    found_elements: List[Any] = field(default_factory=list)

    def __post_init__(self):
        self.driver = ElementDriver(self.deviceID)

    def find_elements(
        self,
        wait: int = 5,
        locatorType: str = "xpath",
        isJustWait: bool = False,
        textInput: Optional[str] = None,
        index: Optional[int] = None,
        isLongClick: bool = False,
        get_attribute: bool = False,
        attribute: Optional[str] = None,
        get_all: bool = False
    ) -> List[Any]:
        """
        Find all elements for the list of xpaths.
        """
        self.found_elements.clear()

        for xpath in self.xpaths:
            element = self.driver.work_on_element(
                wait,
                xpath,
                locatorType,
                isJustWait,
                textInput,
                index,
                isLongClick,
                get_attribute,
                attribute,
                get_all
            )
            self.found_elements.append(element)

        return self.found_elements

    def find_element(
        self,
        wait: int = 5,
        locatorType: str = "xpath",
        isJustWait: bool = False,
        textInput: Optional[str] = None,
        index: Optional[int] = None,
        isLongClick: bool = False,
        get_attribute: bool = False,
        attribute: Optional[str] = None,
        get_all: bool = False
    ) -> Optional[Any]:
        """
        Find the first element that exists among all xpaths, retrying if necessary.
        """
        for i in range(self.retries):
            for xpath in self.xpaths:
                element = self.driver.work_on_element(
                    wait,
                    xpath,
                    locatorType,
                    isJustWait,
                    textInput,
                    index,
                    isLongClick,
                    get_attribute,
                    attribute,
                    get_all
                )
                if element:
                    return element
            time.sleep(self.retry_delay)  # wait before retrying
        return None


# ----------------------
# Usage Example
# ----------------------

# finder = ElementFinder(
#     deviceID="emulator-5554",
#     xpaths=[
#         '//*[@text="Log in"]',
#         '//*[@content-desc="Mobile number or email"]'
#     ],
#     retries=10
# )

# Find first matching element
# element = finder.find_element(wait=5, locatorType="xpath")
# if element:
#     print("Found first element:", element)
# else:
#     print("Element not found.")

# # Find all matching elements
# elements = finder.find_elements(wait=5, locatorType="xpath")
# print(f"Found {len(elements)} elements.")

# elements = finder.find_element(
#     wait=5,
#     get_all=True,
#     get_attribute=True,
#     attribute="text"
# )
# print("Found all elements:", elements)