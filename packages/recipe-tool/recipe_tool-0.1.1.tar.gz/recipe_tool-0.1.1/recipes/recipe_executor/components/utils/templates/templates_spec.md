# Utils Component Specification

## Purpose

The Utils component provides general utility functions for recipes, primarily focused on template rendering. It offers a way to render strings with template variables against the execution context, enabling dynamic content generation in recipes.

## Core Requirements

- Render strings as templates using context data
- Utilize a standard templating engine (Liquid) for consistency
- Ensure that all context values are accessible to the templates
- Handle errors in template rendering gracefully
- Keep the utility functions stateless and reusable

## Implementation Considerations

- Use the Liquid templating library directly without unnecessary abstraction
- Pass the `context.dict()` to the Liquid template for rendering
- Handle rendering errors gracefully with clear error messages
- Keep the implementation stateless and focused on its single responsibility

## Logging

- None

## Component Dependencies

### Internal Components

- **Protocols**: Uses ContextProtocol definition for context data access

### External Libraries

- **python-liquid**: Uses the Liquid templating engine for rendering

### Configuration Dependencies

None

## Error Handling

- Wrap template rendering in try/except blocks
- Raise ValueError with a clear message if rendering fails
- Use `liquid.exceptions.LiquidError` for Liquid-specific errors, otherwise just raise a generic ValueError
- Ensure that the error message includes the template and context for easier debugging

## Output Files

- `recipe_executor/utils/templates.py`
