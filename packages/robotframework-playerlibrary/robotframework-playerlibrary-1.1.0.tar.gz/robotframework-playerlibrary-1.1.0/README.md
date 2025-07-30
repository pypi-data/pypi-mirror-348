# robotframework-playerlibrary
Simple GUI/API automation testing library written in Python using Playwright

**Import the library:**
```
*** Settings ***
Library           PlayerLibrary    assertion_timeout=10000    
```
_assertion_timeout_: Customize the timeout for each assertion in milliseconds

**Example keyword:**
```
*** Keywords ***
Login into the system using provided account
    Input Into    id:login-email       sample-test@abc.com
    Input Into    id:login-password    yourpassword
    Click    //button[contains(.,"Sign In")]
    Page Should Have    Welcome Back!

```
**Example UI scenario:**
```
Suite Setup          Start Browser Then Open Url    https://sample-system.com/     headless=True


Test Setup       Login into the system using provided account    AND
Test Teardown       Start new browser session
Suite Teardown      Quit all browsers

*** Test Cases ***
TC_01 - Check correctness of some elements on the screen
    Element Should Be Shown    ${calendar_picker}
    Element Should Be Shown    ${apply_btn}
    Element Should Be Shown    ${clear_btn}
```
**Example API scenario:**
```
TC_001 - Sample Rest API test case
    [Tags]     api    
    ${sample_header}    Create Header
    start api session
    ${resp}     rest post    ${URL}     ${sample_header}     ${post_body}
    rest patch    https://api.restful-api.dev/objects/${resp}[id]     ${sample_header}    ${patch_body}
    rest put      https://api.restful-api.dev/objects/${resp}[id]     ${sample_header}    ${put_body}
    rest delete   https://api.restful-api.dev/objects/${resp}[id]     ${sample_header}
    rest get      https://api.restful-api.dev/objects                 ${sample_header}
    Rest Dispose
```

**Keyword documentation at** https://lynhbn.github.io/robotframework-playerlibrary/keyword_document.html

**Quick-hand prefix locator supported:**
- `BUILT_IN_PREFIXES` = ('id', 'text', 'data-test-id', 'data-testid','data-test')
- `ATTR_PREFIXES` = ('placeholder', 'name', 'class', 'value', 'title')
- `OBJ_PREFIXES` = ('link',)
- `XPATH_PREFIXES` = ("xpath://", "//")