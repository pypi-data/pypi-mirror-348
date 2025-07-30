# Steps API

Steps are the building blocks of SpiderChef recipes. This reference documents the core step classes and the built-in step types available in SpiderChef.

## Core Step Classes

::: spiderchef.steps.base.BaseStep
    handler: python
    options:
      show_source: true
      show_bases: true
      show_root_heading: true
      show_object_full_path: false
      heading_level: 3

::: spiderchef.steps.base.SyncStep
    handler: python
    options:
      show_source: true
      show_bases: true
      show_root_heading: true
      show_object_full_path: false
      heading_level: 3

::: spiderchef.steps.base.AsyncStep
    handler: python
    options:
      show_source: true
      show_bases: true
      show_root_heading: true
      show_object_full_path: false
      heading_level: 3

::: spiderchef.steps.asynchronous.FetchStep
    handler: python
    options:
      show_source: true
      show_root_heading: true
      show_object_full_path: false
      heading_level: 3

::: spiderchef.steps.asynchronous.SleepStep
    handler: python
    options:
      show_source: true
      show_root_heading: true
      show_object_full_path: false
      heading_level: 3

## Extraction Steps

::: spiderchef.steps.extract.RegexStep
    handler: python
    options:
      show_source: true
      show_root_heading: true
      show_object_full_path: false
      heading_level: 3

::: spiderchef.steps.extract.RegexFirstStep
    handler: python
    options:
      show_source: true
      show_root_heading: true
      show_object_full_path: false
      heading_level: 3

::: spiderchef.steps.extract.XpathStep
    handler: python
    options:
      show_source: true
      show_root_heading: true
      show_object_full_path: false
      heading_level: 3

::: spiderchef.steps.extract.XpathFirstStep
    handler: python
    options:
      show_source: true
      show_root_heading: true
      show_object_full_path: false
      heading_level: 3

::: spiderchef.steps.extract.GetStep
    handler: python
    options:
      show_source: true
      show_root_heading: true
      show_object_full_path: false
      heading_level: 3

::: spiderchef.steps.extract.ExtractItemsStep
    handler: python
    options:
      show_source: true
      show_root_heading: true
      show_object_full_path: false
      heading_level: 3

## Transformation Steps

::: spiderchef.steps.format.JoinBaseUrl
    handler: python
    options:
      show_source: true
      show_root_heading: true
      show_object_full_path: false
      heading_level: 3

::: spiderchef.steps.format.FromJson
    handler: python
    options:
      show_source: true
      show_root_heading: true
      show_object_full_path: false
      heading_level: 3

::: spiderchef.steps.format.ToInt
    handler: python
    options:
      show_source: true
      show_root_heading: true
      show_object_full_path: false
      heading_level: 3

::: spiderchef.steps.format.ToStr
    handler: python
    options:
      show_source: true
      show_root_heading: true
      show_object_full_path: false
      heading_level: 3

::: spiderchef.steps.format.ToFloat
    handler: python
    options:
      show_source: true
      show_root_heading: true
      show_object_full_path: false
      heading_level: 3

::: spiderchef.steps.format.ToMoneyStep
    handler: python
    options:
      show_source: true
      show_root_heading: true
      show_object_full_path: false
      heading_level: 3

::: spiderchef.steps.format.RemoveExtraWhitespace
    handler: python
    options:
      show_source: true
      show_root_heading: true
      show_object_full_path: false
      heading_level: 3

::: spiderchef.steps.format.RemoveHTMLTags
    handler: python
    options:
      show_source: true
      show_root_heading: true
      show_object_full_path: false
      heading_level: 3

## Flow Control Steps

::: spiderchef.steps.conditional.CompareStep
    handler: python
    options:
      show_source: true
      show_root_heading: true
      show_object_full_path: false
      heading_level: 3

## Data Management Steps

::: spiderchef.steps.base.SaveStep
    handler: python
    options:
      show_source: true
      show_root_heading: true
      show_object_full_path: false
      heading_level: 3

## Error Handling Steps

::: spiderchef.steps.error.TryCatchStep
    handler: python
    options:
      show_source: true
      show_root_heading: true
      show_object_full_path: false
      heading_level: 3
