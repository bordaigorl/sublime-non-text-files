# Non-Text-Files Sublime Text plugin

Sometimes it would be more useful if Sublime Text launched the default application for certain file types instead of displaying it in the editor.
For example, if you open a PDF from the Sublime Text sidebar, the incomprehensible stream of compressed data is most often not what you intended to view. Instead you would like to view the document using your default viewer, be it Acrobat or Evince or any other.

This plugin offers settings and commands to control when Sublime should open certain files with external applications.

There is an option to turn off previews for binary files and options to open files with their default external applications.

If you like this plugin and would like to support its development please consider donating through a [paypal donation][paypal].

## Changelog

**v1.3**

+ "Open Externally" should now handle right click on sidebar correctly (fixes #2)

**v1.2**

+ multiple matching patterns do not trigger open multiple times
+ double click behaviour is now more stable and predictable
+ preview closing is more reliable


## Installation

 1. Install [Sublime Text](http://www.sublimetext.com/)

 2. Install the plugin either:
    - with **Package Control**: see <https://sublime.wbond.net/docs/usage>, or
    - **manually**: by cloning this repository in your Sublime Text Package directory

 3. Customise the `open_externally_patterns` setting in your preferences
    (`Preferences > Settings - User`)

## Features and settings

### Prevent Binary File Preview

When the setting `prevent_bin_preview` is set to `true` (default), clicking on a file matching any of the `binary_file_patterns` would not open the file.
Double click will open it normally: this is useful when using plugins like [Hex​Viewer] or [Zip Browser].

The `prevent_bin_preview` settings can be set globally in the `User/Preferences.sublime-settings` file or locally to a project.

### Open files with external applications

Sometimes it would be more useful if Sublime Text launched the default application for certain file types instead of displaying it in the editor.
This plugin allows you to do that via a special option: the files matching any of the `open_externally_patterns` will be opened with the default application as configured in your OS instead of using Sublime. You can set it globally in the `User/Preferences.sublime-settings` file or locally to a project.
This setting follows the same syntax of the `binary_file_patterns` setting: it is just a list of [glob patterns](https://en.wikipedia.org/wiki/Glob_%28programming%29). An example:

    "open_externally_patterns": [
        "*.jpg",
        "*.jpeg",
        "*.png",
        "*.gif",
        "*.zip",
        "*.pdf"
    ]

The plugin also offers a window command `open_externally` that opens a file with the default application. It takes two optional arguments:

 - `path` is the path of the file to be opened; if empty the file of the current view will be opened;
 - `then_close` if true will close the view after opening the file.

You can bind this command to a shortcut by adding the following to your keymap:

```json
{
  "keys": ["super+enter"], "command": "open_externally",
  "args": {"then_close": false}
}
```




[Hex​Viewer]:   <https://sublime.wbond.net/packages/HexViewer> 
[Zip Browser]: <https://sublime.wbond.net/packages/Zip%20Browser> 

[paypal]: <https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=JFWLSUZYXUHAQ>
