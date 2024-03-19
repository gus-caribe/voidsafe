<p align="center">
  <img width="300" height="300" src="http://caribesphaneron.com/wp-content/uploads/2024/03/void_safe_logo_v2.png">
</p>

## VoidSafe

&nbsp;&nbsp;&nbsp;&nbsp; **VoidSafe** is a package that brings a **_null-safe-like_** approach to Python3-written scripts and applications. It provides software developers with resources to apply [**_void-safety_**](https://en.wikipedia.org/wiki/Void_safety) principles to their codebase, allowing **_coalescing_** operations to be performed on **_Potentially Unsafe Instances_** _[2.1]_ , which helps assuring that your software will be able to handle many **memory-access** problems at runtime.

&nbsp;&nbsp;&nbsp;&nbsp; By being entirely [**_type-hinted_**](https://docs.python.org/3/library/typing.html), this package works well when associated with most **_static type checkers_**. When combined with a linter that's capable of predicting **_unboud_** and **_undefined_** variable problems, **VoidSafe** helps developers to identify problems with their code even before running it.

## Inspiration

&nbsp;&nbsp;&nbsp;&nbsp; The inspiration for this package comes from the concept of [**_Null Safety_**](https://kotlinlang.org/docs/null-safety.html), which has been adopted by several programming languages, such as **Dart**, **Kotlin** and **C#**. Since the core developers have shown [_little interest_](https://peps.python.org/pep-0505/) in implementing those principles _canonically_, the opportunity came in as a great challenge.

&nbsp;&nbsp;&nbsp;&nbsp; Python doesn't exactly adopt the concept of **`null`**. One can argue that **`None`** serves for the same purpose, but since Python doesn't handle namespaces by **'{blocks}'**, the **`None`** constant doesn't actually cover every case where a given instance can't be used for operations. For instance, Python allows running scripts containing variables that have never been **_defined_** or **_assigned_** with absolutely **_no warnings_**.

&nbsp;&nbsp;&nbsp;&nbsp; Because there's support for [_changing local variables dynamically_](https://stackoverflow.com/questions/8028708/dynamically-set-local-variable), **`voidsafe`** can't protect your code from **_undefined_** and **_unboud_** instances, but it can protect you from accessing **_Potentially Unsafe Resources_** _[2.2]_ by returning a **_Special Constant_** _[1.3]_ named **`Undefined`** whenever you try to access an **'.attribute'**, **'[item]'** or **'method()'** that hasn't been defined.

&nbsp;&nbsp;&nbsp;&nbsp; That's where **`Void`** **_Special Constant_** comes in. It unites the concept of **`None`** and **`Undefined`** into a single constant, allowing developers to check if a resource is ready to be used for further operations.

## Ok, but... Why bother?

> Why wearing a seatbelt when you can just drive safely, right?

&nbsp;&nbsp;&nbsp;&nbsp; It is known that many professionals use Python as a **_practical_** tool, a **_means_** to achieve a result where the **_result_** holds the business value intended. Data scientists, mathmaticians and physicists often use Python as a "fancy calculator" or a "plotting tool" to elaborate and extract valuable data and information. It's easy to see that this library won't be able to contribute much to those use cases, it would probably only lead to a processing overhed during execution.

&nbsp;&nbsp;&nbsp;&nbsp; But when it comes to Software Engineering, part of the business value is delivered in the form of **_code quality_**, **_maintainability_** and **_service availability_**, which can't be offered if your project is full of lines of code **_craving_** to **raise** **`Error`**s and **`Exception`**s. That is true especially for server-side applications that are supposed to run _24/7_ interacting with third-party services. This library intends to help software developers building up **_robust_** and **_reliable_** applications with Python3.

## Installation

&nbsp;&nbsp;&nbsp;&nbsp; **VoidSafe** is on [**_PyPi_**](https://pypi.org/project/voidsafe/). You can install its latest version via `pip install` as follows:

```console
pip install voidsafe
```

## Examples

&nbsp;&nbsp;&nbsp;&nbsp; Take, for instance, the following [**_Dart_**](https://dart.dev/) code snippet:

> &nbsp;&nbsp;&nbsp;&nbsp; See [this](https://www.darttutorial.org/dart-tutorial/dart-null-aware-operators/) article about Dart's null-aware operators.

```dart
void main() {
    Map<String, String?> unsafeDict = {'item': null};
    String safeStr = '\t safeStr #1';

    safeStr += unsafeDict['item'] ?? '\t safeStr #2';
    safeStr += unsafeDict['item']?.toUpperCase() ?? '\t safeStr #3';

    unsafeDict['item'] ??= '\t unsafeDict #1';
    unsafeDict['item'] ??= '\t unsafeDict #2';

    safeStr += unsafeDict['item'] ?? '\t safeStr #4';
    safeStr += unsafeDict['item']?.toUpperCase() ?? '\t safeStr #5';

    print(safeStr);
}
```   

&nbsp;&nbsp;&nbsp;&nbsp; With the help of `voidsafe` package, the code above could be **_similarly_** brought up to Python like this:

```python
from voidsafe import VoidSafe, ifvoid, value
from typing import Optional

unsafeDict: dict[str, Optional[str]] = {'item': None}
safeStr: str = '\t safeStr #1'

safeStr += unsafeDict['item'] <<ifvoid>> '\t safeStr #2'
safeStr += VoidSafe(unsafeDict['item']).upper() <<ifvoid>> '\t safeStr #3'

VoidSafe(unsafeDict)['item'] = ifvoid << '\t unsafeDict #1'
VoidSafe(unsafeDict)['item'] = ifvoid << '\t unsafeDict #2'

safeStr += unsafeDict['item'] <<ifvoid>> '\t safeStr #4'
safeStr += VoidSafe(unsafeDict['item']).upper() <<ifvoid>> '\t safeStr #5'

print(safeStr)
```   

&nbsp;&nbsp;&nbsp;&nbsp; By running any of the scripts above, you will get the exact same output:

```console
    safeStr #1	 safeStr #2	 safeStr #3	 unsafeDict #1	 UNSAFEDICT #1
```

&nbsp;&nbsp;&nbsp;&nbsp; You can see usage examples all over this project. This repository provides the `API.md` file, which explores barely every possible use for this package's public resources. 

&nbsp;&nbsp;&nbsp;&nbsp; There's a directory named `/examples` which contains commented scripts that can be modified and executed in order to understand the implications that an **_event_** that's `"taken for granted"` will result in the output.

&nbsp;&nbsp;&nbsp;&nbsp; Besides that, `voidsafe` module's `core.py` implements `docstrings` with examples for basically every declaration that's coded inside it, even the _private_ ones.

&nbsp;&nbsp;&nbsp;&nbsp; A **_Wiki_** is under construction at [**_Caribe's Docs_**](docs.caribesphaneron.com) and it will be released soon. It will help developers to understand the concepts introduced by this library.
  
## Support the Project

### Contributing

&nbsp;&nbsp;&nbsp;&nbsp; This project is being maintained by a **_sole developer_** DevTeam. For now, there are no resources available to keep a frequent **_development_** and **_code review_** routine to guarantee that the code pulled by other developers won't compromise the library's principles.

&nbsp;&nbsp;&nbsp;&nbsp; Despite that, you can help this project by giving a **donation**. That way, this **_one-person_** _DevTeam_ can dedicate its time and effort to collaborate with the community by developing **_free_** and **_open-source_** software.

### Donating

&nbsp;&nbsp;&nbsp;&nbsp; If this package has helped adding value to your software or if you appreciated the initiative, consider giving a **_donation_** to help this project keep being **maintained** and **improved**.

&nbsp;&nbsp;&nbsp;&nbsp; When submitting a donation, you can leave a comment telling _us_ how this package has helped you and what could be done to make it even better. That would be much appreciated.

- **PayPal**   
    [![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donate_SM.gif)](https://www.paypal.com/donate/?hosted_button_id=CXX5CKLZHNK3C)
- **Buy me a Coffee**   
    [!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/guscaribe)

...
