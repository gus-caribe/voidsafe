# **Version 0** - _Beta_
&nbsp;&nbsp;&nbsp;&nbsp; **Version 0** includes all the basic features to perform **coalescing** operations, which helps assuring that **safe** can be done with **Potentially Unsafe Instances [2.1]** and their **Potentially Unsafe Resources [2.2]**.

----

## Release `v0.2.0`
&nbsp;&nbsp;&nbsp;&nbsp; This release includes an extensive documentation for the package.

### `#31` Python files Metadata
> **Participants:** @gus-caribe, @felalmeida

&nbsp;&nbsp;&nbsp;&nbsp; Added metadata to `.py` files located under `/examples`:

- **Adaptation:**

    1. Added `#!/usr/bin/env python3` _shebang_ on top of all files;
    2. Added `# -*- coding: utf-8 -*-` encoding metadata comment right after _shebang_.

### `#5` Library Documentation

&nbsp;&nbsp;&nbsp;&nbsp; Added an extensive documentation, which covers the following scopes:

- **Documentation:**

    1. Finished covering declarations' `docstrings`;
    2. Finished implementing `__repr__` methods;
    3. Elaborated the `API.md` file;
    4. Elaborated the content for the `/examples` directory;
    5. Elaborated more on the `README.md`;

## Release `v0.1.1`
&nbsp;&nbsp;&nbsp;&nbsp; In this release, the directory named "nonesafe" was renamed to "voidsafe" to match the module name.

- **Bugs:**

    1. Library directory does not match module name.

## Release `v0.1.0`
&nbsp;&nbsp;&nbsp;&nbsp; This release brings the basic API with the essential resources required to perform coalescing operations. The **docstrings** are still not fully covered. The `__repr__` and `__str__` magic methods are also not fully covered. The **API.md** file and the **/examples** directory won't be filled at this release. And lastly, the **unit tests** haven't still been elaborated.

- **Features:**

    - **Special Objects**:

        1. `VoidTypes`

    - **Special Types**

        1. `UndefinedType`
    
    - **Special Constants**

        1. `UNDEFINED` - alias: `Undefined`
        2. `VOID` - alias: `Void`
    
    - **Special Agents**

        1. `VOIDSAFE` - alias: `VoidSafe`
        2. `VALUE` - alias: `value`
    
    - **Special Operators**

        1. `IFNONE` - alias: `ifnone`
        2. `IFNDEF` - alias: `ifndef`
        3. `IFVOID` - alias: `ifvoid`
