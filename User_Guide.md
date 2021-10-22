# BlueXolo User Guide

## Create and Run a Test Case

In this guide you will find an example of how to create and run a test case, 
but first of all, you need to have an instance of BlueXolo available.

### Import Robot Framework

To be able to use Robot Framework commands and keywords you will need to download and import
the user guide to BlueXolo in order to have available these resources.

> You can download the user guide from the [Robot Framework Documentation].

Once you have the user guide zip file locally, you can go to the menu in BlueXolo and go to
`Robot Framework`, there you can manage all the imported versions and add new ones, to add a
new version you need to click on the :heavy_plus_sign: button.

To create this new source you just need to add a version number, select the user guide
zip file from your computer and click on `Create`.

[Robot Framework Documentation]: https://robotframework.org/robotframework/

### Create a Product

To create a product you need to go to the menu and select `Products`, then click on the :heavy_plus_sign:
button and give the product name of _Demo_ and the version _1.0_ just for this example. As
you can see, in the form you are able to add more information for your product, but for the
purpose of this guide with the required fields it is enough to click on `Create`.

### Create a Collection

With a product already created you need to add a collection to add new testing items, to do
this you need to go to the menu and select `Collections`, then click on the :heavy_plus_sign: and give the
name _Demo_Collection_ and select the previously created product, finally click on `Create`.

### Create a Keyword

Before creating the test case, let's add a new keyword to use run inside the test case, for
this you need to go to `Keywords` in the menu, click on :heavy_plus_sign:, this will redirect you to the
drag and drop environment, first select the _Demo_Collection_ and name the keyword as
_Hello_World_, once you have this basic data, search in the command box for the built-in
command called `Log To Console`, then click on the result and drag and drop to the editor.

When an item is in the editor you can click it and edit their properties, in the case let's
modify the `message` property of the `Log To Console` command, for that try writing
_Hello world!_ and click on `Set`. Finally, save the new keyword clicking on the green button
located in the lower right corner.

### Create a Phase

To create a test case is required to have a phase, this process is really easy, just go to the
menu and click on `Phases`, then click on :heavy_plus_sign: and give the name of _Demo_Phase_ and select the
_Demo_ product, after this you are ready to `Create`.

### Create a Test Case

Go to `Test Cases` in the menu and click on the :heavy_plus_sign: button to create a new test case, then select
your _Demo_Collection_ and _Demo_Phase_, once you have that give a name for your test case, for
example, _Demo_TC_ and finally search your _Hello_World_ keyword in the `Keyword Search` box, click
on the result and drag and drop to the editor, with these steps done everything is ready save the
test case by clicking in the lower right green button.

### Create Parameters

To run any testing item in BlueXolo you need a **Local Network Connection Profile** to connect to an
external server with Robot Framework installed, so you need to create some parameters first, by default the required parameters for a Local Network Connection are available in the **Base Connection Template**, but if you are working on a manually defined database there is a guide to create them. Open the
menu and go to `Parameters`, click on the :heavy_plus_sign: and select _Local Network Connection_ as category group,
give the name of _path_ and click on `Create`. Finally, replicate this process to create other three
parameters _user_, _passwd_ and _host_.

> It is very important to use the specified names and select the Local Network Connection category group on each command.

### Create a Template

A template is basically a wrapper for the parameters that you have created, and it is required to
create a profile. If in your environment you already have a template named **Base Connections**, go to the next step. To create this template open the menu and select `Templates`, click on :heavy_plus_sign:,
give it the name of _Base Connection_ and select the _Local Network Connection_ category group, then
search and add the four parameters created in the previous step. Finally, click on `Create Template`.

### Create a Profile

The last thing to do before you can run any testing item is create a profile, for this you need to
go to the menu and click on `Profiles`, then give it a name, in this case _Demo_Profile_ and select
the _Base Connection_. Once you have done that give the following values to the parameters:

- **host** `robot3.2.2`
- **user** `robot`
- **passwd** `bluexolo`
- **path** `/robot`

Finally, click on `Create`.

> **Note:** The *host* variable in the profile needs to have the value of a reachable IP running a SSH server with Robot Framework installed, by default robot2.9, robot3.2.2 and robot4.0 are reachable thanks to the *out-of-the-box* Robot Framework services defined in the compose environments of BlueXolo. We can take advantage of the internal DNS service built in Docker to pass the name of the container as host.

### Run a Test Case

To run a test case you need to go back to `Test Cases` and click the :arrow_forward: button of the _Demo_TC_
test case, select _Demo_Profile_ as _Connection Profile_ and click on `Run`.

### Check Execution Results

To check what happened during the execution of your test case, go to the home page and click on the
`View Result` button in the task card of your :heavy_check_mark: _Script - Demo_TC_.
