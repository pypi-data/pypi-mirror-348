import re

BUILT_IN_PREFIXES = ('id', 'text', 'data-test-id', 'data-testid','data-test')
ATTR_PREFIXES = ('placeholder', 'name', 'class', 'value', 'title')
OBJ_PREFIXES = ('link',)
XPATH_PREFIXES = ("xpath://", "//")
ALL_PREFIXES = BUILT_IN_PREFIXES + ATTR_PREFIXES + OBJ_PREFIXES

def standardize_locator(locator: str):
    index = 1
    if any(prefix for prefix in ALL_PREFIXES if locator.startswith(prefix)):
        index = get_custom_element_index(locator)
        locator = re.sub(r':', '=', locator, count=1)
        locator = re.sub(r'\[\d+]', '', locator)
        print_xpath(locator)
    else:
        locator = f"{locator}[not(self::script)]" if "[not(self::script)]" not in locator else locator
    return locator, index


def get_custom_element_index(custom_locator):
    """
    Handle the inputted custom locator with or without the index (E.g Customer Name[1])
    Note that index starts from 1 not zero (like xpath expression index)
    :param custom_locator: string with or without the index: E.g "Customer Name[1]"
    :return: a tuple of its index & its actual label
    """
    index = re.search(r'(?<=\[)\d*(?=])', custom_locator)
    if index:
        re.sub(r'\[\d*]$', '', custom_locator)
    return 1 if index is None else int(index.group())


def print_xpath(selector: str):
    prefix, label = selector.split("=")
    if prefix == "text":
        print(f'//body//*[not(self::script)][text()="{label}"]')
    elif prefix == "link":
        print(f'//a[contains(.,"{label}")]')
    else:
        print(f'//*[@{prefix}="{label}"]')


CUSTOM_QUERY = """
      {
           query(document, label) {
              let node = document.evaluate(`xpath_mask`, document, null,
              XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
              return node;
          },
           queryAll(document, label) {
              let xpath = `xpath_mask`;
              let results = [];
              let query = document.evaluate(xpath, document,
                  null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
              for (let i = 0, length = query.snapshotLength; i < length; ++i) {
                  results.push(query.snapshotItem(i));
              }
              return results;
                  }
      }
      """

def get_the_query_by_attribute(prefix: str) -> str:
    return f"""
      {{
           query(document, label) {{
              return document.evaluate(`//*[@{prefix}="${{label}}"]`, document, null, 
              XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
          }},
           queryAll(document, label) {{
              let results = [];
              let query = document.evaluate(`//*[@{prefix}="${{label}}"]`, document, null, 
              XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
              for (let i = 0, length = query.snapshotLength; i < length; ++i) {{
                  results.push(query.snapshotItem(i));
              }}
              return results;
                  }}
      }}
      """

QUERY_BY_LINK = """
      {
           query(document, label) {
              return document.evaluate(`//a[contains(.,"${label}")]`, document, null, 
              XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
          },
           queryAll(document, label) {
              let results = [];
              let query = document.evaluate(`//a[contains(.,"${label}")]`, document, null, 
              XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
              for (let i = 0, length = query.snapshotLength; i < length; ++i) {
                  results.push(query.snapshotItem(i));
              }
              return results;
                  }
      }
      """
