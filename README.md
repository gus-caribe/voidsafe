![Image](http://caribesphaneron.com/wp-content/uploads/2024/03/void_safe_logo.png)

&nbsp;&nbsp;&nbsp;&nbsp; **VoidSafe** is a library that brings a [**void-safe**](https://en.wikipedia.org/wiki/Void_safety), [**None-aware**](https://peps.python.org/pep-0505/) approach to Python3-written scripts and applications. It provides software developers with resources to apply _null-safe-like_ principles to their codebase, guaranteeing that **safe** operations can be performed on **potentially unsafe** instances, which helps assuring that your software will be able to handle many memory-access problems at runtime.

&nbsp;&nbsp;&nbsp;&nbsp; By being entirely [**type-hinted**](https://docs.python.org/3/library/typing.html), this library works well when associated with most **static type checkers**. When combined with a linter that's capable of predicting **unboud** or **undefined** variables, this library helps the developers to identify problems with their code even before running it.

&nbsp;&nbsp;&nbsp;&nbsp; The inspiration comes from the concept of [**Null Safety**](https://kotlinlang.org/docs/null-safety.html), which is adopted by several programming languages, such as **Dart**, **Kotlin** and **C#**.

----

## Ok, but... why bother?

&nbsp;&nbsp;&nbsp;&nbsp; It is known that many professionals use Python as a **practical** tool, a **means** to achieve a result where the **result** holds the business value intended. Data scientists, mathmaticians and physicists often use Python as a "fancy calculator" or a "plotting tool" to extract valuable data and information. It's easy to see that this library won't be able to contribute much to those use cases, it would probably only result in a processing overhed during the analysis or generation tasks.

&nbsp;&nbsp;&nbsp;&nbsp; But when it comes to Software Engineering, part of the business value is delivered in the form of **code quality** and **service availability**, which can't be guaranteed if your codebase is full of snippets that may raise a bunch of **Errors** and **Exceptions**. That is true especially for server-side programs that will run 24/7 with integrations with remote services. This library intends to help software developers to build up **robust** and **trustworthy** applications with Python3.

----

## Installation

&nbsp;&nbsp;&nbsp;&nbsp; **VoidSafe** will be added to **PyPi** soon...

----

## Examples

&nbsp;&nbsp;&nbsp;&nbsp; The examples will be added here soon. A complete guide will added to this project's **/examples** directory.

----

## Donate

&nbsp;&nbsp;&nbsp;&nbsp; You can help me develop more open-source software to the community by donating.

- **PayPal**   
    [![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donate_SM.gif)](https://www.paypal.com/donate/?hosted_button_id=CXX5CKLZHNK3C)
- **Buy me a coffee**   
    [!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/guscaribe)

## License
[MIT](https://choosealicense.com/licenses/mit/)
  
