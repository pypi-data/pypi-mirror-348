<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the Egeria project. -->

# Rules 
* If this is a create, and qualfied name is provided, it will be used.
* If this is an update, and qualified name is provided, it is an error if it doesn't match.
* If this is an update and no qualified name provided, will try to use the display name
* If this is an update and qualified name and guid provided, then the qualified name can be changed
    => This needs work when the upsert methods are done

# Create Solution Component

## Display Name

Lab Processes

## Description
Test to create component that doesn't exist
## Version Identifier
1
## Solution Component Type
Should succeed
## Planned Deployed Implementation Type

## Solution Blueprints

SolutionBlueprint:Clinical Trial Management Solution Blueprint:V1.2

## Parent Components

---


# Update Solution Component

## Display Name

Hospital Processes

## Description
Test to Update a component that exists
## Version Identifier
2
## Solution Component Type
Should succeed
## Planned Deployed Implementation Type

## Solution Blueprints

SolutionBlueprint:Clinical Trial Management Solution Blueprint:V1.2

## Parent Components

---

---


# Update Solution Component

## Display Name

Dunga Din

## Description
Test to Update a component that does not exist 
## Version Identifier
3
## Solution Component Type
Should fail
## Planned Deployed Implementation Type

## Solution Blueprints

SolutionBlueprint:Clinical Trial Management Solution Blueprint:V1.2

## Parent Components

---

# Create Solution Component

## Display Name

Create-with-q-name

## Description
Test to create a new component that does not exist with own qname
## Version Identifier
4
## Solution Component Type
Should succeed
## Planned Deployed Implementation Type

## Solution Blueprints

SolutionBlueprint:Clinical Trial Management Solution Blueprint:V1.2

## Parent Components
## Qualified Name
TEST:Component:Create-with-q-name

---

# Update Solution Component

## Display Name

Update-with-existing-q-name-match

## Description
Test to update a component that that exists and has a supplied q-name
## Version Identifier
5
## Solution Component Type
Should succeed - but need to do real create to fully test
## Planned Deployed Implementation Type

## Solution Blueprints

SolutionBlueprint:Clinical Trial Management Solution Blueprint:V1.2

## Parent Components

## Qualified Name
TEST:Component:Create-with-q-name

---

---

# Update Solution Component

## Display Name

Update-with-q-name-mismatch

## Description
Test to create a new component that does not exist with own qname
## Version Identifier
6
## Solution Component Type
Should fail - but need real implementation to know
## Planned Deployed Implementation Type

## Solution Blueprints

SolutionBlueprint:Clinical Trial Management Solution Blueprint:V1.2

## Parent Components
TEST:Component:Create-with-q-name
## Qualified Name
TEST:Component:Create-with-q-name:meow
---