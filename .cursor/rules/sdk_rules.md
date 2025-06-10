# SDK Development Guidelines

## Models
- Create base model for common fields
- Create separate models for request, response, and API wrapper
- Use Pydantic for validation
- Make fields optional where appropriate
- Use field aliases for API compatibility (snake_case → camelCase)
- Add clear field descriptions
- Include proper type hints
- Don't create empty models just to wrap Dict[str, Any] - use the raw type instead
- Use @property methods in models for data transformation (e.g., error_detail property)

## Manager Class
- Keep focused on one resource type
- Initialize with required config (api_key, base_url)
- Method structure:
  - Clear docstring (purpose, params, returns, exceptions)
  - Prepare request
  - Make API call
  - Handle response
  - Handle errors
- Use type hints consistently
- Use SirenAPIError for API errors (400, 401, 404)
- Use SirenSDKError for SDK errors (validation, network)
- Keep data conversion logic in models, not managers
- Use model properties for error parsing rather than inline validation

## Client Class
- Keep thin, delegate to managers
- Method structure:
  - Clear docstring matching manager method
  - Delegate to manager
  - Return manager response
- Use proper type hints
- Keep error handling consistent

## Status Code Handling
- Use explicit status code checks (if status_code == 200) rather than response.ok

## Error Handling
- Use SirenAPIError for API errors:
  - Include status code
  - Include error code
  - Include API message
  - Include error details
- Use SirenSDKError for SDK errors:
  - Include original exception
  - Include clear message
  - Include status code if available

## Tests
- Structure:
  - Test success cases
  - Test error cases
  - Test validation
  - Test API errors
  - Test SDK errors
- Use clear mock data
- Verify request parameters
- Verify response handling
- Keep comments minimal but helpful

## Example Script
- Keep focused on demonstrating the method
- Structure:
  - Setup example data
  - Call method
  - Show basic response
  - Basic error handling
- Use realistic but safe data
- Keep output minimal
- Handle errors gracefully
- Keep comments focused

## Code Style
- Use type hints consistently
- Keep methods focused and small
- Use clear variable names
- Keep comments minimal but helpful
- Follow PEP 8
- Use consistent error handling
- Keep code flat where possible
- Use utility functions for common tasks

## Documentation
- Clear docstrings for all classes and methods
- Include parameter types and descriptions
- Include return types and descriptions
- Include possible exceptions
- Keep comments focused on why, not what

## Code Organization
- Keep related code together
- Use clear file structure
- Keep files focused
- Use consistent naming
- Keep code modular
